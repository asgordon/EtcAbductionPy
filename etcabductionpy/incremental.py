# incremental.py
# Incremental version of Etcetera Abduction
# Andrew S. Gordon

import unify
import abduction
import etcetera
import forward
import parse

import bisect
import itertools
import sys


def incremental(obs, kb, maxdepth, n, w, b, skolemize = True):
    #return incremental1(obs, kb, maxdepth, n, w, b, skolemize)
    return incremental2(obs, kb, maxdepth, n, w, b, skolemize)

# incremental1 is the first attempt. It does the simplest possible
# thing, which is to break large problems into smaller ones of a fixed
# size, then treats solutions to the past in the beam as proofs of
# another observation, combining them with current solutions to find
# the most probable. It works well on medium problems, but big
# problems tend to create very large sets of etcetera literals for
# explaining the past, which causes a lot of headache when the
# algorithm must crunch a solution.

def incremental1(obs, kb, maxdepth, n, w, b, skolemize = True):
    # n = n-best
    # w = window size
    # b = beam of running candidate interpretations
    indexed_kb = abduction.index_by_consequent_predicate(kb)
    previous = [] # proofs of the previous
    while len(obs) > 0:
        window = obs[0:w]
        obs = obs[w:]
        listoflists = [abduction.and_or_leaflists([ob], indexed_kb, maxdepth) for ob in window]
        if len(previous) > 0:
            listoflists.append(previous)
        pr2beat = 0.0
        nbest = [] # solutions
        nbestPr = [] # probabilities
        for u in itertools.product(*listoflists):
            u = list(itertools.chain.from_iterable(u))
            if etcetera.bestCaseProbability(u) > pr2beat:
                for solution in abduction.crunch(u):
                    jpr = etcetera.jointProbability(solution)
                    if jpr > pr2beat:
                        insertAt = bisect.bisect_left(nbestPr, jpr)
                        nbest.insert(insertAt, solution)
                        nbestPr.insert(insertAt, jpr)
                        if len(nbest) > b:
                            nbest.pop(0)
                            nbestPr.pop(0)
                            pr2beat = nbestPr[0] # only if full
        nbest.reverse() # [0] is now highest
        previous = nbest
    if skolemize:
        return [unify.skolemize(r) for r in previous[0:n]] # only skolemize nbest
    else:
        return previous[0:n]

# incremental2 is the second attempt. It treats each previous
# hypothesis in the beam as its own context, and regenerates the
# and_or_leaflists to include solutions that rely on assumptions in
# this context. Done this way, the past solutions do not have to be
# cruched with the solutions to the current window, which makes it
# more amiable to very large problems.
    
def incremental2(obs, kb, maxdepth, n, w, b, skolemize = True):
    # n = n-best
    # w = window size
    # b = beam of running candidate interpretations
    iteration = 1 # count for skolem constants
    indexed_kb = abduction.index_by_consequent_predicate(kb)
    previous = [] # proofs of the previous
    remaining  = obs[:] # obs yet to be interpretated

    # first, interpret the first window as normal
    window = remaining[0:w]
    remaining = remaining[w:]
    listoflists = [abduction.and_or_leaflists([ob], indexed_kb, maxdepth) for ob in window]
    pr2beat = 0.0
    nbest = [] # solutions
    nbestPr = [] # probabilities
    for u in itertools.product(*listoflists):
        u = list(itertools.chain.from_iterable(u))
        if etcetera.bestCaseProbability(u) > pr2beat:
            for solution in abduction.crunch(u):
                jpr = etcetera.jointProbability(solution)
                if jpr > pr2beat:
                    insertAt = bisect.bisect_left(nbestPr, jpr)
                    nbest.insert(insertAt, solution)
                    nbestPr.insert(insertAt, jpr)
                    if len(nbest) > b:
                        nbest.pop(0)
                        nbestPr.pop(0)
                        pr2beat = nbestPr[0] # only if full
    nbest.reverse() # [0] is now highest
    previous = nbest
    pre = "$" + str(iteration) + ":"
    previous = [unify.skolemize(r, prefix=pre) for r in previous] # skolemize the past (required)
    
    # next, interpret remaining windows in a special way
    while len(remaining) > 0:
        iteration += 1
        window = remaining[0:w]
        remaining = remaining[w:]
        pr2beat = 0.0
        nbest = [] # solutions
        nbestPr = [] # probabilities
        for previousSolution in previous:
            previousSolutionJpr = etcetera.jointProbability(previousSolution)
            context = getContext(previousSolution, obs, kb)
            listoflists = [contextual_and_or_leaflists([ob], indexed_kb, maxdepth, context) for ob in window]

            for u in itertools.product(*listoflists):
                u = list(itertools.chain.from_iterable(u))
                if etcetera.bestCaseProbability(u) * previousSolutionJpr > pr2beat:
                    for solution in abduction.crunch(u):
                        jpr = etcetera.jointProbability(solution) * previousSolutionJpr
                        if jpr > pr2beat:
                            insertAt = bisect.bisect_left(nbestPr, jpr)
                            nbest.insert(insertAt, previousSolution + solution) # joined
                            nbestPr.insert(insertAt, jpr)
                            if len(nbest) > b:
                                nbest.pop(0)
                                nbestPr.pop(0)
                                pr2beat = nbestPr[0] # only if full
        nbest.reverse() # [0] is now highest
        previous = nbest
        pre = "$" + str(iteration) + ":"
        previous = [unify.skolemize(r, prefix=pre) for r in previous] # skolemize the past (required)
    return previous[0:n]
    
def getContext(solution, obs, kb):
    withDuplicates = [item[0] for item in forward.forward(solution, kb)] # why contains duplicates?
    res = []
    for item in withDuplicates:
        if item not in res and item not in obs:
            res.append(item)
    return res

# todo: Write alternative to forward.forward that quickly produces
# unique, none observable inferences

def contextual_and_or_leaflists(remaining, indexed_kb, depth, context, antecedents = [], assumptions = []):
    '''Returns list of all entailing sets of leafs in the and-or backchaining tree, with belief context'''
    if depth == 0 and len(antecedents) > 0: # fail
        return [] # (empty) list of lists
    elif len(remaining) == 0: # done with this level
        if len(antecedents) == 0: # found one
            return [assumptions] # list of lists
        else:
            return contextual_and_or_leaflists(antecedents, indexed_kb, depth - 1, context, [], assumptions)
    else: # more to go on this level
        literal = remaining[0] # first of remaining
        predicate = literal[0]

        if predicate not in indexed_kb:
            return contextual_and_or_leaflists(remaining[1:], indexed_kb, depth, context, antecedents, [literal] + assumptions)
            # shift literal to assumptions
        else:
            revisions = [] 
            for rule in indexed_kb[predicate]: # indexed by predicate of literal
                theta = unify.unify(literal, parse.consequent(rule))
                if theta != None:
                    if depth == 0: # no depth for revision
                        return [] # (empty) list of lists
                    revisions.append([unify.subst(theta, remaining[1:]), # new remaining with substitutions
                                      indexed_kb,
                                      depth,
                                      context,
                                      unify.standardize(unify.subst(theta, parse.antecedent(rule))) +
                                      unify.subst(theta, antecedents),  # new antecedents with substitutions
                                      unify.subst(theta, assumptions)]) # new assumptions with substitutions
            for contextliteral in context:
                theta = unify.unify(literal, contextliteral)
                if theta != None: # literal unifies with context
                    revisions.append([unify.subst(theta, remaining[1:]), # new remaining with substitutions
                                      indexed_kb,
                                      depth,
                                      context, # not revised
                                      unify.subst(theta, antecedents), # antecedents
                                      unify.subst(theta, assumptions) # assumptions
                    ])
                    # should we "break" here now that we've found one?
            return itertools.chain(*[contextual_and_or_leaflists(*rev) for rev in revisions]) # list of lists (if any)
