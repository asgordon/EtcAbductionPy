# etcetera.py
# Etcetera Abduction: Probability-ordered logical abduction for kb of definite clauses 
# Andrew S. Gordon
# Fall 2015

from __future__ import print_function
import argparse
import sys
import parse
import namespace
import forward
import abduction
import bisect

def etcAbduction(obs, kb, maxdepth, skolemize = True):
    '''Logical abduction: returns a list of all sets of assumptions that entail the observations given the kb'''
    indexed_kb = abduction.index_by_consequent_predicate(kb)
    res = []
    for u in abduction.and_or_leaflists(obs, indexed_kb, maxdepth):
        res.extend(abduction.crunch(u))
    res.sort(key=lambda item: jointProbability(item), reverse=True)
    if skolemize:
        return [namespace.skolemize(r) for r in res]
    else:
        return res

def jointProbability(etcs):
    return reduce(lambda x, y: x*y, [l[1] for l in etcs])

def bestCaseProbability(etcs):
    '''If we were wildly successful at unifing all literals, what would the joint probability be?'''
    predicateSet = set()
    pr = 1.0
    for literal in etcs:
        if literal[0] not in predicateSet:
            predicateSet.add(literal[0])
            pr = pr * literal[1]
    return pr

def nbest(obs, kb, maxdepth, n, skolemize = True):
    indexed_kb = abduction.index_by_consequent_predicate(kb)
    pr2beat = 0.0
    nbest = [] # solutions
    nbestPr = [] # probabilities
    for u in abduction.and_or_leaflists(obs, indexed_kb, maxdepth):
        if bestCaseProbability(u) > pr2beat:
            for solution in abduction.crunch(u):
                jpr = jointProbability(solution)
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
        return [namespace.skolemize(r) for r in nbest]
    else:
        return nbest

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description='Etcetera abduction for kb of definite clauses')
    argparser.add_argument('-i', '--infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    argparser.add_argument('-o', '--outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    argparser.add_argument('-g', '--graph', action="store_true", help='Output graph in .dot format')
    argparser.add_argument('-s', '--solution', type=int, default=1, help='Graph solution number s')
    argparser.add_argument('-d', '--depth', type=int, default=5, help='Backchain to depth d')
    argparser.add_argument('-n', '--nbest', type=int, default=10, help='Generate n-best proofs')
    argparser.add_argument('-a', '--all', action="store_true", help='Generate all proofs')
    args = argparser.parse_args()

    lines = args.infile.readlines()
    intext = "".join(lines)
    kb, obs = parse.definite_clauses(parse.parse(intext))

    if args.all:
        solutions = etcAbduction(obs, kb, args.depth)
    else:
        solutions = nbest(obs, kb, args.depth, args.nbest)

    if args.graph:
        solution = solutions[args.solution - 1]
        print(forward.graph(solution, forward.forward(solution, kb), targets=obs), file=args.outfile)
    else:
        for solution in solutions:
            print(solution, file=args.outfile)
