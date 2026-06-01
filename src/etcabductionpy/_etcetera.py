'''
etcetera.py
probability-ordered logical abduction
Andrew S. Gordon
'''

__all__ = ['etcetera', 'nbest', 'joint_log_probability']

from . import _abduction
from . import skolemize
from . import EtceteraLiteral, Literal, KnowledgeBase

import itertools
import bisect

def etcetera(obs: list[Literal], kb: KnowledgeBase, maxdepth: int, skolemize_solutions: bool = True) -> list[list[Literal]]:
    # Exhuastive search for conjunctions of etcetera literals that logically entail the observations
    if not obs:
        return [] # no obs, no solutions
    for ob in obs:
        if ob.predicate not in kb._cpindex: return [] # kb can't handle these obs
    solutions = []
    listoflists = [_abduction.and_or_leaflists([ob], kb, maxdepth, [], []) for ob in obs]
    for u in itertools.product(*listoflists):
        u = list(itertools.chain.from_iterable(u))
        solutions.extend(_abduction.crunch(u))
    solutions.sort(key=lambda item: joint_log_probability(item), reverse=True)
    if skolemize_solutions:
        return [skolemize(r) for r in solutions]
    else:
        return solutions    

def joint_log_probability(solution: list[EtceteraLiteral]) -> float:
    if not solution: return 0.0 # needed for incremental, log(1.0) = 0
    return sum(lit.log_probability for lit in solution)

def best_case_log_probability(solution: list[EtceteraLiteral]) -> float:
    # if we were wildly successful at unifiying all literals, what would the joint log prbability be?
    seen = set()
    total = 0.0
    for lit in solution:
        if lit.predicate not in seen:
            seen.add(lit.predicate)
            total += lit.log_probability
    return total

def nbest(obs: list[Literal], kb: KnowledgeBase, maxdepth: int, n: int, skolemize_solutions: bool = True) -> list[list[Literal]]:
    # returns n-best conjunctions of etcetera literals that logically entail the observations
    if not obs:
        return [] # no obs, no solutions
    for ob in obs:
        if ob.predicate not in kb._cpindex: return [] # kb can't handle these obs
    lpr2beat = -float('inf') # log probability to beat 
    nbest = [] # solutions
    nbest_lpr = [] # probabilities
    listoflists = [_abduction.and_or_leaflists([ob], kb, maxdepth, [], []) for ob in obs]
    for u in itertools.product(*listoflists):
        u = list(itertools.chain.from_iterable(u))
        bc = best_case_log_probability(u)
        if bc > lpr2beat:
            for solution in _abduction.crunch(u):
                jlpr = joint_log_probability(solution)
                if jlpr > lpr2beat:
                    insertAt = bisect.bisect_left(nbest_lpr, jlpr)
                    nbest.insert(insertAt, solution)
                    nbest_lpr.insert(insertAt, jlpr)
                    if len(nbest) > n:
                        nbest.pop(0)
                        nbest_lpr.pop(0)
                        lpr2beat = nbest_lpr[0] # only if full
    nbest.reverse() # highest first
    if skolemize_solutions:
        return [skolemize(solution) for solution in nbest]
    else:
        return nbest

