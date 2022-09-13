# parsecheck.py
# utility for ensuring that knowledge base axioms are well formulated

from __future__ import print_function

import datetime
import argparse
import sys

from context import etcabductionpy
from etcabductionpy import _parse, _unify

argparser = argparse.ArgumentParser(description='Utility for ensuring well-formulated knowledge base axioms')

argparser.add_argument('-i', '--infile',
                       nargs='?',
                       type=argparse.FileType('r'),
                       default=sys.stdin,
                       help='Input file to be checked, defaults to STDIN')

argparser.add_argument('-o', '--outfile',
                       nargs='?',
                       type=argparse.FileType('w'),
                       default=sys.stdout,
                       help='Output file, defaults to STDOUT')

argparser.add_argument('-t', '--text',
                       action='store_true',
                       help='treat text literals differently')



def parsecheck(obs, kb):
    '''Utility for ensuring that knowledge base axioms are well formulated'''
    res = "parsecheck.py report at " + str(datetime.datetime.now()) + "\n\n"
    res += str(len(obs)) + " observations, " + str(len(kb)) + " knowledge base axioms\n\n"
    res += "arity warnings: " + arity_warnings(obs, kb) + "\n\n"
    res += "existential warnings: " + str(existential_warnings(kb)) + "\n\n"
    res += "etcetera warnings: " + str(etcetera_warnings(kb))  + "\n\n"
    res += "missing axiom warnings: " + str(missing_axiom_warnings(kb)) + "\n"

    return res

def arity_warnings(obs, kb):
    '''Checks that predicates and functions have consistent arity throughout observations and knowledge base'''
    warnings = ""
    arity = {}
    ls = []
    for dc in kb:
        ls.extend(_parse.literals(dc))
    ls.extend(obs)
    all = []
    for l in ls:
        all.append(l)
        all.extend(_parse.functions(l))
    for i in all:
        if i[0] in arity:
            if arity[i[0]] != len(i):
                warnings += "\n  inconsistent arity for predicate: " + str(i[0])
        else:
            arity[i[0]] = len(i)
    if len(warnings) == 0:
        return "none"
    else:
        return warnings

def existential_warnings(definite_clauses):
    '''Definite clauses where there are existential variables in the consequent (not found in antecedent)'''
    warnings = ""
    for dc in definite_clauses:
        va = _parse.all_variables(_parse.antecedent(dc))
        vc = _parse.all_variables(_parse.consequent(dc))
        for v in vc:
            if v not in va:
                warnings += "\n  existential variables in the consequent: " + _parse.display(dc)
                break;
    if len(warnings) == 0:
        return "none"
    else:
        return warnings


    

def etcetera_warnings(definite_clauses):
    '''Definite clauses with malformed etcetera literals'''
    warnings = ""
    seen_etcs = []
    for dc in definite_clauses:
        etcs = [l for l in _parse.literals(dc) if l[0][0:3] == 'etc']
        if len(etcs) < 1:
            warnings += "\n  definite clause without etcetera literal: " + _parse.display(dc)
        elif len(etcs) > 1:
            warnings += "\n  definite clause with multiple etcetera literals: " + _parse.display(dc)
        elif etcs[0][0] in seen_etcs:
            warnings += "\n  etcetera literal previous seen elsewhere: " + _parse.display(dc)
        elif len(etcs[0]) < 2:
            warnings += "\n  too few arguments in etcetera literal: " + _parse.display(dc)
        elif not isinstance(etcs[0][1], float):
            warnings += "\n  first argument of etcetera literal is not a floating-point number: " + _parse.display(dc)
        elif etcs[0][1] > 1.0 or etcs[0][1] < 0.0:
            warnings += "\n  probability of etcetera literal is out of range: " + _parse.display(dc)
        elif len(_parse.all_variables(etcs[0])) != len(_parse.all_variables(dc)):
            warnings += "\n  etcetera literal missing variables founds elsewhere in definite clause: " + _parse.display(dc)
        elif len(_parse.all_variables([l for l in _parse.literals(dc) if l != etcs[0]])) < len(_parse.all_variables(etcs[0])):
            warnings += "\n  etcetera literal includes variables not found elsewhere in definite clause: " + _parse.display(dc)
        else:
            seen_etcs.append(etcs[0][0])
    if len(warnings) == 0:
        return "none"
    else:
        return warnings


def missing_axiom_warnings(definite_clauses):
    '''Predicates that appear in antecedents but not in any consequent'''
    warnings = ""
    seen_antecedent_predicates = set()
    seen_consequent_predicates = set()
    for dc in definite_clauses:
        seen_consequent_predicates.add(_parse.consequent(dc)[0])
        for literal in _parse.antecedent(dc):
            if literal[0][0:3] != 'etc':
                seen_antecedent_predicates.add(literal[0])
    for predicate in seen_consequent_predicates:
        if predicate in seen_antecedent_predicates:
            seen_antecedent_predicates.remove(predicate)
    for predicate in seen_antecedent_predicates:
        warnings +="\n  no etcetera axiom for literal: " + predicate
    if len(warnings) == 0:
        return "none"
    else:
        return warnings
    

def is_text_literal(literal):
    if literal[0] == 'text':
        return True
    else:
        return False

def is_text_definite_clause(definite_clause):
    if is_text_literal(definite_clause[2]):
        return True
    else:
        return False
        
# run

args = argparser.parse_args()

inlines = args.infile.readlines()
intext = "".join(inlines)
kb, obs = _parse.parse(intext)
obs = _unify.standardize(obs)

if args.text: # text flag is set, so ignore text literals and axioms
    obs = [o for o in obs if not is_text_literal(o)]
    kb  = [a for a in kb if not is_text_definite_clause(a)]

report = parsecheck(obs, kb)
print(report, file=args.outfile)
sys.exit()
