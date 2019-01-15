;; given

(card_heart)
(card_train)
(card_baseball)

;; Why heart? Maybe symbolic of love

(if (and (symbolic_of_love' e)
	 (etc2_card_heart 0.1 e))
    (card_heart))

;; Why symbolic of love? Maybe heartbreak

(if (and (heartbreak' e1 x)
	 (etc2_symbolic_of_love 0.1 e e1 x))
    (symbolic_of_love' e))

;; Why heartbreak? Maybe missed event

(if (and (missed_event' e1 person event)
	 (etc1_heartbreak 0.1 e e1 person event))
    (heartbreak' e person))

;; Why missed event? Maybe scheduling failure of transport

(if (and (scheduled_event' e1 event location)
	 (scheduled_transport' e2 person location transporter)
	 (execution_schedule_failure' e3 transporter)
	 (etc1_missed_event 0.1 e e1 e2 e3 event location person transporter))
    (missed_event' e person event))

;; why execution_schedule_failure? it happens
(if (etc0_execution_schedule_failure 0.1 e transporter)
    (execution_schedule_failure' e transporter))

;; why scheduled_tranport? Maybe it is a train_trip?
(if (and (train_trip' e1 passenger location transporter)
	 (etc1_scheduled_transport 0.1 e e1 passenger location transporter))
    (scheduled_transport' e passenger location transporter))

;; Why train_trip? It happens
(if (etc0_train_trip 0.1 e passenger location transporter)
    (train_trip' e passenger location transporter))

;; why sheduled_event? Maybe baseball_game
(if (and (baseball_game' e1)
	 (etc1_scheduled_event' 0.1 e e1 event location))
    (scheduled_event' e event location))

;; why baseball_game? it happens
(if (etc0_baseball_game 0.1 e) (baseball_game' e))

;; Why card_train? Maybe train trip
(if (and (train_trip' e passenger location transporter)
	 (etc4_card_train 0.1 e passenger location transporter))
    (card_train))

;; why card_baseball? maybe a baseball game
(if (and (baseball_game' e1)
	 (etc2_card_baseball 0.1 e1))
    (card_baseball))
   
