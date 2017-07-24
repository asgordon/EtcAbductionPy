;; The observables

(chicken C)
(egg E)

;; The priors of the observables

(if (etc0_chicken 0.001 x) (chicken x))
(if (etc0_egg 0.002 x) (egg x))

;; Why egg? Maybe a hen

(if (and (hen x)
	 (etc1_egg 0.1 x y))
    (egg y))

;; Why chicken? Maybe its a hen

(if (and (hen x)
	 (etc1_chicken 1.0 x))
    (chicken x))

;; The prior probabilities of assummed literals

(if (etc0_hen 0.0005 x) (hen x))
	 
