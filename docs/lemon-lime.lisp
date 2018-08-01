;; Example 3: Lemon or Lime ? 

;; Observables: Four different fruit

(yellow FRUIT1)
(not_round FRUIT1)

(yellow FRUIT2)
(round FRUIT2)

(not_yellow FRUIT3)
(not_round FRUIT3)

(not_yellow FRUIT4)
(round FRUIT4)

;; Prior probabilities of class labels

(if (etc0_lime 0.6 x) (lime x)) ;; 600 / 1000
(if (etc0_lemon 0.4 x) (lemon x)) ;; 400 / 1000

;; Prior probabilities of features

(if (etc0_yellow 0.9 x) (yellow x))
(if (etc0_not_yellow 0.1 x) (not_yellow x))
(if (etc0_round 0.33 x) (round x))
(if (etc0_not_round 0.67 x) (not_round x))

;; conditional probabilities of the features given the class

(if (and (lime x) (etc1_yellow 0.9166666667 x)) ;; 550 / 600
    (yellow x))

(if (and (lime x) (etc1_not_yellow 0.08333333333 x)) ;; 50 / 600
    (not_yellow x))

(if (and (lemon x) (etc2_yellow 0.875 x)) ;; 350 / 400
    (yellow x))

(if (and (lemon x) (etc2_not_yellow 0.125 x)) ;; 50 / 400
    (not_yellow x))

(if (and (lime x) (etc1_round 0.5 x)) ;; 300 / 600
    (round x))

(if (and (lime x) (etc1_not_round 0.5 x)) ;; 300 / 600
    (not_round x))

(if (and (lemon x) (etc2_round 0.075 x)) ;; 30 / 400
    (round x))

(if (and (lemon x) (etc2_not_round 0.925 x)) ;; 370 / 400
    (not_round x))


