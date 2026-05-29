# test_etcetera.py

from etcabductionpy import etcetera, nbest, KnowledgeBase

test_problem = '''
(if (etc0_rain 0.1 ?loc) (rain ?loc))
(if (etc0_hose 0.01 ?loc) (hose ?loc))
(if (etc0_wet 0.01 ?loc) (wet ?loc))
(if (and (rain ?loc) (etc1_wet 0.9 ?loc)) (wet ?loc))
(if (and (hose ?loc) (etc2_wet 0.8 ?loc)) (wet ?loc))
(wet ?z)
'''

def test_etcetera_single_obs():
    kb, obs = KnowledgeBase.from_src(test_problem)
    obs = kb.standardize_literals(obs)
    solutions = etcetera(obs, kb, 5)
    assert len(solutions) == 3
    # [[(etc0_rain 0.1 $1), (etc1_wet 0.9 $1)], [(etc0_wet 0.01 $1)], [(etc0_hose 0.01 $1), (etc2_wet 0.8 $1)]]

def test_etcetera_sorting():
    kb, obs = KnowledgeBase.from_src(test_problem)
    obs = kb.standardize_literals(obs)
    solutions = etcetera(obs, kb, 5)
    # first solution should be rain -> wet (highest probability)
    assert any(str(l).startswith('(etc0_rain') for l in solutions[0])
    assert any(str(l).startswith('(etc1_wet') for l in solutions[0])

def test_nbest_single_obs():
    kb, obs = KnowledgeBase.from_src(test_problem)
    obs = kb.standardize_literals(obs)
    solutions = nbest(obs, kb, 5, n=2)
    assert len(solutions) == 2

def test_nbest_all():
    kb, obs = KnowledgeBase.from_src(test_problem)
    obs = kb.standardize_literals(obs)
    solutions = nbest(obs, kb, 5, n=10)
    assert len(solutions) == 3  # n=10 but only 3 solutions exist

def test_no_obs():
    kb, obs = KnowledgeBase.from_src("")
    assert len(etcetera(obs, kb, 5)) == 0

def test_unindexed_obs():
    kb, obs = KnowledgeBase.from_src("(unexplained X)")
    assert len(etcetera(obs, kb, 5)) == 0