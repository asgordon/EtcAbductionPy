# forward.py
# An exhaustive forward chaining algorithm with graph file output (.dot)
# Andrew S. Gordon

# todo: namespace variables?

import parse
import unify

def forward(facts, kb):
    '''An exhaustive forward chaining algorithm for first-order definite clauses'''
    # each production is [antecedent_list, consequent_literal, triggers]
    stack = list(facts)
    productions = [[parse.antecedent(k), parse.consequent(k), []] for k in kb]
    entailed = []
    while len(stack) > 0:
        current = stack.pop(0)
        for prod in productions:
            for ant in prod[0]:
                theta = unify.unify(current, ant)
                if theta != None:
                    new_consequent = unify.subst(theta, prod[1])
                    new_triggers = prod[2] + [current]
                    if len(prod[0]) == 1: # last one
                        entailed.append([new_consequent,
                                         new_triggers])
                        stack.append(new_consequent)
                    else:
                        new_antecedent = list(prod[0])
                        new_antecedent.remove(ant)
                        new_antecedent = [unify.subst(theta, x) for x in new_antecedent]
                        productions.append([new_antecedent,
                                            new_consequent,
                                            new_triggers])
    return entailed

def graph(facts, entailed, targets=[]):
    '''.dot format graph representation of proof, highlighting targets if provided'''
    #res = "digraph proof {\n graph [rankdir=\"RL\"]\n"
    res = "digraph proof {\n graph [rankdir=\"TB\"]\n"
    samestr = ""
    # nodes
    nodes = facts + [x[0] for x in entailed]
    for n in xrange(len(nodes)):
        if nodes[n] in facts:
            res += " n" + str(n) + " [label=\"" + nodelabel(nodes[n]) + "\"];\n"
        elif nodes[n] in targets:
            res += " n" + str(n) + " [shape=box peripheries=2 label=\"" + nodelabel(nodes[n]) + "\"];\n"
            samestr += " n" + str(n)
        else:
            res += " n" + str(n) + " [shape=box label=\"" + nodelabel(nodes[n]) + "\"];\n"
    # arcs
    for e in entailed:
        for a in e[1]:
            res += " n" + str(nodes.index(a)) + " -> n" + str(nodes.index(e[0])) + "\n"
    # rank=same
    if len(samestr) > 0:
        res += " {rank=same" + samestr + "}\n"
    res += "}\n"
    return res

def nodelabel(expression):
    '''Turns a s-expression literal into a nice string, with special case for etc'''
    if isinstance(expression, list):
        if True and expression[0][:3] == "etc": # for nicer graphs
            return expression[0] + " " + str(expression[1])
        else:
            return "(" + " ".join(nodelabel(i) for i in expression) + ")"
    else:
        return str(expression)
                                           

                
                
        
    




