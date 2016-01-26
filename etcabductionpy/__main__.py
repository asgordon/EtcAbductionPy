# etcabductionpy.__main__
# Etcetera Abduction in Python
# Andrew S. Gordon
# Spring 2016

from __future__ import print_function
import argparse
import sys

import parse
import etcetera
import forward

argparser = argparse.ArgumentParser(description='Etcetera Abduction in Python')

argparser.add_argument('-i', '--infile',
                       nargs='?',
                       type=argparse.FileType('r'),
                       default=sys.stdin,
                       help='Input file of observed literals as lisp s-expressions, defaults to STDIN')

argparser.add_argument('-o', '--outfile',
                       nargs='?',
                       type=argparse.FileType('w'),
                       default=sys.stdout,
                       help='Output file, defaults to STDOUT')

argparser.add_argument('-k', '--kb',
                       nargs='?',
                       type=argparse.FileType('r'),
                       help='Knowledge base of definite clauses as lisp s-expressions')

argparser.add_argument('-n', '--nbest',
                       type=int,
                       default=10,
                       help='Generate NBEST-best proofs, defaults to 10')

argparser.add_argument('-g', '--graph',
                       action='store_true',
                       help='Output graph of solution in .dot format')

argparser.add_argument('-s', '--solution',
                       type=int,
                       default=1,
                       help='Graph the SOLUTION-best solution, defaults to 1')

argparser.add_argument('-d', '--depth',
                       type=int,
                       default=5,
                       help='Backchain to depth DEPTH, defaults to 5')

argparser.add_argument('-a', '--all',
                       action='store_true',
                       help='Generate all solutions')

argparser.add_argument('-f', '--forward',
                       action='store_true',
                       help='Forward chain from INFILE with KB')

args = argparser.parse_args()


# Load files

inlines = args.infile.readlines()
intext = "".join(inlines)
kb, obs = parse.definite_clauses(parse.parse(intext))

if args.kb:
    kblines = args.kb.readlines()
    kbtext = "".join(kblines)
    kbkb, kbobs = parse.definite_clauses(parse.parse(kbtext))
    kb.extend(kbkb)

# Handle forward

if args.forward:
    entailed = forward.forward(obs, kb)
    if args.graph:
        print(forward.graph(obs, entailed), file=args.outfile)
    else:
        for e in entailed:
            print(parse.display(e[0]), file=args.outfile)
    sys.exit()

# Handle abduction

if args.all:
    solutions = etcetera.etcAbduction(obs, kb, args.depth)
else:
    solutions = etcetera.nbest(obs, kb, args.depth, args.nbest)

if args.graph:
    solution = solutions[args.solution - 1]
    print(forward.graph(solution, forward.forward(solution, kb), targets=obs),
          file=args.outfile)
else:
    for solution in solutions:
        print(parse.display(solution), file=args.outfile)
    print(str(len(solutions)) + " solutions.")


# To do: enable skolemize as an option
