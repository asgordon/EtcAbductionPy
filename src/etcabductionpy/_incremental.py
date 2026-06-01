'''
incremental.py
incremental etcetera abduction
Andrew S. Gordon
'''

__all__ = ['incremental']

from . import Literal, KnowledgeBase
from . import _abduction
from . import _etcetera
from . import skolemize
from . import forward
from . import unify

import itertools, bisect
from collections.abc import Iterable

# This version of incremental treats each previous
# hypothesis in the beam as its own context, and regenerates the
# and_or_leaflists to include solutions that rely on assumptions in
# this context. Done this way, the past solutions do not have to be
# cruched with the solutions to the current window, which makes it
# more amiable to very large problems.

def incremental(obs: list[Literal], kb: KnowledgeBase, maxdepth: int, n: int, w: int, b: int, skolemize_solutions: bool = True) -> list[list[Literal]]:
    
    if not obs:
        return [] # no obs, no solutions
    for ob in obs:
        if ob.predicate not in kb._cpindex: return [] # kb can't handle these obs

    iteration = 1 # count for skolem constants
    previous = [] # proofs of the previous
    remaining = list(obs) # obs yet to be interpreted (copy)

    # first, interpret the first window as normal
    window = remaining[0:w]
    remaining = remaining[w:]
    lpr2beat = -float('inf') # log probability to beat 
    nbest = [] # solutions
    nbest_lpr = [] # probabilities
    listoflists = [_abduction.and_or_leaflists([ob], kb, maxdepth, [], []) for ob in window]
    for u in itertools.product(*listoflists):
        u = list(itertools.chain.from_iterable(u))
        bc = _etcetera.best_case_log_probability(u)
        if bc > lpr2beat:
            for solution in _abduction.crunch(u):
                jlpr = _etcetera.joint_log_probability(solution)
                if jlpr > lpr2beat:
                    insertAt = bisect.bisect_left(nbest_lpr, jlpr)
                    nbest.insert(insertAt, solution)
                    nbest_lpr.insert(insertAt, jlpr)
                    if len(nbest) > b: # beam
                        nbest.pop(0)
                        nbest_lpr.pop(0)
                        lpr2beat = nbest_lpr[0] # only if full
    nbest.reverse() # highest first
    previous = nbest
    pre = "$" + str(iteration) + ":"
    previous = [skolemize(r, prefix=pre) for r in previous] # skolemize the past (required)

    # next, interpret remaining windows in a special way
    while remaining:
        iteration += 1
        window = remaining[0:w]
        remaining = remaining[w:]
        lpr2beat = -float('inf') # log probability to beat
        nbest = []
        nbest_lpr = []
        for previousSolution in previous:
            previousSolution_jlpr = _etcetera.joint_log_probability(previousSolution)
            context = get_context(previousSolution, obs, kb)
            listoflists = [contextual_and_or_leaflists([ob], kb, maxdepth, context) for ob in window]

            for u in itertools.product(*listoflists):
                u = list(itertools.chain.from_iterable(u))
                bc = _etcetera.best_case_log_probability(u)
                if bc + previousSolution_jlpr > lpr2beat:
                    for solution in _abduction.crunch(u):
                        jlpr = _etcetera.joint_log_probability(solution) + previousSolution_jlpr
                        if jlpr > lpr2beat:
                            insertAt = bisect.bisect_left(nbest_lpr, jlpr)
                            nbest.insert(insertAt, previousSolution + solution) # joined
                            nbest_lpr.insert(insertAt, jlpr)
                            if len(nbest) > b: # beam
                                nbest.pop(0)
                                nbest_lpr.pop(0)
                                lpr2beat = nbest_lpr[0] # only if full
        nbest.reverse() # highest first
        previous = nbest
        pre = "$" + str(iteration) + ":"
        previous = [skolemize(r, prefix=pre) for r in previous] # skolemize the past (required)
    return previous[0:n]

def get_context(solution: list[Literal], obs: list[Literal], kb: KnowledgeBase) -> list[Literal]:
    withDuplicates = [item[0] for item in forward(solution, kb)] # why contains duplicates?
    res = []
    for item in withDuplicates:
        if item not in res and item not in obs:
            res.append(item)
    return res

# todo: Write alternative to forward.forward that quickly produces unique, none observable inferences (?)

def contextual_and_or_leaflists(remaining: list[Literal], kb: KnowledgeBase, depth: int, context: list[Literal], antecedents: list[Literal] | None = None, assumptions: list[Literal] | None = None) -> Iterable[list[Literal]]:
    antecedents = antecedents or []
    assumptions = assumptions or []
    if depth == 0 and antecedents: # fail
        return []
    if not remaining: # done with this level
        if not antecedents: # found one
            return [assumptions]
        else:
            return contextual_and_or_leaflists(antecedents, kb, depth - 1, context, [], assumptions)
    # more to go on this level
    literal = remaining[0] # first of remaining
    if literal.predicate not in kb._cpindex:
        return contextual_and_or_leaflists(remaining[1:], kb, depth, context, antecedents, [literal] + assumptions) # shift literal to assumptions
    revisions = []
    for dc in kb._cpindex[literal.predicate]: # definite clause
        theta = unify(literal, dc.consequent)
        if theta != None:
            if depth == 0: # no depth for revision
                return [] # fail
            revisions.append([
                [lit.subst(theta) for lit in remaining[1:]],
                 kb,
                 depth,
                 context,
                 kb.standardize_literals([ant.subst(theta) for ant in dc.antecedents]) +
                 [ant.subst(theta) for ant in antecedents], # new antecedents with substitutions
                 [ass.subst(theta) for ass in assumptions] # new assumptions with subsitutions
            ])
    for contextliteral in context:
        theta = unify(literal, contextliteral)
        if theta != None: # literal unifies with context
            revisions.append([
                [lit.subst(theta) for lit in remaining[1:]],
                kb,
                depth,
                context, # not revised
                [ant.subst(theta) for ant in antecedents], # antecedents
                [ass.subst(theta) for ass in assumptions] # assumptions
            ])
            # should we break here now that we've found one? Don't know
    return itertools.chain(*[contextual_and_or_leaflists(*rev) for rev in revisions]) # list of lists (if any)
