# abduction.py
# Logical abduction for kb of definite clauses
# Andrew S. Gordon

import parse
import unify
import namespace
import itertools

def abduction(obs, kb, maxdepth, skolemize = True):
    '''Logical abduction: returns a list of all sets of assumptions that entail the observations given the kb'''
    indexed_kb = index_by_consequent_predicate(kb)
    res = []
    for leaflist in and_or_leaflists(obs, indexed_kb, maxdepth):
        res.extend(crunch(leaflist))
    if skolemize:
        return [namespace.skolemize(r) for r in res]
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
    if depth == 0 and len(antecedents) > 0: # fail
        return [] # (empty) list of lists
    elif len(remaining) == 0: # done with this level
        if len(antecedents) == 0: # found one
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
                    revisions.append([namespace.namespace_subst(theta, remaining[1:]), # new remaining with namespace substitutions
                                      indexed_kb,
                                      depth,
                                      namespace.namespace(unify.subst(theta, parse.antecedent(rule))) +
                                      namespace.namespace_subst(theta, antecedents),  # new antecedents with namespace substitutions
                                      namespace.namespace_subst(theta, assumptions)]) # new assumptions with namespace substitutions
            return itertools.chain(*[and_or_leaflists(*rev) for rev in revisions]) # list of lists (if any)

def crunch(conjunction): # returns a list of all possible ways to unify conjunction literals
    res = [conjunction] # start with one solution
    pairs = itertools.combinations(conjunction, 2)
    thetas = [theta for theta in [unify.unify(p[0], p[1]) for p in pairs] if theta is not None]
    ps = powerset(thetas)
    for thetaset in ps: 
        if len(thetaset) > 0:
            consistent = mergethetas(thetaset)
            if consistent:
                res.append([k for k,v in itertools.groupby(sorted(unify.subst(consistent, conjunction)))])
    return res

def mergethetas(thetaset):
    '''Merge all substitutions into a single dictionary, or None if not consistent'''
    x = []
    y = []
    for theta in thetaset:
        for var in theta:
            x.append(var)
            y.append(theta[var])
    return unify.unify(x,y)

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1))

