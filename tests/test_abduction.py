# test_abduction.py

from etcabductionpy import abduction, KnowledgeBase

test_problem = '''

;; wet1: maybe rain
(if (rain ?loc)
    (wet ?loc))

;;  wet2: maybe garden hose
(if (hose ?loc)
    (wet ?loc))

;; observable 1
(wet ?z)

'''

def test_single_obs():
    kb, obs = KnowledgeBase.from_src(test_problem)
    solutions = abduction(obs, kb, 5)
    assert len(solutions) == 2
    print(solutions) # [[(rain $1)], [(hose $1)]]

def test_no_kb_no_ob():
    kb, obs = KnowledgeBase.from_src("")
    solutions = abduction(obs, kb, 5)
    assert len(solutions) == 0

def test_no_kb_1_ob():
    kb, obs = KnowledgeBase.from_src("(unexplained X)")
    solutions = abduction(obs, kb, 5)
    assert len(solutions) == 0 

def test_2_different_obs():
    kb, _ = KnowledgeBase.from_src(test_problem)
    obs = kb.add_src("(wet Here) (wet There)")
    solutions = abduction(obs, kb, 5)
    assert len(solutions) == 4 # [[(rain Here), (rain There)], [(rain Here), (hose There)], [(rain There), (hose Here)], [(hose Here), (hose There)]]

def test_3_different_obs():
    kb, _ = KnowledgeBase.from_src(test_problem)
    obs = kb.add_src("(wet Here) (wet There) (wet Everywhere)")
    solutions = abduction(obs, kb, 5)
    assert len(solutions) == 8 # [[(rain Everywhere), (rain Here), (rain There)], [(hose Everywhere), (rain Here), (rain There)], [(rain Everywhere), (rain Here), (hose There)], [(hose Everywhere), (rain Here), (hose There)], [(rain Everywhere), (hose Here), (rain There)], [(hose Everywhere), (hose Here), (rain There)], [(rain Everywhere), (hose Here), (hose There)], [(hose Everywhere), (hose Here), (hose There)]]

def test_2_obs_w_var():
    kb, obs = KnowledgeBase.from_src(test_problem)
    obs.extend(kb.add_src("(wet Here)"))
    solutions = abduction(obs, kb, 5)
    assert len(solutions) == 6 # [[(rain Here)], [(rain $1), (rain Here)], [(rain $1), (hose Here)], [(hose $1), (rain Here)], [(hose Here)], [(hose $1), (hose Here)]]


problem_additions = '''

;; hose
(if (gardening ?loc)
    (hose ?loc))

;; rain
(if (rainy_season ?loc)
    (rain ?loc))

'''

def test_backchaining():
    kb, obs = KnowledgeBase.from_src(test_problem + problem_additions)
    solutions = abduction(obs, kb, 5)
    assert len(solutions) == 2 # [[(rainy_season $1)], [(gardening $1)]]

def test_backchaining_depth():
    kb, obs = KnowledgeBase.from_src(test_problem + problem_additions)
    solutions = abduction(obs, kb, 0)
    print(solutions)
    assert len(solutions) == 0