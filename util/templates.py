# templates.py
# utility for generating template forms for knowledgebase files
# for use in the generation of narrative text

from __future__ import print_function

import argparse
import sys

from context import etcabductionpy
from etcabductionpy import parse

# spit out a template for each one

# run

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

inlines = args.infile.readlines()
intext = "".join(inlines)
kb, obs = parse.parse(intext)

# iterate through axioms to find etc literals in antecednets

outtext = ""
for dc in kb:
    # find etc literal in antecedent
    etcliteral = []
    for literal in parse.antecedent(dc):
        if literal[0][:3] == 'etc':
            # write out new dc template
            outtext += "(if " + parse.display(literal) + "\n" + "    (text \"" + literal[0] + " template\"))\n\n"

print(outtext, file=args.outfile)
sys.exit()