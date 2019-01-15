;; Given

(card_baseball)
(card_train)
(card_heart)

;; Why heart? Maybe symbolic of love

(if (and (symbolic_of_love' e)
	 (etc2_card_heart 0.1 e))
    (card_heart))

;; Why symbolic of love? Maybe fall_in_love

(if (and (fall_in_love' e1 x y)
	 (etc1_symbolic_of_love 0.1 e e1 x y))
    (symbolic_of_love' e))

;; Why love? Maybe repeated meeting

(if (and (repeated_meeting' e1 x y)
	 (etc1_fall_in_love 0.1 e e1 x y))
    (fall_in_love' e x y))

;; Why repeated meeting? Maybe train commuting?

(if (and (train_commuting' e1 from to passenger conductor)
	 (etc1_repeated_meeting 0.1 e e1 from to passenger conductor))
    (repeated_meeting' e passenger conductor))

;; Why train commuting? Maybe regular practice

(if (and (regular_practice' e1 player field)
	 (etc1_train_commuting 0.1 e e1 from field player conductor))
    (train_commuting' e from field player conductor))

;; Why regular practice? Maybe baseball_player

(if (and (baseball_player' e1 player)
	 (etc1_regular_practice 0.1 e e1 player location))
    (regular_practice' e player location))

;; Why baseball_player? It happens

(if (etc0_baseball_player 0.1 e x) (baseball_player' e x))

;; Why card_baseball? Maybe baseball player

(if (and (baseball_player' e x)
	 (etc2_card_baseball 0.1 e x))
    (card_baseball))

;; Why train_card? Maybe train_commuting

(if (and (train_commuting' e from to passenger conductor)
	 (etc2_train_card 0.1 e from to passenger conductor))
    (card_train))

;; Extra bonus

(if (train_commuting' e from to passenger conductor)
    (conductor' e conductor))
