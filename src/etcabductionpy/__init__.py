'''
etcabductionpy package
Referece implementation of Etcetera Abduction in Python.
Andrew S. Gordon
'''

__author__ = 'Andrew S. Gordon'
__version__ = "0.5.0"

from ._sexp import Sexp, Parser
from ._knowledgebase import Term, Literal, EtceteraLiteral, DefiniteClause, KnowledgeBase
from ._unify import unify, skolemize
from ._abduction import abduction
from ._etcetera import etcetera, nbest, joint_log_probability
from ._forward import forward, graph
from ._incremental import incremental

__all__ = [
    'Sexp', 'Parser',
    'Term', 'Literal', 'EtceteraLiteral', 'DefiniteClause', 'KnowledgeBase',
    'unify', 'skolemize',
    'abduction',
    'etcetera', 'nbest', 'joint_log_probability',
    'forward', 'graph',
    'incremental'
]