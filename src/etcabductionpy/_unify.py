'''
unify.py
Fast and simple unification of first-order logic literals
Andrew S. Gordon
'''
__all__ = ['unify', 'skolemize']

from . import Literal, Term

def unify(x: Literal, y: Literal) -> 'dict[Term, Term]':
    return functionless_unify(x, y)

def functionless_unify(x: Literal, y: Literal) -> 'dict[Term, Term]':
    # returns theta if success, returns None if not
    if x == y:
        return {}
    if x.predicate != y.predicate:
        return None
    if len(x.arguments) != len(y.arguments):
        return None
    theta = {} # dict[Term, Term]
    for termx, termy in zip(x.arguments, y.arguments):
        while termx in theta:
            termx = theta[termx]
        while termy in theta:
            termy = theta[termy]
        if termx != termy:
            if termx.is_variable:
                if termy.is_variable and termx < termy: # deal with standardized/non-standardized var ordering
                    theta[termy] = termx
                else:
                    theta[termx] = termy
            elif termy.is_variable:
                theta[termy] = termx
            else:
                return None
    # remove indirects
    for v in theta:
        while theta[v] in theta:
            theta[v] = theta[theta[v]]
    return theta

def countup(prefix = "_"):
    '''Unique symbol name generator'''
    n = 1
    while True:
        yield prefix + str(n)
        n += 1

def skolemize(solution: list[Literal], prefix: str = "$") -> 'list[Literal]':
    # converts any variables in a solution into Skolem constants
    skolem_constants = countup(prefix)
    theta = {} # dict{Term: Term}
    all_vars = set()
    for lit in solution:
        all_vars.update(lit.all_variables())
    for var in sorted(all_vars):
        if var not in theta:
            theta[var] = Term(next(skolem_constants))
    return [lit.subst(theta) for lit in solution]



