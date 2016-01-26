# unify.py
# A most-general-unifier unification algorithm for arbitrary s-expressions
# Andrew S. Gordon

def unify(x, y, theta = {}, functions = False):
    # return unify1(x, y, theta) # old
    if functions:
        return robinson(x, y, {})
    else:
        return nofunctions(x, y, {})

# Support functions

def subst(theta, x):
    if listp(x):
        return [subst(theta, z) for z in x]
    elif x in theta and variablep(x): # redundant?
        return subst(theta, theta[x])
    else:
        return x
    
def listp(item): # includes both literals and functions
    return isinstance(item, list)

def variablep(item): # a string that starts with a question mark
    return isinstance(item, str) and len(item) > 1 and item[0] == "?"

def countup(prefix = "_"):
    '''Unique symbol name generator'''
    n = 1
    while True:
        yield prefix + str(n)
        n += 1

standardized_universals = countup('?#') # use standardized_universals.next() to get the next one

def all_variables(sexp):
    '''returns the set of all ?variables'''
    #if isinstance(sexp, str) and sexp[0] == '?':
    if variablep(sexp):
        return set([sexp])
    elif isinstance(sexp, list):
        return set().union(*[all_variables(item) for item in sexp])
    else:
        return set()

def standardize(sexp):
    '''Ensures that all variable ?names in an s-expression are standardized variables, e.g. ?#42'''
    foreigners = [x for x in all_variables(sexp) if not x[0:2] == "?#"]
    aliases = {}
    for f in foreigners:
        aliases[f] = standardized_universals.next()
    return subst(aliases, sexp)

def skolemize(sexp):
    skolem_constants = countup('$') # use skolem_constants.next() to get the next one
    all_vars = all_variables(sexp)
    instances = {}
    for var in all_vars:
        instances[var] = skolem_constants.next()
    return subst(instances, sexp)


# Version 1 : Classic style of old LISP programmers
    
def unify1(x, y, theta = {}):
    if theta == None:
        return None
    elif x == y:
        return theta
    elif variablep(x):
        return unify_var(x,y,theta)
    elif variablep(y):
        return unify_var(y,x,theta)
    elif listp(x) and listp(y) and len(x) == len(y):
        return unify1(x[1:], y[1:], unify1(x[0], y[0], theta))
    else:
        return None

def unify_var(var, x, theta):
    if variablep(x) and var < x: # prevents circularities
        return unify_var(x, var, theta)
    elif var in theta:
        return unify1(theta[var], x, theta)
    elif occur_check(var,x):
        return None
    else:
        theta_copy = theta.copy()
        theta_copy[var] = x
        return theta_copy
#        theta[var] = x
#        return theta
        
def occur_check(var, x):
    if var == x:
        return True
    elif listp(x):
        for i in x:
            if occur_check(var, i): return True
    return False



# Version 2: Robinson's 1965 Unification Algorithm

def robinson(x, y, theta = {}):
    stack = [(x,y)]
    while stack:
        s, t = stack.pop()
        while (variablep(s) and
               (s in theta)):
            s = theta[s]
        while (variablep(t) and
               (t in theta)):
            t = theta[t]
        if s != t:
            if variablep(s):
                if variablep(t):
                    #theta[s] = t
                    if s < t: # deal with standardized/non-standardized var ordering
                        theta[t] = s
                    else:
                        theta[s] = t
                else:
                    if robOccursCheck(s,t,theta):
                        theta[s] = t
                    else:
                        return None
            elif variablep(t):
                if robOccursCheck(t,s,theta):
                    theta[t] = s
                else:
                    return None
            elif (isinstance(s, list) and
                  isinstance(t, list) and
                  len(s) == len(t) and
                  s[0] == t[0]):
                stack.extend(zip(s[1:], t[1:]))
            else:
                return None
    return theta

def robOccursCheck(var, target, theta):
    stack = [target]
    while stack:
        t = stack.pop()
        for z in allvars(target):
            if var == z:
                return false
            if z in theta:
                stack.append(theta[z])
    return True

def allvars(term):
    res = []
    stack = [term]
    while stack:
        t = stack.pop()
        if isinstance(t, list):
            stack.extend(t[1:])
        elif variablep(t):
            res.append(t)
    return res


# Version 3: Faster, but no functions

def nofunctions(x, y, theta = {}):
    # unifies two lists not containing lists
    lx = len(x)
    if lx != len(y):
        return None
    for i in xrange(lx):
        s = x[i]
        t = y[i]
        while s in theta:
            s = theta[s]
        while t in theta: 
            t = theta[t]
        if s != t:
            if s[0] == "?": # cheaper var test
                if t[0] == "?" and s < t: # deal with standardized/non-standardized var ordering
                    theta[t] = s
                else:
                    theta[s] = t
            elif t[0] == "?": # cheaper var test
                theta[t] = s
            else:
                return None
    return theta
                
        
                
# Todo: standardize and subst in single function (optimization)
