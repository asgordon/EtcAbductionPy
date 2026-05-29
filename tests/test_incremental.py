# test incremental py

from etcabductionpy import KnowledgeBase, incremental


test_kb = '''

;; The observables

(tick T1)
(tick T2)
(tick T3) 
(tick T4) 
(tick T5) 
(tick T6)
(tick T7) 
(tick T8)
(tick T9) 
(tick T10)
(tick T11)
(tick T12)
(tick T13)
(tick T14)
(tick T15)
(tick T16)
(tick T17)
(tick T18)
(tick T19)
(tick T20)

;; The prior

(if (etc0_tick 0.01 x) (tick x))

;; Maybe a clock

(if (and (clock c)
	 (etc1_tick 0.9 c x))
    (tick x))

(if (etc0_clock 0.001 c) (clock c))

'''

def test_incremental_twenty_ticks():
    kb, obs = KnowledgeBase.from_src(test_kb)
    obs = kb.standardize_literals(obs)
    solutions = incremental(obs, kb, 5, 10, 4, 10, skolemize_solutions=True)
    assert len(solutions) == 10
    # top solution should have one clock + 20 tick explanations
    top = solutions[0]
    clock_lits = [l for l in top if l.predicate == 'etc0_clock']
    tick_lits = [l for l in top if l.predicate == 'etc1_tick']
    assert len(clock_lits) == 1
    assert len(tick_lits) == 20