(xor_sunny_snowstorm' E1)

(if (etc0_sunny 0.6 e)
    (sunny' e))

(if (etc0_snowstorm 0.2 e)
    (snowstorm' e))
  
(if (and (sunny' e1)
	 (etc1_xor_sunny_snowstorm 1.0 e e1 coin))
    (xor_sunny_snowstorm' e))

(if (and (snowstorm' e1)
	 (etc2_xor_sunny_snowstorm 1.0 e e1 coin))
    (xor_sunny_snowstorm' e))
