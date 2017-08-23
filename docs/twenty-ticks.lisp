

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
