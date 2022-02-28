;; It is dark, and you are almost sure you saw a flash of light

(dark' E1) (xor_flash_of_light' E2 L 0.99 0.01)

;; You know very little about darkness:

(if (etc0_dark 0.3 e)
    (dark' e))

;; You know a bit about flashes of light:

(if (etc0_flash_of_light 0.01 e l)
    (flash_of_light' e l))

(if (and (firefly' e1 f)
	 (etc1_flash_of_light 0.8 e e1 l f))
    (flash_of_light' e l))

;; And a bit about fireflies

(if (etc0_firefly 0.01 e f)
    (firefly' e f))

(if (and (dark' e1)
	 (etc1_firefly 0.7 e e1 f))
    (firefly' e f))


;; likelihood

;(if (etc0_likelihood pr e)
;    (likelihood' e pr))

;; XOR trick, with confidence

;(if (and (flash_of_light' e1 l)
;	 (likelihood' e2 pr1)
;	 (etc1_xor_flash_of_light 1.0 e e1 e2 l pr1 pr2))
;    (xor_flash_of_light' e l pr1 pr2))

;(if (and (likelihood' e1 pr2)
;	 (etc2_xor_flash_of_light 1.0 e e1 l pr1 pr2))
;    (xor_flash_of_light' e l pr1 pr2))

;; simplification

(if (and (flash_of_light' e1 l)
	 (etc1_xor_flash_of_light pr1 e e1 l pr2))
    (xor_flash_of_light' e l pr1 pr2))

(if (etc2_xor_flash_of_light pr2 e l pr1)
    (xor_flash_of_light' e l pr1 pr2))
