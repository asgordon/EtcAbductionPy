;; Given

(card_heart)
(card_baseball)
(card_train)

;; Why card heart? Maybe something has the shape of a heart

(if (and (shape_of_heart' e object)
	 (etc8_card_heart 0.1 e object))
    (card_heart))

;; Why shape of object? Maybe crafted object

(if (and (crafted_object' e1 object)
	 (etc1_shape_of_heart' 0.1 e e1 object))
    (shape_of_heart' e object))

;; Why crafted object? Maybe a pinata

(if (and (pinata' e1 object)
	 (etc1_crafted_object 0.1 e e1 object))
    (crafted_object' e object))

;; Why pinata? Maybe a pinata game

(if (and (pinata_game' e1 player pinata bat)
	 (etc1_pinata 0.1 e e1 player pinata bat))
    (pinata' e pinata))

;; Why Pinata game? Maybe birthday party

(if (and (birthday_party' e1 attendee location)
	 (etc1_pinata_game 0.1 e e1 attendee location pinata bat))
    (pinata_game' e attendee pinata bat))

;; Why birthday party? It happens

(if (etc0_birthday_party 0.1 e attendee location)
    (birthday_party' e attendee location))

;; Why card baseball? Maybe swinging a bat

(if (and (swinging_bat' e1 person bat)
	 (etc8_card_baseball 0.1 e1 person bat))
    (card_baseball))

;; Why swinging a bat? Maybe pinata game

(if (and (pinata_game' e1 player pinata bat)
	 (etc1_swinging_bat 0.1 e e1 player bat pinata))
    (swinging_bat' e player bat))


;; Why card_train? Maybe setting of event is a train

(if (and (train' e1 train)
	 (setting_of' e2 e1 train)
	 (etc8_card_train 0.1 e1 e2 train))
    (card_train))

;; Why train? it happens

(if (etc0_train 0.1 e train) (train' e train))

;; Why settting_of? Maybe a birthday party

(if (and (birthday_party' e1 attendee location)
	 (etc1_setting_of 0.1 e e1 attendee location))
    (setting_of' e e1 location))
    

    

  
  
