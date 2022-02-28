;; It is dark, and you either saw or didn't see a flash of light.

(dark' E1) (xor_flash_of_light' E2 L)

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
    

;; XOR trick

(if (and (flash_of_light' e1 l)
	 (etc1_xor_flash_of_light 1.0 e e1 l))
    (xor_flash_of_light' e l))

(if (etc2_xor_flash_of_light 1.0 e l)
    (xor_flash_of_light' e l))
