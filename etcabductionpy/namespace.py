# namespace.py
# Dealing with namespace issues for variables in s-expressions
# Andrew S. Gordon

import unify

# namespace

def variablep(item): # a string that starts with a question mark
    return isinstance(item, str) and len(item) > 1 and item[0] == "?"

def namespace_variablep(item): # a string that starts with "?#"
    return isinstance(item, str) and len(item) > 2 and item[0:2] == "?#"

def countup(prefix = "_"):
    '''Unique symbol name generator'''
    n = 1
    while True:
        yield prefix + str(n)
        n += 1

namespace_universals = countup('?#') # use namespace_universals.next() to get the next one

def foreign_variables(sexp):
    return [x for x in all_variables(sexp) if not namespace_variablep(x)]

def all_variables(sexp):
    '''returns the set of all ?variables'''
    #if isinstance(sexp, str) and sexp[0] == '?':
    if variablep(sexp):
        return set([sexp])
    elif isinstance(sexp, list):
        return set().union(*[all_variables(item) for item in sexp])
    else:
        return set()

def namespace(sexp):
    '''Ensures that all variable ?names in an s-expression are in the namespace, e.g. ?#42'''
    foreigners = foreign_variables(sexp)
    aliases = {}
    for f in foreigners:
        aliases[f] = namespace_universals.next()
    return unify.subst(aliases, sexp)

def skolemize(sexp):
    skolem_constants = countup('$') # use skolem_constants.next() to get the next one
    all_vars = all_variables(sexp)
    instances = {}
    for var in all_vars:
        instances[var] = skolem_constants.next()
    return unify.subst(instances, sexp)

# Todo
# Refactor: standardize(sexp), standardized_variablep(item), unstandardized_variables(sexp),
#           subst_only_standardized_variables(theta, x), subst_and_standardize(theta, x),
#           standardized_universals,
# Move to unify.py


