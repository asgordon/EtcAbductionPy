# test_sexp.py

from etcabductionpy import Parser
import pytest

def test_parse_symbol():
    assert str(Parser("foo").parse_first()) == 'foo'
    assert str(Parser(" one ").parse_first()) == "one"
    assert str(Parser("  :symbol seven").parse_first()) == ":symbol"

def test_parse_number():
    assert str(Parser("0002002039932.939292").parse_first()) == "2002039932.939292" 

def test_parse_list():
    assert str(Parser("( predicate arg1   \n :keyword1 \"string\" \t -0.9399)").parse_first()) == "(predicate arg1 :keyword1 \"string\" -0.9399)"
    assert Parser("(one two three :four -5.01 \"six and some more\")").parse_first().to_list()[4] == -5.01

def test_parse_nested_list():
    assert str(Parser("(if(and(one)(two))(three))").parse_first()) == "(if (and (one) (two)) (three))"

def test_parse_sexps():
    assert str(Parser("one\n two\n :three\n -04.0").parse_sexps()[3]) == "-4.0"

def test_parse_all():
    p = Parser("one\ntwo\nthree\nfour")
    p.parse_all()
    assert p.lineno() == 4, f"Expected line 4 after parsing all lines, got {p.lineno()}"

def test_unmatched_paren():
    with pytest.raises(ValueError):
        Parser("())").parse_all()