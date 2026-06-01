'''
parsecheck.py
utility for ensuring that knowledge base axioms are well formulated
Andrew S. Gordon
'''

import datetime
import argparse
import sys

from etcabductionpy import KnowledgeBase, DefiniteClause, Literal, EtceteraLiteral, Term

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

def all_literals(dc: DefiniteClause) -> list[Literal]:
    '''All literals in a definite clause (antecedents + consequent)'''
    return list(dc.antecedents) + [dc.consequent]

def parsecheck(obs: list[Literal], kb: KnowledgeBase) -> str:
    '''Utility for ensuring that knowledge base axioms are well formulated'''
    res = "parsecheck.py report at " + str(datetime.datetime.now()) + "\n\n"
    res += str(len(obs)) + " observations, " + str(len(kb)) + " knowledge base axioms\n\n"
    res += "arity warnings: " + arity_warnings(obs, kb) + "\n\n"
    res += "existential warnings: " + str(existential_warnings(kb)) + "\n\n"
    res += "etcetera warnings: " + str(etcetera_warnings(kb))  + "\n\n"
    res += "missing axiom warnings: " + str(missing_axiom_warnings(kb)) + "\n"
    return res

def arity_warnings(obs: list[Literal], kb: KnowledgeBase):
    '''Checks that predicates and functions have consistent arity throughout observations and knowledge base'''
    arity: dict[str, int] = {}
    warnings: list[str] = []

    def check(lit: Literal) -> None:
        pred = lit.predicate
        a = len(lit.arguments)
        if pred in arity:
            if arity[pred] != a:
                warnings.append(f"  inconsistent arity for predicate: {pred}")
            else:
                arity[pred] = a
    
    for lit in obs:
        check(lit)
    for dc in kb:
        for lit in all_literals(dc):
            check(lit)
    return "\n".join(warnings) if warnings else "none"

def existential_warnings(kb: KnowledgeBase) -> str:
    '''Definite clauses where there are existential variables in the consequent (not found in antecedent)'''
    warnings: list[str] = []
    for dc in kb:
        antecedent_vars = set()
        for ant in dc.antecedents:
            antecedent_vars.update(ant.all_variables())
        consequent_vars = dc.consequent.all_variables()
        for v in consequent_vars:
            if v not in antecedent_vars:
                warnings.append(f"  existential variables in the consequent: {repr(dc)}")
                break
    return "\n".join(warnings) if warnings else "none"

def etcetera_warnings(kb: KnowledgeBase) -> str:
    '''Definite clauses with malformed etcetera literals'''
    warnings: list[str] = []
    seen_etcs: list[str] = []

    for dc in kb:
        etcs = [l for l in all_literals(dc) if isinstance(l, EtceteraLiteral)]
        if len(etcs) < 1:
            warnings.append(f"  definite clause without etcetera literal: {repr(dc)}")
        elif len(etcs) > 1:
            warnings.append(f"  definite clause with multiple etcetera literals: {repr(dc)}")
        else:
            etc = etcs[0]
            if etc.predicate in seen_etcs:
                warnings.append(f"  etcetera literal previously seen elsewhere: {repr(dc)}")
            elif len(etc.arguments) < 1:
                warnings.append(f"  too few arguments in etcetera literal: {repr(dc)}")
            elif etc.probability > 1.0 or etc.probability < 0.0:
                warnings.append(f"  probability of etcetera literal out of range: {repr(dc)}")
            else:
                etc_vars = etc.all_variables()
                dc_vars = dc.all_variables()
                non_etc_vars = set()
                for l in all_literals(dc):
                    if not isinstance(l, EtceteraLiteral):
                        non_etc_vars.update(l.all_variables())
                if len(etc_vars) != len(dc_vars):
                    warnings.append(f"  etcetera literal missing variables found elsewhere in definite clause: {repr(dc)}")
                elif len(non_etc_vars) < len(etc_vars):
                    warnings.append(f"  etcetera literal includes variables not found elsewhere in definite clause: {repr(dc)}")
                else:
                    seen_etcs.append(etc.predicate)
    return "\n".join(warnings) if warnings else "none"


def missing_axiom_warnings(kb: KnowledgeBase) -> str:
    '''Predicates that appear in antecedents but not in any consequent'''
    antecedent_predicates: set[str] = set()
    consequent_predicates: set[str] = set()

    for dc in kb:
        consequent_predicates.add(dc.consequent.predicate)
        for lit in dc.antecedents:
            if not isinstance(lit, EtceteraLiteral):
                antecedent_predicates.add(lit.predicate)
    
    # predicate used in antecedent but never definite in any consequent
    undefined = antecedent_predicates - consequent_predicates
    warnings: list[str] = []
    for predicate in sorted(undefined):
        warnings.append(f"  no etcetera axiom for literal: {predicate}")
    
    return "\n".join(warnings) if warnings else "none"
    

def is_text_literal(lit: Literal) -> bool:
    return lit.predicate == 'text'

def is_text_definite_clause(dc: DefiniteClause) -> bool:
    return is_text_literal(dc.consequent)
        
# --- main ---

args = argparser.parse_args()

intext = args.infile.read()
kb, obs = KnowledgeBase.from_src(intext)
obs = kb.standardize_literals(obs)

if args.text:
    obs = [o for o in obs if not is_text_definite_clause(o)]
    # rebuild kb without text axioms
    new_clauses = [dc for dc in kb if not is_text_definite_clause(dc)]
    kb = KnowledgeBase(new_clauses)

report = parsecheck(obs, kb)
print(report, file=args.outfile)

