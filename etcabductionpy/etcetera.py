'''etcetera.py
Probability-ordered logical abduction for a Knowledge Base of definite clauses 
Andrew S. Gordon
'''

import bisect
import itertools
import functools

from . import unify
from . import abduction

def etcetera(obs, kb, maxdepth, skolemize = True):
    '''Exhuastive search for conjunctions of etctera literals that logically entail the observations'''
    indexed_kb = abduction.index_by_consequent_predicate(kb)
    res = []
    listoflists = [abduction.and_or_leaflists([ob], indexed_kb, maxdepth) for ob in obs]
    for u in itertools.product(*listoflists):
        u = list(itertools.chain.from_iterable(u))
        res.extend(abduction.crunch(u))
    res.sort(key=lambda item: joint_probability(item), reverse=True)
    if skolemize:
        return [unify.skolemize(r) for r in res]
    else:
        return res

def joint_probability(etcs):
    '''Product of probabitilies of etctera literals, and 1.0 for empty list'''
    if not etcs: return 1.0 # needed for incremental
    return functools.reduce(lambda x, y: x*y, [l[1] for l in etcs])

def best_case_probability(etcs):
    '''If we were wildly successful at unifing all literals, what would the joint probability be?'''
    predicateSet = set()
    pr = 1.0
    for literal in etcs:
        # if literal[0][0:3] != 'etc': raise ValueError('Not an etcetera literal: ' + str(literal))
        if literal[0] not in predicateSet:
            predicateSet.add(literal[0])
            pr = pr * literal[1]
    return pr

def nbest(obs, kb, maxdepth, n, skolemize = True):
    '''Returns n-best conjunctions of etcetera literals that logically entail the observations'''
    indexed_kb = abduction.index_by_consequent_predicate(kb)
    pr2beat = 0.0
    nbest = [] # solutions
    nbestPr = [] # probabilities
    listoflists = [abduction.and_or_leaflists([ob], indexed_kb, maxdepth) for ob in obs]
    for u in itertools.product(*listoflists):
        u = list(itertools.chain.from_iterable(u))
        if best_case_probability(u) > pr2beat:
            for solution in abduction.crunch(u):
                jpr = joint_probability(solution)
                if jpr > pr2beat:
                    insertAt = bisect.bisect_left(nbestPr, jpr)
                    nbest.insert(insertAt, solution)
                    nbestPr.insert(insertAt, jpr)
                    if len(nbest) > n:
                        nbest.pop(0)
                        nbestPr.pop(0)
                        pr2beat = nbestPr[0] # only if full
    nbest.reverse() # [0] is now highest
    if skolemize:
        return [unify.skolemize(r) for r in nbest]
    else:
        return nbest
