'''
templates.py
utility for generating template forms for knowledgebase files 
for use in the generation of narrative text
Andrew S. Gordon
'''

import argparse
import sys


from etcabductionpy import KnowledgeBase, EtceteraLiteral

argparser = argparse.ArgumentParser(description='Utility for generating text generation templates from a knowledgebase')

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

args = argparser.parse_args()

# read a knowledgebase

intext = args.infile.read()
kb, _ = KnowledgeBase.from_src(intext)

# iterate through axioms to find etc literals in antecednets

outtext = ""

for dc in kb:
    for literal in dc.antecedents:
        if isinstance(literal, EtceteraLiteral):
            # write out new dc template
            outtext += f"(if {repr(literal)}\n"
            outtext += f'    (text "{literal.predicate} template"))\n\n'

print(outtext, file=args.outfile)
