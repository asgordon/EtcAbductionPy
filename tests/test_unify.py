# test_unify.py

from etcabductionpy import unify, skolemize, Literal, Term, EtceteraLiteral

def test_predicate_mismatch():
    x = Literal.from_src("(p A B C)")
    y = Literal.from_src("(q A B C)")
    assert unify(x, y) == None

def test_length_mismatch():
    x = Literal.from_src("(p A B C)")
    y = Literal.from_src("(p A B C D)")
    assert unify(x, y) == None

def test_eq():
    x = Literal.from_src("(p A B C)")
    y = Literal.from_src("(p A B C)")
    assert unify(x, y) == {}

def test_simple_unify():
    x = Literal.from_src("(p ?a B C)")
    y = Literal.from_src("(p A B C)")
    assert unify(x, y) == {Term('?a'): Term('A')}

def test_complex_unify():
    x = Literal.from_src("(p ?a ?b ?c)")
    y = Literal.from_src("(p ?b ?c C)")
    assert unify(x, y) == {Term('?a'): Term('C'), Term('?b'): Term('C'), Term('?c'): Term('C')}

def test_circular_theta():
    x = Literal.from_src("(p ?a ?b ?c)")
    y = Literal.from_src("(p ?b ?c ?a)")
    assert unify(x, y) == {Term('?b'): Term('?a'), Term('?c'): Term('?a')}

def test_reverse_complex_unify():
    x = Literal.from_src("(p ?c ?b ?a)")
    y = Literal.from_src("(p C ?c ?b)")
    assert unify(x, y) == {Term('?a'): Term('C'), Term('?b'): Term('C'), Term('?c'): Term('C')}
    
def test_reverse_circular_theta():
    x = Literal.from_src("(p ?c ?b ?a)")
    y = Literal.from_src("(p ?a ?c ?b)")
    assert unify(x, y) == {Term('?c'): Term('?a'), Term('?b'): Term('?a')}

def test_standardized_unify():
    x = Literal.from_src("(p ?#1 B C)")
    y = Literal.from_src("(p A B C)")
    assert unify(x, y) == {Term('?#1'): Term('A')}

def test_complex_standardized_unify():
    x = Literal.from_src("(p ?#1 ?#2 ?#3)")
    y = Literal.from_src("(p ?#2 ?#3 C)")
    assert unify(x, y) == {Term('?#1'): Term('C'), Term('?#2'): Term('C'), Term('?#3'): Term('C')}

def test_standardized_circular_theta():
    x = Literal.from_src("(p ?#1 ?#2 ?#3)")
    y = Literal.from_src("(p ?#2 ?#3 ?#1)")
    assert unify(x, y) == {Term('?#2'): Term("?#1"), Term('?#3'): Term('?#1')}


# skolemization

def test_skolemize_no_variables():
      solution = [Literal.from_src("(p A B)"), Literal.from_src("(q C D)")]
      result = skolemize(solution)
      assert result == solution  # no change, no variables

def test_skolemize_single_variable():
    solution = [Literal.from_src("(p ?x A)")]
    result = skolemize(solution)
    assert len(result) == 1
    assert result[0].arguments[0] == Term('$1')

def test_skolemize_shared_variable():
    solution = [Literal.from_src("(p ?x A)"), Literal.from_src("(q ?x B)")]
    result = skolemize(solution)
    assert len(result) == 2
    assert result[0].arguments[0] == Term('$1')
    assert result[1].arguments[0] == Term('$1')

def test_skolemize_different_variable():
    solution = [Literal.from_src("(p ?x A)"), Literal.from_src("(q ?y B)")]
    result = skolemize(solution)
    assert len(result) == 2
    assert result[0].arguments[0] == Term('$1')
    assert result[1].arguments[0] == Term('$2')

def test_skolemize_etcetera_literal():
    solution = [EtceteraLiteral.from_src("(etc0 0.5 ?x C)")]
    result = skolemize(solution)
    assert len(result) == 1
    assert isinstance(result[0], EtceteraLiteral)  # type preserved
    assert result[0].probability == 0.5  # probability remains

def test_skolemize_empty_solution():
    result = skolemize([])
    assert result == []

def test_skolemize_preserves_non_variables():
    solution = [Literal.from_src("(p 1.0 \"quoted\")")]
    result = skolemize(solution)
    assert result[0] == solution[0]  # numbers and strings remain