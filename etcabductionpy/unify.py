# unify.py
# A most-general-unifier unification algorithm for arbitrary s-expressions
# Andrew S. Gordon
# Fall 2015

def unify(x, y, theta = {}):
    if theta == None:
        return None
    elif x == y:
        return theta
    elif variablep(x):
        return unify_var(x,y,theta)
    elif variablep(y):
        return unify_var(y,x,theta)
    elif listp(x) and listp(y) and len(x) == len(y):
        return unify(x[1:], y[1:], unify(x[0], y[0], theta))
    else:
        return None

def unify_var(var, x, theta):
    if variablep(x) and var < x: # prevents circularities
        return unify_var(x, var, theta)
    elif var in theta:
        return unify(theta[var], x, theta)
    elif occur_check(var,x):
        return None
    else:
        theta_copy = theta.copy()
        theta_copy[var] = x
        return theta_copy

def occur_check(var, x):
    if var == x:
        return True
    elif listp(x):
        for i in x:
            if occur_check(var, i): return True
    return False

def subst(theta, x):
    if listp(x):
        return [subst(theta, z) for z in x]
    elif x in theta and variablep(x):
        return subst(theta, theta[x])
    else:
        return x
    
def listp(item): # includes both literals and functions
    return isinstance(item, list)

def variablep(item): # a string that starts with a question mark
    return isinstance(item, str) and len(item) > 1 and item[0] == "?"
