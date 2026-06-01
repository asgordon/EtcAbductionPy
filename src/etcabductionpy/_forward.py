'''
forward.py
forward chaining in first-order logic and proof graphs
Andrew S. Gordon
'''

__all__ = ['forward', 'graph']

from . import KnowledgeBase, EtceteraLiteral, Literal, unify

def forward(facts: list[Literal], kb: KnowledgeBase) -> list[tuple[Literal,list[Literal]]]:
    # an exhaustive forward-chaining. Returns list of (entailed_literal, triggers) tuples
    entailed: list[tuple[Literal, list[Literal]]] = []
    # queue of facts to try against all rules (makes a copy)
    queue = list(facts)
    # each production: (remaining_antecedents, consequent, triggers_so_far)
    productions: list[tuple[list[Literal], Literal, list[Literal]]] = []
    for dc in kb: # uses __iter__
        productions.append((list(dc.antecedents), dc.consequent, []))
    while queue:
        fact = queue.pop(0)
        i = 0
        while i < len(productions):
            ants, cons, triggers = productions[i]
            if ants:
                for j, target in enumerate(ants):
                    theta = unify(fact, target)          
                    if theta is not None:
                        new_triggers = triggers + [fact]
                        if len(ants) == 1:
                            # all antecedents satisfied: fire the rule
                            result = cons.subst(theta)
                            entailed.append((result, new_triggers))
                            queue.append(result)
                        else:
                            # partial match, keep going
                            remaining = [a.subst(theta) for k, a in enumerate(ants) if k != j]
                            cons_so_far = cons.subst(theta)
                            productions.append((remaining, cons_so_far, new_triggers))
            i += 1
    return entailed


def graph(facts: list[Literal], entailed: list[tuple[Literal, list[Literal]]], targets: list[Literal] | None = None) -> str:
    # .dot format graph representation of proof, highlighting targets if provided
    targets = targets or []
    res = 'digraph proof {\n graph [rankdir="TB"]\n'
    samestr = ""
    nodes = list(facts) + [e[0] for e in entailed]
    for i, node in enumerate(nodes):
        label = node_label(node)
        if node in facts:
            res += f' n{i} [label="{label}"]\n'
        elif node in targets:
            res += f' n{i} [shape=box peripheries=2 label="{label}"];\n'
            samestr += f' n{i}'
        else:
            res += f' n{i} [shape=box label="{label}"];\n'
    for ent_consequent, ent_triggers in entailed:
        for trigger in ent_triggers:
            src = nodes.index(trigger)
            dst = nodes.index(ent_consequent)
            res += f' n{src} -> n{dst}\n'
    if samestr:
        res += f' {{rank=same{samestr}}}\n'
    res += '}\n'
    return res

def node_label(literal: Literal) -> str:
    # creates a nice string for a literal, with a special case for etc literals
    if isinstance(literal, EtceteraLiteral):
        return f'{literal.predicate} {literal.probability}'
    else:
        return str(literal)[1:-1] # str representation removing parentheses
    
