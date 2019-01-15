
;; Given

(card_heart)
(card_train)
(card_baseball)

;; why card heart? Maybe someone's heart

(if (and (heart_of' e heart person)
	 (etc6_card_heart 0.1 e heart person))
    (card_heart))

;; why heart_of someone? Maybe they have heart disease

(if (and (heart_disease' e1 person)
	 (etc1_heart_of 0.1 e e1 heart person))
    (heart_of' e heart person))

;; why heart_disease? Maybe polluted workplace_of

(if (and (polluted' e1 location)
	 (workplace_of' e2 person location)
	 (etc1_heart_disease 0.1 e e1 e2 person location))
    (heart_disease' e person))

;; Hack: Everyone with heart disease dies!

(if (heart_disease' e person)
    (dies' e person))

;; Why polluted? Maybe near polluting trains

(if (and (polluting_trains' e1 trains)
	 (happens_near' e2 e1 location)
	 (etc1_polluted 0.1 e e1 e2 trains location))
    (polluted' e location))

;; Why polluting trains? They happen.

(if (etc0_polluting_trains 0.1 e trains)
    (polluting_trains' e trains))

;; Why happens near? It happens

(if (etc0_happens_near 0.1 e1 e2 location) (happens_near' e1 e2 location))

;; Why card_train? Maybe polluting trains

(if (and (polluting_trains' e1 trains)
	 (etc6_card_train 0.1 e1 trains))
    (card_train))

;; Why workplace_of? It happens

(if (etc0_workplace_of 0.1 e person location)
    (workplace_of' e person location))

;; why card_baseball? Maybe a baseball player!

(if (and (baseball_player' e person)
	 (etc6_card_baseball 0.1 e person))
    (card_baseball))

;; why baseball_player? Maybe someone works at a practice field

(if (and (practice_field' e1 location)
	 (workplace_of' e2 person location)
	 (etc1_baseball_player 0.1 e e1 e2 person location))
    (baseball_player' e person))

;; why practice field? It happens

(if (etc0_practice_field 0.1 e location) (practice_field' e location))



    
