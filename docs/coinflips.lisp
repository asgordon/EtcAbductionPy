
(coinflip' E1 Coin1) (xor_heads_tails' E2 Coin1)

(if (etc0_coinflip 0.01 e coin)
    (coinflip' e coin))

(if (and (coinflip' e1 coin)
	 (etc1_heads' 0.5 e e1 coin))
    (heads' e coin))

(if (and (coinflip' e1 coin)
	 (etc1_tails' 0.5 e e1 coin))
    (tails' e coin))

(if (and (heads' e1 coin)
	 (etc1_xor_heads_tails 1.0 e e1 coin))
    (xor_heads_tails' e coin))

(if (and (tails' e1 coin)
    	 (etc2_xor_heads_tails 1.0 e e1 coin))
    (xor_heads_tails' e coin))
