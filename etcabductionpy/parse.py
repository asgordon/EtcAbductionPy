# parse.py
# A simple parser for definite clauses in first order logic
# Andrew S. Gordon


from __future__ import print_function
import argparse
import sys

def parse(src):
    '''Parse multiple expressions in src text into a list of python list s-expressions'''
    return(variablize(sexp(wrap(src))))

def sexp(src):
    '''Convert src text into a python list s-expressions'''
    return read_from_tokens(tokenize(decomment(src)))

def decomment(src):
    '''Ignore anything on a line following a semicolon'''
    lines = src.split('\n')
    lines = [l.partition(';')[0] for l in lines]
    return " ".join(lines)

def tokenize(chars):
    '''split src into tokens on whitespace or parentheses'''
    return decomment(chars).replace('(', ' ( ').replace(')', ' ) ').split()

def wrap(src):
    '''Wrap an outer list around your src file'''
    return '(' + src + ')'

def read_from_tokens(tokens):
    '''Read an expression from a sequence of tokens.'''
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF while reading')
    token = tokens.pop(0)
    if '(' == token:
        L = []
        while tokens[0] != ')':
            L.append(read_from_tokens(tokens))
        tokens.pop(0) # pop off ')'
        return L
    elif ')' == token:
        raise SyntaxError('unexpected )')
    else:
        return cast(token)

def cast(token):
    '''Numbers become numbers; every other token is a symbol.'''
    try: return int(token)
    except ValueError:
        try: return float(token)
        except ValueError:
            return token

def definite_clauses(expressions):
    '''Separates definite clauses from everything else in a list of expressions'''
    yes = []
    no = []
    for e in expressions:
        if isinstance(e, list) and len(e) == 3 and e[0] == 'if':
            yes.append(e)
        else:
            no.append(e)
    return (yes,no)

def antecedent(rule): # always a list of literals
    if (rule[1][0] == 'and'):
        return rule[1][1:]
    else:
        return [rule[1]]

def consequent(rule): # always a literal
    return rule[2]
    
def all_variables(sexp):
    '''returns the set of all ?variables'''
    if isinstance(sexp, str) and sexp[0] == '?':
        return set([sexp])
    elif isinstance(sexp, list):
        return set().union(*[all_variables(item) for item in sexp])
    else:
        return set()

def literals(definite_clause):
    if (isinstance(definite_clause, list) and
        len(definite_clause) == 3 and
        isinstance(definite_clause[1], list) and
        len(definite_clause[1]) > 0):
        if definite_clause[1][0] == 'and':
            return definite_clause[1][1:] + [definite_clause[2]]
        else:
            return [definite_clause[1], definite_clause[2]]
    else:
        raise SyntaxError("Malformed definite_clause: " + str(definite_clause))

def functions(literal): 
    '''Returns a list of all of the functions used in the arguments of the literal'''
    if literal == []:
        return []
    if isinstance(literal[0], list):
        return [literal[0]] + functions(literal[1:]) 
    else:
        return functions(literal[1:])
    pass

def variablize(sexp):
    '''Converts any lowercase-beginning term in the [1:] of any list into a ?term'''
    if isinstance(sexp, list) == False: # problem
        return sexp
    else:
        res = []
        for i in range(len(sexp)): # was xrange
            if isinstance(sexp[i], list):
                res.append(variablize(sexp[i]))
            elif (i > 0 and isinstance(sexp[i], str) and sexp[i][0].islower()):
                res.append("?" + sexp[i])
            else:
                res.append(sexp[i])
        return res

def display(sexp):
    '''Convert a sexp into a string'''
    if isinstance(sexp, list):
        return "(" + " ".join([display(s) for s in sexp]) + ")"
    else:
        return str(sexp)
