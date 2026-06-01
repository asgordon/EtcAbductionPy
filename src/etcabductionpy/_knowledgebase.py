'''
knowledgebase.py
Python classes for etcabductionpy
Andrew S. Gordon
'''

__all__ = ['Term', 'Literal', 'EtceteraLiteral', 'DefiniteClause', 'KnowledgeBase']

import math

from . import Sexp
from . import Parser

class Term:
    __slots__ = ('value', 'is_variable')

    def __init__(self, value):
        self.value = value
        self.is_variable = isinstance(value, str) and value and value[0] == '?'
    
    @staticmethod
    def from_sexp(sexp: Sexp) -> 'Term':
        if sexp.type == 'symbol':
            v = sexp.value
            if v and v[0].islower(): # lowercase first character implies variable
                v = '?' + v # so add a ?
            if v.startswith('?') and len(v) == 1:
                raise ValueError(f"Invalid variable: {v!r}")
            return Term(v)
        if sexp.type == 'string':
            return Term(f"\"{sexp.value}\"")
        if sexp.type == 'number':
            return Term(sexp.value)
        raise ValueError(f"Cannot make Term from Sexp of type {sexp.type}")
    
    @staticmethod
    def from_src(src: str) -> 'Term':
        sexp = Parser(src).parse_first()
        return Term.from_sexp(sexp)

    def __repr__(self) -> str:
        return str(self.value)
    
    def __hash__(self) -> int:
        return hash(self.value)
    
    def __eq__(self, other) -> bool:
        return isinstance(other, Term) and self.value == other.value
    
    def __lt__(self, other) -> bool:
        return self.value < other.value
    
    def __gt__(self, other) -> bool:
        return self.value > other.value
    
class Literal:
    __slots__ = ('predicate', 'arguments')

    def __init__(self, predicate: str, arguments: tuple[Term, ...]):
        self.predicate = predicate
        self.arguments = arguments

    @staticmethod
    def from_sexp(sexp: Sexp) -> 'Literal':
        if sexp.type != 'list':
            raise ValueError(f"Cannot make Literal from Sexp of type {sexp.type}")
        predicate = sexp.value[0].value
        arguments = tuple(Term.from_sexp(t) for t in sexp.value[1:])
        # is this an etcetera literal? If so, return the more specific type
        if predicate.startswith('etc') and len(arguments) > 0 and isinstance(arguments[0].value, float):
            return EtceteraLiteral(predicate, arguments)
        return Literal(predicate, arguments)
    
    @staticmethod
    def from_src(src: str) -> 'Literal':
        sexp = Parser(src).parse_first()
        return Literal.from_sexp(sexp)
    
    def subst(self, theta: dict[Term, Term]) -> 'Literal':
        # Q: Should self be returned if no substitutions are made?
        new_args = tuple(theta[t] if t in theta else t for t in self.arguments)
        if isinstance(self, EtceteraLiteral):
            return EtceteraLiteral(self.predicate, new_args)
        return Literal(self.predicate, new_args)

    def all_variables(self) -> 'set[Term]':
        result = set()
        for arg in self.arguments:
            if arg.is_variable:
                result.add(arg)
        return result

    def __repr__(self) -> str:
        if len(self.arguments) > 0:
            return f"({self.predicate} {' '.join(repr(a) for a in self.arguments)})"
        else:
            return f"({self.predicate})"
    
    def __hash__(self) -> int:
        return hash((self.predicate, self.arguments))
    
    def __eq__(self, other) -> bool:
        return isinstance(other, Literal) and self.predicate == other.predicate and self.arguments == other.arguments
    
    def __lt__(self, other) -> bool:
        return str(self) < str(other)
    
    def __gt__(self, other) -> bool:
        return str(self) > str(other)
    
class EtceteraLiteral(Literal):
    __slots__ = ('log_probability',)

    def __init__(self, predicate: str, arguments: tuple[Term, ...]):
        if not predicate.startswith('etc'):
            raise ValueError(f"Not an etcetera predicate: {predicate!r}")
        if not arguments:
            raise ValueError(f"EtceteraLiteral requires at least one argument (a probability)")
        if not isinstance(arguments[0].value, float) or arguments[0].value <= 0:
            raise ValueError(f"First argument must be a positive float (probability), got {arguments[0].value!r}")
        super().__init__(predicate, arguments)
        self.log_probability = math.log(arguments[0].value)

    @property
    def probability(self) -> float:
        return self.arguments[0].value
    
    @staticmethod
    def from_sexp(sexp: Sexp) -> 'EtceteraLiteral':
        literal = Literal.from_sexp(sexp)
        return EtceteraLiteral(literal.predicate, literal.arguments)
    
    @staticmethod
    def from_src(src: str) -> 'EtceteraLiteral':
        sexp = Parser(src).parse_first()
        return  EtceteraLiteral.from_sexp(sexp)
    
class DefiniteClause:
    __slots__ = ('antecedents', 'consequent')

    def __init__(self, antecedents: list[Literal], consequent: Literal):
        self.antecedents = antecedents
        self.consequent = consequent

    @staticmethod
    def from_sexp(sexp: Sexp) -> 'DefiniteClause':
        if sexp.type != 'list' or len(sexp.value) != 3 or sexp.value[0].value != 'if':
            raise ValueError(f"Not a definite clause: {sexp}")
        # antecedent is always a list of literals
        antecedent_sexp = sexp.value[1]
        if antecedent_sexp.value[0].value == 'and':
            antecedents = [Literal.from_sexp(t) for t in antecedent_sexp.value[1:]]
        else:
            antecedents = [Literal.from_sexp(antecedent_sexp)]
        # consequent is always a single literal
        consequent = Literal.from_sexp(sexp.value[2])
        return DefiniteClause(antecedents, consequent)
    
    @staticmethod
    def from_src(src: str) -> 'DefiniteClause':
        sexp = Parser(src).parse_first()
        return DefiniteClause.from_sexp(sexp)
    
    def subst(self, theta: dict[Term, Term]) -> 'DefiniteClause':
        #Q: Should self be returned if no substitutions are made?
        new_ants = [a.subst(theta) for a in self.antecedents]
        new_cons = self.consequent.subst(theta)
        return DefiniteClause(new_ants, new_cons)
    
    def all_variables(self) -> 'set[Term]':
        result = set()
        for ant in self.antecedents:
            result.update(ant.all_variables())
        result.update(self.consequent.all_variables())
        return result

    def __repr__(self) -> str:
        if len(self.antecedents) == 1:
            antecedent_str = repr(self.antecedents[0])
        else:
            antecedent_str = f"(and {' '.join(repr(a) for a in self.antecedents)})"
        return f"(if {antecedent_str} {repr(self.consequent)})"
    
    def __eq__(self, other) -> bool:
        return isinstance(other, DefiniteClause) and self.antecedents == other.antecedents and self.consequent == other.consequent

    def __hash__(self) -> int:
        return hash((tuple(self.antecedents), self.consequent))

def countup(prefix = "_"):
    '''Unique symbol name generator'''
    n = 1
    while True:
        yield prefix + str(n)
        n += 1

class KnowledgeBase:
    __slots__ = ('_countup', '_cpindex')

    def __init__(self, clauses: list['DefiniteClause']):
        self._countup = countup('?#')
        self._cpindex = dict() # dict[str, [DefiniteClause] where str is DefiniteClause.consequent.predicate
        for dc in clauses:
            self.add_definite_clause(dc)

    def standardize_literals(self, literals: list[Literal]) -> 'list[Literal]':
        theta: dict[Term, Term] = dict()
        for lit in literals: 
            for var in lit.all_variables():
                if var not in theta and not var.value.startswith('?#'):
                    theta[var] = Term(next(self._countup)) # standardized variable Term
        return [lit.subst(theta) for lit in literals]

    def add_definite_clause(self, dc: DefiniteClause): 
        # insert into _cpindex
        consequent_predicate = dc.consequent.predicate
        if consequent_predicate in self._cpindex:
            self._cpindex[consequent_predicate].append(dc)
        else:
            self._cpindex[consequent_predicate] = [dc]
    
    @staticmethod
    def from_sexp(sexp: Sexp) -> 'tuple[KnowledgeBase, list[Literal]]':
        if sexp.type != 'list':
            raise ValueError(f"Not a list s-expression: {sexp}")
        literals = []
        clauses = []
        for item in sexp.value:
            if item.type != 'list': # definite clause or literal
                raise ValueError(f"Not a literal or definite clause s-expression: {item}") 
            if item.value[0].value == 'if': # must be a definite clause
                clauses.append(DefiniteClause.from_sexp(item))
            elif item.value[0].value == 'and': # conjunction of literals
                literals.extend(Literal.from_sexp(s) for s in item.value[1:])
            else:
                literals.append(Literal.from_sexp(item))
        kb = KnowledgeBase(clauses)
        return(kb, literals)
    
    def add_sexp(self, sexp: Sexp) -> 'list[Literal]':
        if sexp.type != 'list':
            raise ValueError(f"Not a list s-expression: {sexp}")
        literals = []
        for item in sexp.value:
            if item.type != 'list':
                raise ValueError(f"Not a literal or definite clause s-expression: {item}")
            if item.value[0].value == 'if': # must be a definite clause
                dc = DefiniteClause.from_sexp(item)
                self.add_definite_clause(dc)
            elif item.value[0].value == 'and': # conjunction of literals
                literals.extend(Literal.from_sexp(s) for s in item.value[1:])
            else:
                literals.append(Literal.from_sexp(item))
        return literals

    @staticmethod
    def from_src(src: str) -> 'tuple[KnowledgeBase, list[Literal]]':
        sexp = Parser(src).parse_all()
        return KnowledgeBase.from_sexp(sexp)
    
    def add_src(self, src: str) -> 'list[Literal]':
        sexp = Parser(src).parse_all()
        return self.add_sexp(sexp)
    
    def __len__(self) -> int:
        return sum(len(entries) for entries in self._cpindex.values())
    
    def __iter__(self):
        for entries in self._cpindex.values(): # entries is a list[DefiniteClause]
            for dc in entries: # dc is a Definite Clause
                yield dc



