;; The observables

(collapse K)
(missing_nail n S)

;; Priors of the observables

(if (etc0_collapse 0.001 x) (collapse x))
(if (etc0_missing_nail 0.001 x y) (missing_nail x y))

;; Knowledge

;; For want of a battle the kingdom was lost
(if (and (battle_lost_to x y)
	 (etc1_collapse 0.5 x))
    (collapse x))

(if (etc0_battle_lost_to 0.001 x y) (battle_lost_to x y))

;; For want of a message the battle was lost
(if (and (missing_message_about m y)
	 (etc1_battle_lost_to 0.5 x y m))
    (battle_lost_to x y))

(if (etc0_missing_message_about 0.001 m y) (missing_message_about m y))

;; for want of a rider the message was lost
(if (and (missing_rider r m)
	 (etc1_missing_message_about 0.5 r m y))
    (missing_message_about m y))

(if (etc0_missing_rider 0.001 r m) (missing_rider r m))

;; For want of a horse the rider was lost
(if (and (missing_horse h r)
	 (etc1_missing_rider 0.5 h r m))
    (missing_rider r m))

(if (etc0_missing_horse 0.001 h r) (missing_horse h r))

;; For want of a shoe the horse was lost
(if (and (missing_shoe s h)
	 (etc1_missing_horse 0.5 h s r))
    (missing_horse h r))

(if (etc0_missing_shoe 0.001 s h) (missing_shoe s h))

;; For want of a nail the shoe was lost
(if (and (missing_nail n s)
	 (etc1_missing_shoe 0.0005 n s h))  ;; <-- or is it 0.0005?
    (missing_shoe s h))



;; Alternative formulation of missing shoe

;(if (and (missing_nail n s)
;	 (shoe_on_horse s h)
;	 (etc2_missing_shoe 0.5 n s h))
;    (missing_shoe s h))
;
;(if (etc0_shoe_on_horse 0.001 s h) (shoe_on_horse s h))
