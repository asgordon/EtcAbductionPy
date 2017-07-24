;; The observables
;(task' E1 Me Mary E2)
;(water' E2 Mary Plant)
(vacation' E3 Me)
(dead' E4 Plant)

;; The priors
(if (etc0_dead 0.01 e x) (dead' e x))
(if (etc0_vacation 0.01 e x) (vacation' e x))
(if (etc0_task 0.1 e x y z) (task' e x y z))
(if (etc0_water 0.02 e x y) (water' e x y))

;; Why dead? Nobody watered
(if (and (didnt' e1 y e2)
	 (water' e2 y x)
	 (etc1_dead 0.9 e e1 e2 x y))
    (dead' e x))

;; why didnt? couldnt
(if (and (couldnt' e2 x e)
	 (etc1_didnt 0.9 e e1 e2 x))
    (didnt' e x e1))

;; why didnt? forgot
(if (and (forgot' e2 x e1)
	 (task' e3 y x e1)
	 (etc1_didnt 0.9 e e1 e2 e3 x y))
    (didnt' e x e1))

;; why couldnt? On vacation
(if (and (vacation' e1 x)
	 (etc1_couldnt 0.9 e e1 e2 x))
    (couldnt' e x e2))

;; why task? couldnt oneself
(if (and (couldnt' e2 x e1)
	 (etc1_task 0.9 e e1 e2 x y))
    (task' e x y e1))

;; priors on assumptions
(if (etc0_didnt 0.01 e1 y e2) (didnt' e1 y e2))
(if (etc0_couldnt 0.01 e1 y e2) (couldnt' e1 y e2))
(if (etc0_forgot 0.05 e x e1) (forgot' e x e1))


