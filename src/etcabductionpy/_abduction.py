'''
abduction.py 
Exhaustive tree-leaf logical abduction
Andrew S. Gordon
'''

__all__ = ['abduction']

import itertools
from . import unify, skolemize
from . import Literal, KnowledgeBase

def abduction(obs: list[Literal], kb: KnowledgeBase, maxdepth: int, skolemize_solutions: bool = True):
    # exhaustive search for sets of leaf assumptions that entail the observations given the kb
    if not obs:
        return [] # no obs, no solutions
    for ob in obs:
        if ob.predicate not in kb._cpindex: return [] # kb can't handle these obs
    solutions = []
    listoflists = [and_or_leaflists([ob], kb, maxdepth, [], []) for ob in obs]
    for u in itertools.product(*listoflists):
        u = list(itertools.chain.from_iterable(u))
        solutions.extend(crunch(u))
    if skolemize_solutions:
        return [skolemize(solution) for solution in solutions]
    else:
        return solutions

def and_or_leaflists(remaining: list[Literal], kb: KnowledgeBase, depth: int, antecedents: list[Literal], assumptions: list[Literal]) -> 'list[list[Literal]]':
    if depth == 0 and antecedents: # fail
        return []
    if not remaining: # done with this level
        if not antecedents: # found one
            return [assumptions]
        else:
            return and_or_leaflists(antecedents, kb, depth - 1, [], assumptions)
    # more to go on this level
    literal = remaining[0] # first of remaining
    if literal.predicate not in kb._cpindex:
        return and_or_leaflists(remaining[1:], kb, depth, antecedents, [literal] + assumptions) # shift literal to assumptions
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
                 kb.standardize_literals([ant.subst(theta) for ant in dc.antecedents]) +
                 [ant.subst(theta) for ant in antecedents], # new antecedents with substitutions
                 [ass.subst(theta) for ass in assumptions] # new assumptions with substitutions
                 ]) 
    return itertools.chain(*[and_or_leaflists(*rev) for rev in revisions]) # list of lists (if any)

def crunch(conjunction: list[Literal]) -> list[list[Literal]]:
    # returns all possible ways that literals in a conjunction could be unified
    seen = set()
    results = []
    for solution in cruncher(conjunction, 0): # dedupe solutions
        key = frozenset(solution)
        if key not in seen:
            seen.add(key)
            results.append(list(key))
    return results

def cruncher(conjunction: list[Literal], idx: int = 0) -> list[list[Literal]]:
    if idx >= len(conjunction) - 1: # last one
        return [conjunction]
    else:
        res = []
        for subsequent in range(idx + 1, len(conjunction)):
            theta = unify(conjunction[idx], conjunction[subsequent])
            if theta != None:
                new_conjunction = [lit.subst(theta) for lit in conjunction[0:subsequent] + conjunction[(subsequent + 1):len(conjunction)]]
                res.extend(cruncher(new_conjunction, idx))
        res.extend(cruncher(conjunction, idx + 1))
        return res

