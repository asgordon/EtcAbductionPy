# tricopa.py : Use etcabductionpy to solve tricopa problems
# Andrew S. Gordon
# November 2015

from __future__ import print_function
import argparse
import sys
import re

sys.path.append('../etcabductionpy')
import etcetera
import parse
import forward
import unify

# Question class and parser

class Question(tuple):
    # consider adding natural language text in the future
    def __new__(cls, number, given, alta, altb, answer):
        return tuple.__new__(Question, (number, given, alta, altb, answer))
    def number(self): return self[0]
    def given(self): return self[1]
    def alta(self): return self[2]
    def altb(self): return self[3]
    def answer(self): return self[4]

def listofliterals(sexp_str):
    # returns a list of literals from a given s-expression string
    x = parse.variablize(parse.sexp(sexp_str))
    if (x[0] == 'and'):
        return x[1:]
    else:
        return [x]

def tcparse(question_file, answer_file):
    result = [] # list of Question objects
    qlines = question_file.readlines()
    alines = answer_file.readlines()
    lineno = 0
    for i in xrange(len(qlines)):
        if (re.search("^[0-9]+\. ", qlines[i])): # e.g. "43. "
            qnum = int(qlines[i].split('.')[0])
            answer = alines[qnum - 1].split()[1]
            result.append(Question(qnum, listofliterals(qlines[i+1]), listofliterals(qlines[i+3]), listofliterals(qlines[i+5]), answer))
    return result

# Evaluation functions

def contains(conj, lit): # where conj is the list of entailed, lit is an answer literal.
    for c in conj:
        if unify.unify(lit, c):
            return True
    return False

def percentEntailed(entailed, alt): #percent of alt that is entailed
    count = 0
    for a in alt:
        if contains(entailed, a):
            count +=1
    return(float(count) / float(len(alt)))

def highestPercent(entailedlist, alt): #index of highest percentEntailed
    highest = len(entailedlist)
    percent = 0.0
    for i in xrange(len(entailedlist)):
        iperc = percentEntailed(entailedlist[i], alt)
        if iperc > percent:
            percent = iperc
            highest = i
    return highest, percent

def entailedlist(obs, nbest, kb):
    return [[pair[0] for pair in forward.forward(n, kb)] for n in nbest]

def score1q(q, kb, depth, n):
    nbest = etcetera.nbest(q.given(), kb, depth, n)
    elist = entailedlist(q.given(), nbest, kb)
    altaIndex, altaPercent = highestPercent(elist, q.alta())
    altbIndex, altbPercent = highestPercent(elist, q.altb())
    score = 0
    if q.answer() == 'a':
        if altaPercent > altbPercent:
            score = 1
        elif altaIndex < altbIndex:
            score = 1
        elif altaIndex == altbIndex and altaPercent == altbPercent and altaPercent == 1.0 and len(q.alta()) > len(q.altb()):
            score = 1
    elif q.answer() == 'b':
        if altbPercent > altaPercent:
            score = 1
        elif altbIndex < altaIndex:
            score = 1
        elif altaIndex == altbIndex and altaPercent == altbPercent and altaPercent == 1.0 and len(q.altb()) > len(q.alta()):
            score = 1
    else:
        print("big problem")
    print(q.number(), q.answer(), altaIndex, altaPercent, altbIndex, altbPercent, score)
    return score

def scoreall(qlist, kb, depth, n):
    score = 0
    for q in qlist:
        if q.number() not in [68]:
            score += score1q(q, kb, depth, n)
    return(score)

def workflow(q, kb, depth):
    best = etcetera.nbest(q.given(), kb, depth, 1)[0]
    return(forward.graph(best, forward.forward(best, kb), targets=q.given()))

def xbestproof(q, kb, depth, x):
    xbest = etcetera.nbest(q.given(), kb, depth, x + 1)[x]
    return(forward.graph(xbest, forward.forward(xbest, kb), targets=q.given()))

# command-line control
        
if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-i', '--infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    argparser.add_argument('-t', '--tricopa', nargs='?', type=argparse.FileType('r'), default="TriCOPA.txt")
    argparser.add_argument('-a', '--answers', nargs='?', type=argparse.FileType('r'), default="TriCOPA-answers.txt")
    argparser.add_argument('-k', '--kb', nargs='?', type=argparse.FileType('r'), default="tricopa-kb.lisp")
    argparser.add_argument('-o', '--outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    argparser.add_argument('-q', '--question', type=int)
    argparser.add_argument('-d', '--depth', type=int, default=3)
    argparser.add_argument('-n', '--nbest', type=int, default=10)
    argparser.add_argument('-g', '--graph', action="store_true")
    argparser.add_argument('-x', '--xbestproof', type=int)
    args = argparser.parse_args()
    questionlist = tcparse(args.tricopa, args.answers) # a list
    kb, ignore = parse.definite_clauses(parse.parse("".join(args.kb.readlines())))

    if args.question:
        if args.graph:
            if args.xbestproof:
                print(xbestproof(questionlist[args.question -1], kb, args.depth, args.xbestproof))
            else:
                print(workflow(questionlist[args.question -1], kb, args.depth))
        else:
            print(score1q(questionlist[args.question - 1], kb, args.depth, args.nbest))
    else:
        print(scoreall(questionlist, kb, args.depth, args.nbest))
    
                            




            
        
        



    
    
