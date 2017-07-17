import unify
import abduction
import bisect
import itertools
import etcetera

def incremental(obs, kb, maxdepth, n, w, b, skolemize = True):
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



