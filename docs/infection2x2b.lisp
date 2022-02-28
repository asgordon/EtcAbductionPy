(positive T1 P)
(positive T2 P)

(if (and (infected x)
         (etc_true_positive 1.0 t x))
    (positive t x))

(if (and (healthy x)
         (etc_false_positive 0.05 t x))
    (positive t x))

(if (etc_healthy 0.98 x)
    (healthy x))

(if (etc_infected 0.02 x)
    (infected x))

(if (etc_positive 0.069 t x)
    (positive t x))

(if (and (healthy x)
	 (positive T1 x)
	 (etc_false_positive_2 1.0 x))
    (positive T2 x))
