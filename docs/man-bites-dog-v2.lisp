;; "man bites dog" version 2

;; The observables

(man W1)
(bites W2)
(dog W3)
(seq W1 W2 W3)

;; why word man? maybe refering to a man

(if (and (man' e x)
	 (ref w x)
	 (etc1_word_man 0.1 e w x))
    (man w))

;; why man'? why not!

(if (etc0_man 0.1 e x) (man' e x))

;; why word bites? Maybe refering to a biting eventuality

(if (and (bite' e x y)
	 (ref w e)
	 (etc1_word_bites 0.1 e x y w))
    (bites w))

;; why bites'? why not!

(if (etc0_bite 0.1 e x y) (bite' e x y))

;; why dog? Maybe refering to a dog

(if (and (dog' e d)
	 (ref w d)
	 (etc1_word_dog 0.1 e w d))
    (dog w))

;; why dog'? why not!

(if (etc0_dog 0.1 e x) (dog' e x))

;; why ref? Why not!

(if (etc0_ref 0.1 w c) (ref w c))


;; why seq? maybe monotransitive construction

(if (and (monotransitive e x y)
	 (ref s1 x)
	 (ref s2 e)
	 (ref s3 y)
	 (etc1_seq 0.1 e x y s1 s2 s3))
    (seq s1 s2 s3))

;; why monotransitive? maybe bite'

(if (and (bite' e x y)
	 (etc1_monotransitive 0.1 e x y))
    (monotransitive e x y))

    
