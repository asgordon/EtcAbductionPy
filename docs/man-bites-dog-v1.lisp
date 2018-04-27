;; "man bites dog" version 1

;; the observables

(man)
(bites)
(dog)

;; why word bites? maybe bite'

(if (and (bite' e x y)
	 (etc1_word_bites 0.1 e x y))
    (bites))

;; why bites'? why not!

(if (etc0_bites 0.1 e x y) (bite' e x y))

;; why word man? may be a man

(if (and (man' e x)
	 (etc1_word_man 0.1 e x))
    (man))

;; why man'? why not!

(if (etc0_man 0.1 e x) (man' e x))

;; why word dog? maybe a dog

(if (and (dog' e x)
	 (etc1_word_dog 0.1 e x))
    (dog))

;; why dog'? why not! 

(if (etc0_dog 0.1 e x) (dog' e x))





;; Attempt #1: biting people is what dogs do

;; why a dog? maybe a dog biting a person

(if (and (person' e1 a)
	 (bite' e2 d a)
	 (etc1_dog 0.2 e e1 e2 d a))
    (dog' e d))

;; why person? why not!

(if (etc0_person 0.1 e x) (person' e x))

;; why person? maybe a man

(if (and (man' e1 x)
	 (etc1_person 1.0 e e1 x))
    (person' e x))

;; Attempt #2: Biting food is what people do

;; why man'? Maybe eating food

(if (and (food' e1 y)
	 (bite' e2 x y)
	 (etc1_man 0.2 e e1 e2 x y))
    (man' e x))

;; why food? why not!

(if (etc0_food 0.1 e x) (food' e x))

;; why food? maybe a dog

(if (and (dog' e1 x)
	 (etc2_dog 0.9 e e1 x))
    (food' e x))

