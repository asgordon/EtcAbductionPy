(positive P)

(if (and (infected x)
         (etc_true_positive 1.0 x))
    (positive x))

(if (and (healthy x)
         (etc_false_positive 0.05 x))
    (positive x))

(if (etc_healthy 0.98 x)
    (healthy x))

(if (etc_infected 0.02 x)
    (infected x))

(if (etc_positive 0.069 x)
    (positive x))
