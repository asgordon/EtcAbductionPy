'''etcabductionpy.__main__
Command line interface
Andrew S. Gordon
'''

import argparse
import sys

from . import (
    parse, display, etcetera, nbest, forward, graph, incremental, standardize
)

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

argparser.add_argument('-c', '--incremental',
                       action='store_true',
                       help='Use incremental abduction')

argparser.add_argument('-v', '--variables',
                       action='store_true',
                       help='Leave variables in solutions rather than Skolem constants')

argparser.add_argument('-w', '--window',
                       type=int,
                       default=4,
                       help='Incremental abduction window-size, defaults to 4')

argparser.add_argument('-b', '--beam',
                       type=int,
                       default=10,
                       help='Incremental abduction beam-size, defaults to 10')
                    
args = argparser.parse_args()


# Load files

inlines = args.infile.readlines()
intext = "".join(inlines)
kb, obs = parse(intext)
obs = standardize(obs)

_skolemize = not args.variables

if args.kb:
    kblines = args.kb.readlines()
    kbtext = "".join(kblines)
    kbkb, kbobs = parse(kbtext)
    kb.extend(kbkb)

# Handle forward

if args.forward:
    entailed = forward(obs, kb)
    if args.graph:
        print(graph(obs, entailed), file=args.outfile)
    else:
        for e in entailed:
            print(display(e[0]), file=args.outfile)
    sys.exit()

# Handle abduction

if args.all:
    solutions = etcetera(obs, kb, args.depth, skolemize = _skolemize)
else:
    if args.incremental:
        solutions = incremental(obs, kb, args.depth, args.nbest,
                                            args.window, args.beam, skolemize = _skolemize)
    else:
        solutions = nbest(obs, kb, args.depth, args.nbest, skolemize = _skolemize)

if args.graph:
    solution = solutions[args.solution - 1]
    print(graph(solution, forward(solution, kb), targets=obs),
          file=args.outfile)
else:
    for solution in solutions:
        print(display(solution), file=args.outfile)
    print(str(len(solutions)) + " solutions.")



