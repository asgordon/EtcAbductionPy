

;; Given

(card_train)
(card_baseball)
(card_heart)

;; Why card_train? Maybe it's a pun for practice

(if (and (english_pun_for_practice' e)
	 (etc3_card_train 0.1 e))
    (card_train))

;; Why english pun for practice? Maybe a practice event

(if (and (practice' e1 person ability)
	 (etc1_english_pun_for_practice 0.1 e e1 person ability))
    (english_pun_for_practice' e))

;; Why practice? Maybe ambition to be better

(if (and (ambition_to_be_better' e1 person ability)
	 (etc1_practice 0.1 e e1 person ability))
    (practice' e person ability))

;; Why ambition_to_be_better? Maybe you admiration

(if (and (admiration' e1 viewer master ability)
	 (etc1_ambition_to_be_better 0.1 e e1 viewer master ability))
    (ambition_to_be_better' e viewer ability))

;; Why admiration? Maybe sports performance done really well

(if (and (sports_performance' e1 player ability)
	 (done_very_well' e2 e1)
	 (etc1_admiration 0.1 e e1 e2 player ability viewer))
    (admiration' e viewer player ability))

;; Why done very well? It happens

(if (etc0_done_very_well 0.1 e e1) (done_very_well' e e1))

;; Why sports_performance? Maybe an at bat

(if (and (at_bat' e1 batter)
	 (etc1_sports_performance 0.1 e e1 batter ability))
    (sports_performance' e batter ability))

;; Why at bat? It happens

(if (etc0_at_bat 0.1 e1 b) (at_bat' e1 b))

;; Why card_baseball? Maybe at bat

(if (and (at_bat' e1 b)
	 (etc1_card_baseball 0.1 e1 b))
    (card_baseball))


;; Why heart? Maybe symbolic of love

(if (and (symbolic_of_love' e)
	 (etc2_card_heart 0.1 e))
    (card_heart))

;; Why symbolic of love? Maybe admiration

(if (and (admiration' e1 viewer master ability)
	 (etc2_symbolic_of_love 0.1 e e1 viewer master ability))
    (symbolic_of_love' e))








