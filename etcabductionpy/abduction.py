'''abduction.py
Base functionality for logical abduction using a knowledge base of definite clauses
Andrew S. Gordon
'''

import itertools

from . import parse
from . import unify

def abduction(obs, kb, maxdepth, skolemize = True):
    '''Logical abduction: returns a list of all sets of assumptions that entail the observations given the kb'''
    indexed_kb = index_by_consequent_predicate(kb)
    res = []
    listoflists = [and_or_leaflists([ob], indexed_kb, maxdepth) for ob in obs]
    for u in itertools.product(*listoflists):
        u = list(itertools.chain.from_iterable(u))
        res.extend(crunch(u))
    if skolemize:
        return [unify.skolemize(r) for r in res]
    else:
        return res

def index_by_consequent_predicate(kb):
    res = {}
    for dc in kb:
        predicate = parse.consequent(dc)[0]
        if predicate in res:
            res[predicate].append(dc)
        else:
            res[predicate] = [dc]
    return res

def and_or_leaflists(remaining, indexed_kb, depth, antecedents = [], assumptions = []):
    '''Returns list of all entailing sets of leafs in the and-or backchaining tree'''
    if depth == 0 and antecedents: # fail
        return [] # (empty) list of lists
    elif not remaining: # done with this level
        if not antecedents:  # found one
            return [assumptions] # list of lists
        else:
            return and_or_leaflists(antecedents, indexed_kb, depth - 1, [], assumptions)
    else: # more to go on this level
        literal = remaining[0] # first of remaining
        predicate = literal[0]
        if predicate not in indexed_kb:
            return and_or_leaflists(remaining[1:], indexed_kb, depth, antecedents, [literal] + assumptions) # shift literal to assumptions
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
                                      unify.standardize(unify.subst(theta, parse.antecedent(rule))) +
                                      unify.subst(theta, antecedents),  # new antecedents with substitutions
                                      unify.subst(theta, assumptions)]) # new assumptions with substitutions
            return itertools.chain(*[and_or_leaflists(*rev) for rev in revisions]) # list of lists (if any)

def crunch(conjunction):
    '''Returns all possible ways that literals in a conjunction could be unified'''
    return [k for k,v in itertools.groupby(sorted(cruncher(conjunction, 0)))] # dedupe solutions

def cruncher(conjunction, idx = 0):
    if idx >= len(conjunction) - 1: # last one
        return [[k for k,v in itertools.groupby(sorted(conjunction))]] # dedupe literals in solution
    else:
        res = []
        for subsequent in range(idx + 1,len(conjunction)): 
            theta = unify.unify(conjunction[idx], conjunction[subsequent])
            if theta:

                new_conjunction = unify.subst(theta,
                                              conjunction[0:subsequent] +
                                              conjunction[(subsequent + 1):len(conjunction)])
                res.extend(cruncher(new_conjunction, idx))
        res.extend(cruncher(conjunction, idx + 1))
        return res
