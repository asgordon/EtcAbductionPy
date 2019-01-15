;; Given

(card_baseball)
(card_train)
(card_heart)

;; Interpretation 1: Miles's idea

;; Why heart? Maybe a racing heart

(if (and (racing_heart' e1 h)
	 (etc1_card_heart 0.1 e1 h))
    (card_heart))

;; Why performance anxiety? Maybe at bat

(if (and (at_bat' e1 b)
	 (etc1_performance_anxiety 0.1 e1 e b))
    (performance_anxiety' e b))

;; Why baseball? Maybe at bat

(if (and (at_bat' e1 b)
	 (etc1_card_baseball 0.1 e1 b))
    (card_baseball))

;; Why train? Maybe metaphor for like a train

(if (and (like_a_train' e1 e2)
	 (etc1_card_train 0.1 e1 e2))
    (card_train))

;; Why like a train? Maybe racing heart

(if (and (racing_heart' e1 p)
	 (etc1_like_a_train 0.1 e e1 p))
    (like_a_train' e e1))

;; Why at bat? Maybe playing sports

(if (and (playing_sports' e1 p)
	 (etc1_at_bat 0.1 e e1 p))
    (at_bat' e p))

;; Why playing sports? It happens

(if (etc0_playing_sports 0.1 e p) (playing_sports' e p))

;; Why racing heart? Maybe playing sports

(if (and (playing_sports' e1 p)
	 (etc2_racing_heart 0.1 e1 e p h))
    (racing_heart' e h))
	 
