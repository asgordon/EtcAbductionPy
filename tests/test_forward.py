# test_forward.py

from etcabductionpy import forward, graph, KnowledgeBase

# forward

test_kb = '''
(if (a ?x) (b ?x))
(a Foo)
'''

def test_forward_simple():
    kb, facts = KnowledgeBase.from_src(test_kb)
    entailed = forward(facts, kb)
    # (a Foo) should trigger (b ?x) producing (b Foo)
    assert len(entailed) == 1
    assert str(entailed[0][0]) == '(b Foo)'
    assert entailed[0][1] == facts # trigger is the original fact list

test_kb2 = '''
  (if (a ?x) (b ?x))
  (if (and (b ?x) (c ?x)) (d ?x))
  (if (d ?x) (e ?x))
  (a Foo)
  (c Foo)
  '''

def test_forward_complex():
    kb, facts = KnowledgeBase.from_src(test_kb2)
    entailed = forward(facts, kb)

    # (a Foo) -> (b Foo)
    # (b Foo) -> (c Foo) -> (d Foo)
    # (d Foo) -> (e Foo)
    assert len(entailed) == 3

    consequents = [str(e[0]) for e in entailed]
    assert '(b Foo)' in consequents
    assert '(d Foo)' in consequents
    assert '(e Foo)' in consequents

# graph

def test_graph_simple():
    kb, facts = KnowledgeBase.from_src(test_kb2)
    entailed = forward(facts, kb)
    # pick an entailed literal as the target (not a fact)
    target_literal = entailed[0][0]  # e.g. (b Foo)
    dot = graph(facts, entailed, targets=[target_literal])
    assert 'digraph proof' in dot
    assert 'shape=box' in dot
    assert 'peripheries=2' in dot
