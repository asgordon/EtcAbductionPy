;; Given

(card_train)
(card_baseball)
(card_heart)

;; Why card_train? Maybe late train

(if (and (frequently_late_train' e1 train station days)
	 (etc1_card_train 0.1 e1 train station days))
    (card_train))

;; For clarity, train is a train

(if (frequently_late_train' e1 train station days)
    (train' e train))

;; Why frequently late train? Maybe its a person, frequently distracted along the way

(if (and (anthropomorphized' e1 train)
	 (frequently_distracted' e2 train path days)
	 (path_destination' e3 path station)
	 (etc1_frequently_late_train 0.1 e e1 e2 e3 train path station days))
    (frequently_late_train' e train station days))

;; Why anthropomorphize? Interesting, but let's say it just happens.

(if (etc0_anthropomorphized 0.1 e1 object)
    (anthropomorphized' e1 object))

;; Why path_destination? It happens

(if (etc0_path_destination 0.1 e path destination)
    (path_destination' e path destination))

;; Why frequently distracted? Maybe frequent interesting events

(if (and (frequent_events_at_location' e1 e2 location days)
	 (frequently_watching' e3 person e2 days)
	 (etc1_distracted 0.1 e e1 e2 e3 person location days))
    (frequently_distracted' e person location days))

;; Why event at location? Maybe a baseball game

(if (and (baseball_games' e2 days)
	 (etc1_events_at_location 0.1 e1 e2 location days))
    (frequent_events_at_location' e1 e2 location days))

;; why baseball_games? it happens

(if (etc0_baseball_games 0.1 e days) (baseball_games' e days))

;; Why frequently watching? Maybe love of event type

(if (and (love_of' e1 person e2)
	 (etc1_frequently_watching 0.1 e e1 person e2 days))
    (frequently_watching' e person e2 days))

;; Why love_of? It happens

(if (etc0_love_of 0.1 e1 person e2)
    (love_of' e1 person e2))

;; Why heart? Maybe symbolic of love

(if (and (symbolic_of_love' e)
	 (etc2_card_heart 0.1 e))
    (card_heart))

;; Why symbolic of love? Maybe love of something

(if (and (love_of' e1 person e2)
	 (etc1_symbolic_of_love 0.1 e e1 person e2))
    (symbolic_of_love' e))

;; why card_baseball? maybe a baseball game season

(if (and (baseball_games' e1 gamedays)
	 (etc2_card_baseball 0.1 e1 gamedays))
    (card_baseball))





    
