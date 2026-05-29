import pytest

from etcabductionpy import Term, Literal, EtceteraLiteral, DefiniteClause, KnowledgeBase

# term

def test_term_variables():
    assert Term.from_src(" ?one ").is_variable
    assert Term.from_src(" yup ").is_variable # lowercase first letter implies variable
    assert not Term.from_src(" Nope ").is_variable
    assert not Term.from_src("1.0").is_variable

def test_term_values():
    assert Term.from_src("10.202020").value == 10.202020
    assert Term.from_src('"one"').value == '"one"'

def test_term_repr():
    assert str(Term.from_src(" ?one ")) == "?one"
    assert str(Term.from_src("?one")) == repr(Term.from_src("?one"))
    assert Term.from_src("?one") == Term.from_src(str(Term.from_src("?one")))

def test_term_construction():
    with pytest.raises(ValueError):
        Term.from_src("?")

def test_term_equality():
    assert Term.from_src("this") == Term.from_src(" this ")
    assert Term.from_src("?x") == Term.from_src("x") # auto-add ?
    assert Term.from_src("?x") == Term.from_src("?x")
    assert Term.from_src("1.0").value == 1.0

def test_term_hashes():
    assert hash(Term.from_src("this")) == hash(Term.from_src(" this "))

# literal

def test_literal_construction():
    assert Literal.from_src("(one two three)").predicate == "one"
    lit = Literal.from_src("(foo)")
    assert lit.predicate == 'foo'
    assert lit.arguments == ()

def test_literal_repr():
    assert str(Literal.from_src("(pred arg1 arg2)")) == "(pred ?arg1 ?arg2)"
    assert repr(Literal.from_src("(foo)")) == "(foo)"

def test_literal_hashing():
    assert hash(Literal.from_src("(one two three)")) == hash(Literal.from_src("(one two three)"))

def test_literal_equality():
    assert Literal.from_src("(p a b)") == Literal.from_src("(p a b)")
    assert Literal.from_src("(p a b)") != Literal.from_src("(p a c)")
    assert Literal.from_src("(p a b)") != Literal.from_src("(q a b)")

def test_literal_subst():
    lit1 = Literal.from_src("(p ?a ?b)")
    theta = {Term("?a"): Term("FOO"), Term("?b"): Term("BAR")}
    lit2 = lit1.subst(theta)
    assert lit1 != lit2
    assert str(lit2) == "(p FOO BAR)"

def test_literal_all_variables():
    lit = Literal.from_src("(p One Two ?three Four ?five)")
    vars = lit.all_variables()
    assert len(vars) == 2
    assert Term("?three") in vars
    assert Term("?five") in vars

# etcetera literal

def test_etcetera_log_probabilities():
    assert EtceteraLiteral.from_src("(etc0_a 0.1 b)").log_probability == EtceteraLiteral.from_src("(etc0_b 0.1 c)").log_probability

def test_etcetera_equality():
    assert EtceteraLiteral.from_src("(etc0_a 0.1 b)") == EtceteraLiteral.from_src("(etc0_a 0.1 b)")

def test_etcetera_hashing():
    assert hash(EtceteraLiteral.from_src("(etc0_a 0.1 b)")) == hash(EtceteraLiteral.from_src("(etc0_a 0.1 b)"))

def test_etcetera_construction():
    with pytest.raises(ValueError):
          EtceteraLiteral.from_src("(not_etc 0.5 x)")
    with pytest.raises(ValueError):
          EtceteraLiteral.from_src("(etc0_a 0.0 x)")
    with pytest.raises(ValueError):
          EtceteraLiteral.from_src("(etc0_a -0.1 x)")
    assert isinstance(Literal.from_src("(etc0_a 0.5 x)"), EtceteraLiteral)

def test_etcetera_subst():
    elit1 = EtceteraLiteral.from_src("(etc0 0.5 ?a ?b C)")
    theta = {Term("?a"): Term("FOO"), Term("?b"): Term("BAR")}
    elit2 = elit1.subst(theta)
    assert isinstance(elit2, EtceteraLiteral)
    assert str(elit2) == "(etc0 0.5 FOO BAR C)"

# definite clause

def test_dc_single_antecedent():
    dc = DefiniteClause.from_src("(if (a ?x) (b ?x))")
    assert len(dc.antecedents) == 1
    assert dc.antecedents[0].predicate == "a"
    assert dc.consequent.predicate == "b"

def test_dc_multiple_antecedents():
    dc = DefiniteClause.from_src("(if (and (a ?x) (b ?x)) (c ?x))")
    assert len(dc.antecedents) == 2
    assert dc.antecedents[0].predicate == "a"
    assert dc.antecedents[1].predicate == "b"
    assert dc.consequent.predicate == "c"

def test_dc_etcetera_in_antecedent():
    dc = DefiniteClause.from_src("(if (and (etc0_a 0.1 ?x) (b ?x)) (c ?x))")
    etc = dc.antecedents[0]
    assert isinstance(etc, EtceteraLiteral)
    assert etc.probability == 0.1

def test_dc_repr_single():
    dc = DefiniteClause.from_src("(if (a ?x) (b ?x))")
    assert repr(dc) == "(if (a ?x) (b ?x))"

def test_dc_repr_multiple():
    dc = DefiniteClause.from_src("(if (and (a ?x) (b ?x)) (c ?x))")
    assert repr(dc) == "(if (and (a ?x) (b ?x)) (c ?x))"

def test_dc_repr_roundtrip():
    src = "(if (and (etc0_a 0.5 ?x) (b ?x)) (c ?x))"
    dc = DefiniteClause.from_src(src)
    assert repr(dc) == src

def test_dc_invalid():
    with pytest.raises(ValueError):
        DefiniteClause.from_src("(a b c)")
    with pytest.raises(ValueError):
        DefiniteClause.from_src("(if (a))")

def test_dc_all_variables():
    dc = DefiniteClause.from_src("(if (and (a ?x) (b ?y)) (c ?z))")
    vars = dc.all_variables()
    assert len(vars) == 3
    assert Term("?x") in vars
    assert Term("?y") in vars
    assert Term("?z") in vars

def test_dc_subst():
    dc1 = DefiniteClause.from_src("(if (and (a ?x) (b ?y)) (c ?z))")
    theta = { Term("?x"): Term("X"), Term("?y"): Term("Y"), Term("?z"): Term("Z")}
    dc2 = dc1.subst(theta)
    assert str(dc2) == "(if (and (a X) (b Y)) (c Z))"

def test_dc_eq_hash():
    dc1 = DefiniteClause.from_src("(if (and (a ?x) (b ?y)) (c ?z))")
    theta = { Term("?x"): Term("X"), Term("?y"): Term("Y"), Term("?z"): Term("Z")}
    dc2 = dc1.subst(theta)
    assert dc2 == DefiniteClause.from_src("(if (and (a X) (b Y)) (c Z))")
    assert hash(dc2) == hash(DefiniteClause.from_src("(if (and (a X) (b Y)) (c Z))"))

# knowledge base

test_kb_src = '''

;; Test KB source

;; rain 

;; prior of rain
(if (etc0_rain 0.1 ?loc)
    (rain ?loc))

;; hose

;; prior of hose
(if (etc0_hose 0.01 ?loc)
    (hose ?loc))    

;; wet 

;; prior of wet
(if (etc0_wet 0.01 ?loc)
    (wet ?loc))

;; wet1: maybe rain
(if (and (rain ?loc)
         (etc1_wet 0.9 ?loc))
    (wet ?loc))

;;  wet2: maybe garden hose
(if (and (hose ?loc)
         (etc2_wet 0.8 ?loc))
    (wet ?loc))

;; observable 1
(wet ?z)


'''

def test_kb_construction():
    kb, obs = KnowledgeBase.from_src(test_kb_src)
    assert len(obs) == 1
    assert "rain" in kb._cpindex
    assert "wet" in kb._cpindex
    assert "hose" in kb._cpindex
    assert len(kb._cpindex) == 3
    assert len(kb) == 5

def test_obs_standardization():
    kb, obs = KnowledgeBase.from_src(test_kb_src)
    standardized = kb.standardize_literals(obs)
    assert len(standardized) == 1
    assert str(standardized[0]) == "(wet ?#1)"

def test_kb_add_src():
    kb, obs = KnowledgeBase.from_src(test_kb_src)
    more_obs = kb.add_src("(if (etc0_explosion 0.001 ?loc) (explosion ?loc))")
    assert len(more_obs) == 0
    assert "explosion" in kb._cpindex

def test_kb_empty():
    kb, obs = KnowledgeBase.from_src("")
    assert len(obs) == 0
    assert len(kb._cpindex) == 0
    assert len(kb) == 0

def test_literal_only():
    kb, obs = KnowledgeBase.from_src("(p ?a ?b)")
    assert len(obs) == 1
    assert str(obs[0]) == "(p ?a ?b)"

def test_kb_iter():
    kb, _ = KnowledgeBase.from_src(test_kb_src)
    dcs = list(kb)
    assert len(dcs) == 5
    for dc in dcs:
        assert isinstance(dc, DefiniteClause)