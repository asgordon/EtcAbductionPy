;; tricopa-kb.lisp
;; Andrew S. Gordon
;; January 2015

;; accelerate

(if (etc0_accelerate 0.01 e x) (accelerate' e x))

;; accelerate 1: Maybe you want to quickly move somewhere

(if (and (goal' e1 e2 x)
	 (quickly' e2 e3)
	 (moveTo' e3 x l)
	 (etc1_accelerate 0.9 e1 e2 e3 e x l))
    (accelerate' e x))

;; accompany

(if (etc0_accompany 0.01 e x y) (accompany' e x y))

;; accompany 1: maybe you are happily strolling with someone

(if (and (stroll' e1 y)
	 (happy' e2 x)
	 (happy' e3 y)
	 (etc1_accompany 0.1 e1 e2 e3 e x y))
    (accompany' e x y))

;; accompany 2 (bt-lt): maybe bt is the parent

(if (and (parent' e1 BT LT)
	 (etc2_accompany 0.8 e1 e))
    (accompany' e LT BT))

;; accompany 3: maybe you are exiting with a friend

(if (and (friend' e1 x y)
	 (exit' e2 y)
	 (etc3_accompany 0.5 e1 e2 e x y))
    (accompany' e x y))

;; accompany 4: maybe you like them

(if (and (like' e1 x y)
	 (etc4_accompany 0.5 e e1 x y))
    (accompany' e x y))

;; acquaintance

(if (etc0_acquaintance 0.5 e x y) (acquaintance' e x y))

;; afraid

(if (etc0_afraid 0.1 e x) (afraid' e x))

;; afraid 1: maybe you see something threatening

(if (and (see' e1 x y)
	 (threat0' e2 y x)
	 (etc1_afraid 0.75 e1 e2 e x y))
    (afraid' e x))

;; afraid 2: maybe you fear an attack

(if (and (fearThat' e1 x e2)
	 (attack' e2 y x)
	 (etc2_afraid 0.8 e1 e2 e x y))
    (afraid' e x))

;; agree

(if (etc0_agree 0.1 e x y) (agree' e x y))

;; angry

(if (etc0_angry 0.2 e x) (angry' e x))

;; angryAt

(if (etc0_angryAt 0.1 e x y) (angryAt' e x y))

;; angryAt 1: Maybe they trying to annoy you

(if (and (annoy' e1 x y)
	 (goal' e2 e1 x)
	 (etc1_angryAt 0.8 e1 e2 e x y))
    (angryAt' e y x))

;; angryAt 2: Maybe you are angry that they flirted with your love

(if (and (love' e1 x y)
	 (flirtWith' e2 z y)
	 (etc2_angryAt 0.9 e1 e2 e x y z))
    (angryAt' e x z))

;; angryAt 3: maybe they attacked someone you like

(if (and (attack' e1 y z)
         (like' e2 x z)
         (etc3_angryAt 0.9 e1 e2 e x y z))
    (angryAt' e x y))

;; angryAt 4:  maybe they bothered your child

(if (and (bother' e1 y z)
         (parent' e2 x z)
         (etc4_angryAt 0.9 e1 e2 e x y z))
    (angryAt' e x y))

;; angryAt 5: maybe they attacked you ;; added?

(if (and (attack' e1 y x)
         (etc5_angryAt 0.9 e1 e2 e x y))
    (angryAt' e x y))

;; annoy

(if (etc0_annoy 0.1 e x y) (annoy' e x y))

;; annoy 1: maybe because they are poking you

(if (and (poke' e1 x y)
	 (etc1_annoy 0.8 e1 e x y))
    (annoy' e x y))

;; annoy 2: maybe because they argued with you

(if (and (argueWith' e1 x y)
	 (etc2_annoy 0.4 e1 e x y))
    (annoy' e x y))

;; approach

(if (etc0_approach 0.05 e x y) (approach' e x y)) ;; raised from 0.01

;; approach 1: maybe you want to attack
(if (and (goal' e1 e2 x)
         (attack' e2 x y)
         (etc1_approach 0.3 e1 e2 e x y))
    (approach' e x y))

;; approach 2 (door): maybe you want to open it
(if (and (goal' e1 e2 x)
	 (open' e2 x D)
	 (etc2_approach 0.8 e1 e2 e x))
    (approach' e x D))

;; approach 3: maybe you want to help

(if (and (goal' e1 e2 x)
	 (help' e2 x y)
	 (etc3_approach 0.3 e1 e2 e x y))
    (approach' e x y))

;; approach 4 (door): maybe you want to enter
(if (and (goal' e1 e2 x)
	 (enter' e2 x)
	 (etc4_approach 0.8 e1 e2 e x))
    (approach' e x D))

;; approach 5 (door): maybe you want to exit
(if (and (goal' e1 e2 x)
	 (exit' e2 x)
	 (etc5_approach 0.85 e1 e2 e x))
    (approach' e x D))

;; approach 6: maybe you want to be with your friend
(if (and (friend' e1 x y)
	 (etc6_approach 0.1 e1 e x y))
    (approach' e x y))

;; approach 7: maybe you want to help an attack
(if (and (attack' e1 y z)
	 (goal' e2 e3 x)
	 (help' e3 x y)
	 (etc7_approach 0.35 e1 e2 e3 e x y z))
    (approach' e x z))

;; argueWith

(if (etc0_argueWith 0.01 e x y) (argueWith' e x y))

;; argueWith 1 : maybe you disagree

(if (and (disagree' e1 x y)
	 (etc1_argueWith 0.1 e1 e x y))
    (argueWith' e x y))

;; argueWith 2: Maybe you want the opposite of their goal

;(if (and (goal' e1 e2 x)
;	 (not' e2 e3)
;	 (goal' e4 e3 y)
;	 (etc2_argueWith 0.5 e1 e2 e3 e4 x y))
;   (argueWith' e x y))

;; argueWith 3: maybe you are angry

(if (and (angry' e1 x)
	 (etc3_argueWith 0.1 e e1 x y))
    (argueWith' e x y))

;; arguewith 4: maybe they are argueing with you too

(if (and (argueWith' e1 y x)
	 (etc4_argueWith 0.8 e e1 x y))
    (argueWith' e x y))

;; argueWith 5: maybe you are angry at them

(if (and (angryAt' e1 x y)
	 (etc5_argueWIth 0.5 e e1 x y))
    (argueWith' e x y))



;; asleep

(if (etc0_asleep 0.3 e x) (asleep' e x))

;; atLoc

(if (etc0_atLoc 0.1 e x l) (atLoc' e x l))

;; atLoc (2 args) -1 eventuality locations

(if (etc0b_atLoc 0.01 e l) (atLoc' e l))

;; atLoc 1 : maybe you are talking to someone there

(if (and (talkTo' e1 x y)
	 (etc1_atLoc 0.2 e1 e x y l))
    (atLoc' e x l))

;; attack

(if (etc0_attack 0.1 e x y) (attack' e x y))

;; attack 1: maybe they are angry at you

(if (and (angryAt' e1 x y)
	 (etc1_attack 0.1 e1 e x y))
    (attack' e x y))

;; attack 2: maybe they are angry 

(if (and (angry' e1 x)
	 (etc2_attack 0.1 e e1 x y))
    (attack' e x y))


;; avoid

(if (etc0_avoid 0.06 e x y) (avoid' e x y))

;; avoid 1 : maybe they annoy you

(if (and (annoy' e1 x y)
	 (etc1_avoid 0.4 e1 e x y))
    (avoid' e y x))

;; avoid 2: maybe you fear they will attack you

(if (and (fearThat' e1 x e2)
	 (attack' e2 y x)
	 (etc2_avoid 0.9 e1 e2 e x y))
    (avoid' e x y))

;; avoid 3: maybe you dislike them

(if (and (dislike' e1 x y)
	 (etc3_avoid 0.4 e1 e x y))
    (avoid' e x y))

;; avoid 4: maybe you dislike them and their unwanted flirtations

(if (and (dislike' e1 x y)
	 (flirtWith' e2 y x)
	 (etc4_avoid 0.8 e1 e2 e x y))
    (avoid' e x y))

;; avoid 5: maybe you are afraid

(if (and (afraid' e1 x)
	 (etc5_avoid 0.3 e1 e x y))
    (avoid' e x y))

;; block

(if (etc0_block 0.01 e x y) (block' e x y))

;; block 1: maybe your goal is to defend someone from an attack

(if (and (attack' e1 y z)
	 (goal' e2 e3 x)
	 (defend' e3 x z)
	 (etc1_block 0.75 e1 e2 e3 e x y z))
    (block' e x y))

;; block 2: maybe you want to prevent someone from doing something

(if (and (goal' e1 e2 x)
	 (prevent' e2 x e3)
	 (goal' e4 e3 y)
	 (etc2_block 0.5 e1 e2 e3 e x y))
    (block' e x y))

;; bolt

(if (etc0_bolt 0.01 e x) (bolt' e x))

;; bolt 1: maybe you are trying to avoid someone

(if (and (goal' e1 e2 x)
	 (avoid' e2 x y)
	 (etc1_bolt 0.5 e1 e2 e x y))
    (bolt' e x))

;; bored

(if (etc0_bored 0.1 e x) (bored' e x))

;; bored 1: maybe because you've been inside all day

(if (and (inside' e1 x)
	 (etc1_bored 0.2 e1 e x))
    (bored' e x))

;; bother

(if (etc0_bother 0.05 e x y) (bother' e x y))

;; bother 1: maybe you want them to be afraid

(if (and (goal' e1 e2 x)
	 (afraid' e2 y)
	 (etc1_bother 0.6 e1 e2 e x y))
    (bother' e x y))

;; bother 2: maybe you are bullying

(if (and (bully' e1 x y)
	 (etc2_bother 0.1 e1 e x y))
    (bother' e x y))

;; bully

(if (etc0_bully 0.1 e x y) (bully' e x y))

;; chase

(if (etc0_chase 0.01 e x y) (chase' e x y))

;; chase 1: Maybe playing tag

(if (and (playWith' e1 x y)
	 (etc1_chase 0.2 e1 e x y))
    (chase' e x y))

;; chase 2: Maybe angryAt

(if (and (angryAt' e1 x y)
	 (etc2_chase 0.2 e1 e x y))
    (chase' e x y))

;; chase 3: Maybe to rob them of something

(if (and (goal' e1 e2 x)
	 (rob' e2 x y)
	 (etc3_chase 0.3 e1 e2 e x y))
    (chase' e x y))

;; chase 4: Maybe you want to scare them

(if (and (goal' e1 e2 x)
	 (afraid' e2 y)
	 (etc4_chase 0.4 e1 e2 e x y))
    (chase' e x y))

;; chase 5: Maybe you want to attack them

(if (and (goal' e1 e2 x)
	 (attack' e2 x y)
	 (etc5_chase 0.4 e1 e2 e x y))
    (chase' e x y))

;; close

(if (etc0_close 0.01 e x d) (close' e x d))

;; close 1: maybe you don't like the person outside
(if (and (outside' e1 y)
	 (dislike' e2 x y)
	 (inside' e3 x)
	 (etc1_close 0.75 e1 e2 e3 e x y d))
    (close' e x d))

;; cold

(if (etc0_cold 0.1 e x) (cold' e x))

;; conflicted -1

(if (etc0_conflicted 0.01 e x e1) (conflicted' e x e1))

;; console

(if (etc0_console 0.1 e x y) (console' e x y))

;; creep

(if (etc0_creep 0.01 e x) (creep' e x))

;; creep 1: maybe you don't want to be seen

(if (and (goal' e1 e2 x)
	 (not' e2 e3)
	 (see' e3 y x)
	 (etc1_creep 0.9 e1 e2 e3 e x y))
    (creep' e x))

;; creep 2: maybe you don't want someone to know you are exiting

(if (and (exit' e1 x)
	 (goal' e2 e3 x)
	 (not' e3 e4)
	 (know' e4 y e1)
	 (inside' e5 y)
	 (etc2_creep 0.9 e1 e2 e3 e4 e5 e x y))
    (creep' e x))

;; creepUpOn

(if (etc0_creepUpOn 0.01 e x y) (creepUpOn' e x y))

;; creepUpOn 1: maybe you don't want to be seen
(if (and (goal' e1 e2 x) 
	 (not' e2 e3)
	 (see' e3 y x)
	 (etc1_creepUpOn 0.9 e1 e2 e3 e x y))
    (creepUpOn' e x y))

;; curious

(if (etc0_curious 0.2 e x) (curious' e x))

;; dance

(if (etc0_dance 0.01 e x) (dance' e x))

;; dance 1 : maybe you are happy

(if (and (happy' e1 x)
	 (etc1_dance 0.1 e1 e x))
    (dance' e x))

;; decelerate

(if (etc0_decelerate 0.01 e x) (decelerate' e x))

;; decelerate 1 : maybe because you are exhausted

(if (and (exhausted' e1 x)
	 (etc1_decelerate 0.8 e1 e x))
    (decelerate' e x))

;; defend

(if (etc0_defend 0.1 e x y) (defend' e x y))

;; defend 1: maybe they are being attacked

(if (and (attack' e1 x y)
	 (etc1_defend 0.75 e1 e x y z))
    (defend' e z y))

;; disabled

(if (etc0_disabled 0.01 e x) (disabled' e x))


;; disagree

(if (etc0_disagree 0.1 e x y) (disagree' e x y))

;; disappointed -1

(if (etc0_disappointed 0.01 e x e1) (disappointed' e x e1))

;; discipline

(if (etc0_discipline 0.1 e x y) (discipline' e x y))

;; discipline 1: maybe they hit something

(if (and (hit' e1 y z)
	 (parent' e2 x y)
	 (etc1_discipline 0.9 e1 e2 e x y z))
    (discipline' e x y))


;; dislike

(if (etc0_dislike 0.1 e x y) (dislike' e x y))

;; dislike 1: maybe they annoy you

(if (and (annoy' e1 x y)
	 (etc1_dislike 0.75 e1 e x y))
    (dislike' e y x))

;; embarrassed

(if (etc0_embarrassed 0.1 e1 x e2) (embarrassed' e1 x e2))

;; energized

(if (etc0_energized 0.1 e x) (energized' e x))

;; enemies -1

(if (etc0_enemies 0.01 e x y) (enemies' e x y))

;; enter

(if (etc0_enter 0.05 e x) (enter' e x))

;; escape

(if (etc0_escape 0.01 e x y) (escape' e x y))

;; escape 1: maybe your goal is to avoid

(if (and (goal' e1 e2 x)
	 (avoid' e2 x y)
	 (etc1_escape 0.5 e1 e2 e x y))
    (escape' e x y))

;; escape 2: maybe you just robbed them of something

(if (and (rob' e1 x y)
	 (etc2_escape 0.1 e1 e x y))
    (escape' e x y))

;; examine

(if (etc0_examine 0.01 e x y) (examine' e x y))

;; examine 1 : maybe you want to know something about it

(if (and (knowledgeGoal' e1 e2 x)
	 (etc1_examine 0.25 e1 e2 e x y))
    (examine' e x y))

;; excited

(if (etc0_excited 0.1 e x) (excited' e x))

;; excited 1: maybe you see someone you like

(if (and (see' e1 x y)
	 (like' e2 x y)
	 (etc1_excited 0.8 e1 e2 e x y))
    (excited' e x))

;; excitedThat -1

(if (etc0_excitedThat 0.01 e x e1) (excitedThat' e x e1))

;; exhausted

(if (etc0_exhausted 0.1 e x) (exhausted' e x))

;; exhausted 1: maybe you've been running

(if (and (run' e1 x)
	 (etc1_exhausted 0.2 e1 e x))
    (exhausted' e x))

;; exit

(if (etc0_exit 0.05 e x) (exit' e x))

;; exit 1: maybe to avoid someone inside

(if (and (avoid' e2 y x)
	 (goal' e3 e2 y)
	 (etc1_exit 0.5 e1 e2 e3 e x y))
    (exit' e y))

;; exit 2: maybe because you are inside

;(if (and (inside' e1 x)
;	 (etc2_exit 0.2 e1 x))
 ;    (exit' e x))

;; exit 3: maybe because someone outside was waiting to accompany you
(if (and (waitFor' e1 y e4)
	 (goal' e2 e3 y)
	 (accompany' e3 x y)
	 (etc3_exit 0.9 e1 e2 e3 e4 e x y))
    (exit' e4 x))


;; fear -1 

(if (etc0_fear 0.01 e x y) (fear' e x y))

;; fearThat

(if (etc0_fearThat 0.1 e1 x e2) (fearThat' e1 x e2))

;; fight

(if (etc0_fight 0.01 e x y) (fight' e x y))

;; fight 1: maybe its really a straightforward attack

(if (and (attack' e1 x y)
	 (goal' e2 e1 x)
	 (etc1_fight 0.3 e1 e2 e x y))
    (fight' e x y))

;; tried fight 2 here, but blew up question 51


;; flinch

(if (etc0_flinch 0.01 e x) (flinch' e x))

;; flinch 1: maybe you are startled
(if (and (startle' e1 y x) 
	 (etc1_flinch 0.9 e1 e x y))
    (flinch' e x))

;; flirtWith

(if (etc0_flirtWith 0.01 e x y) (flirtWith' e x y))

;; friend

(if (etc0_friend 0.1 e x y) (friend' e x y))

;; follow

(if (etc0_follow 0.01 e x y) (follow' e x y))

;; follow 1: maybe you are lost

(if (and (lost' e1 x)
	 (etc1_follow 0.1 e1 e x y))
    (follow' e x y))

;; forgotToDo 

(if (etc0_forgotToDo 0.01 e x e1) (forgotToDo' e x e1))

;; goal

(if (etc0_goal 0.5 e1 e2 x) (goal' e1 e2 x)) 

;; goodbye

(if (etc0_goodbye 0.1 e x y) (goodbye' e x y))

;; greet -1

(if (etc0_greet 0.01 e x y) (greet' e x y))

;; happy

(if (etc0_happy 0.5 e x) (happy' e x))

;; happyThat -1

(if (etc0_happyThat 0.01 e x e1) (happyThat' e x e1))

;; hate -1

(if (etc0_hate 0.01 e x y) (hate' e x y))

;; hear

(if (etc0_hear 0.3 e1 x e2) (hear' e1 x e2))

;; hear 1: maybe its someone approaching

(if (and (approach' e1 x y)
	 (etc1_hear 0.8 e1 e2 e x y)) ;; e2 = e1?
    (hear' e y e2))

;; help

(if (etc0_help 0.1 e x y) (help' e x y))

;; help 1: maybe because they are injured

(if (and (injured' e1 y)
	 (etc1_help 0.2 e1 e x y))
    (help' e x y))

;; hiding

(if (etc0_hiding 0.05 e x) (hiding' e x))

;; hiding 1: because you are embarrased and do not want to be seen

(if (and (embarrassed' e1 x e2)
	 (etc1_hiding 0.9 e1 e2 e x))
    (hiding' e x))

;; hit

(if (etc0_hit 0.01 e x y) (hit' e x y))

;; hit 1 : maybe you are angry

(if (and (angry' e1 x)
	 (etc1_hit 0.1 e1 e x y))
    (hit' e x y))

;; hit 2 : maybe you are angry at them

(if (and (angryAt' e1 x y)
	 (etc2_hit 0.15 e1 e x y))
    (hit' e x y))

;; hit 3: maybe the goal is to attack

(if (and (goal' e1 e2 x)
	 (attack' e2 x y)
	 (etc3_hit 0.2 e1 e2 e x y))
    (hit' e x y))

;; hit 4 (box): uncontrollable rage

(if (and (angry' e1 x)
	 (goal' e2 e3 x)
	 (not' e3 e1)
	 (etc4_hit 0.25 e1 e2 e3 e x))
    (hit' e x B))

;; hot -1

(if (etc0_hot 0.01 e x) (hot' e x))

;; huddleWith

(if (etc0_huddleWith 0.01 e x y) (huddleWith' e x y))

;; huddleWith 1 : maybe you are cold

(if (and (cold' e1 x)
	 (etc1_huddleWith 0.1 e1 e x y))
    (huddleWith' e x y))

;; hug

(if (etc0_hug 0.01 e x y) (hug' e x y))

;; hug 1 : maybe to console

(if (and (console' e1 x y)
	 (goal' e2 e1 x)
	 (etc1_hug 0.7 e1 e2 e x y))
    (hug' e x y))

;; hug 2 : maybe you like them

(if (and (like' e1 x y)
	 (etc2_hug 0.2 e1 e x y))
    (hug' e x y))

;; hug 3: maybe you are friends

(if (and (friend' e1 x y)
	 (etc3_hug 0.1 e1 e x y))
    (hug' e x y))

;; hug 4: maybe you are excited to see your friend

(if (and (friend' e1 x y)
	 (excited' e2 x)
	 (etc4_hug 0.1 e1 e2 e x y))
    (hug' e x y))

;; hug 5: maybe you are happy to resolve your argument

(if (and (argueWith' e1 x y)
	 (agree' e2 x y)
	 (agree' e3 y x)
	 (etc5_hug 0.3 e1 e2 e3 e x y))
    (hug' e x y))

;; hug 6: maybe you are relieved

(if (and (relief' e1 x e2)
;;	 (relief' e3 y e2)
	 (etc6_hug 0.6 e1 e2 e x y)) ;; e3
    (hug' e x y))

;; hug 7 : maybe you love them

(if (and (love' e1 x y)
	 (etc7_hug 0.1 e1 e x y))
    (hug' e x y))

;; injured

(if (etc0_injured 0.1 e x) (injured' e x))

;; injured 1: maybe you were in a fight

(if (and (fight' e1 x y)
	 (etc1_injured 0.5 e1 e x y))
    (injured' e x))


;; inside

(if (etc0_inside 0.2 e x) (inside' e x))

;; inside 1: maybe you are asleep

(if (and (asleep' e1 x)
	 (etc1_inside 0.5 e1 e x))
    (inside' e x))

;; ignore

(if (etc0_ignore 0.01 e x y) (ignore' e x y))

;; ignore 1: maybe you dislike them
(if (and (dislike' e1 x y)
	 (etc1_ignore 0.75 e1 e x y))
    (ignore' e x y))

;; ignore 2: maybe you just don't know them well (not friends)

(if (and (not' e1 e2)
	 (friend' e2 x y)
	 (etc2_ignore 0.5 e1 e2 e x y))
    (ignore' e x y))

;; jealous -1

(if (etc0_jealous 0.01 e x e1) (jealous' e x e1))

;; jump

(if (etc0_jump 0.01 e x) (jump' e x))

;; jump 1: Maybe you are excited

(if (and (excited' e1 x)
	 (etc1_jump 0.2 e1 e x))
    (jump' e x))

;; kidnap -1

(if (etc0_kidnap 0.01 e x y) (kidnap' e x y))

;; kiss

(if (etc0_kiss 0.01 e x y) (kiss' e x y))

;; kiss 1: because you love them and want to be happy

(if (and (love' e1 x y)
	 (goal' e2 e3 x)
	 (happy' e3 x)
	 (etc1_kiss 0.7 e1 e2 e3 e x y))
    (kiss' e x y))

;; knock

(if (etc0_knock 0.01 e x d) (knock' e x d))

;; knock 1: maybe you want someone to open it

(if (and (open' e1 y d)
	 (goal' e2 e1 x)
	 (etc1_knock 0.9 e1 e2 e x y d))
    (knock' e x d))

;; knock 2: maybe you want to enter

(if (and (goal' e1 e2 x)
	 (enter' e2 x)
	 (etc2_knock 0.9 e1 e2 e x d))
    (knock' e x d))

;; know

(if (etc0_know 0.2 e1 x e2) (know' e1 x e2))


;; knowledgeGoal

(if (etc0_knowledgeGoal 0.1 e1 e2 x) (knowledgeGoal' e1 e2 x))

;; knowledgeGoal 1 : maybe you are a curious person

(if (and (curious' e1 x)
	 (etc1_knowledgeGoal 0.6 e1 e2 e3 x))
    (knowledgeGoal' e2 e3 x))

;; lead

(if (etc0_lead 0.01 e x y) (lead' e x y))

;; lead 1: maybe you are the parent

(if (and (parent' e1 x y)
	 (etc1_lead 0.1 e1 e x y))
    (lead' e x y))

;; leave

(if (etc0_leave 0.01 e x y) (leave' e x y))

;; leave 1: maybe its goodbye time

(if (and (goodbye' e1 x y)
	 (etc1_leave 0.1 e1 e x y))
    (leave' e x y))

;; like

(if (etc0_like 0.2 e x y) (like' e x y))

;; like 1 : maybe because you got to know them

(if (and (acquaintance' e1 x y)
	 (etc1_like 0.3 e1 e x y))
    (like' e x y))

;; like 2 : maybe because you are their parent

;(if (and (parent' e1 x y)
;	 (etc2_like 0.9 e1 x y))
;    (like' e x y))

;; limp

(if (etc0_limp 0.01 e x) (limp' e x))

;; limp 1 : maybe you are injured

(if (and (injured' e1 x)
	 (etc1_limp 0.8 e1 e x))
    (limp' e x))

;; lost

(if (etc0_lost 0.1 e x) (lost' e x))

;; love

(if (etc0_love 0.3 e x y) (love' e x y))

;; meander

(if (etc0_meander 0.05 e x) (meander' e x))

;; meander 1 : maybe you are worried about something

(if (and (fearThat' e1 x e2)
	 (etc1_meander 0.3 e1 e x e2))
    (meander' e x))

;; meander 2: Maybe you are bored

(if (and (bored' e1 x)
	 (etc2_meander 0.3 e1 e x))
    (meander' e x))

;; moveTo

(if (etc0_moveTo 0.01 e x l) (moveTo' e x l))

;; moveTo 1 (corner): maybe you are feeling sad. Corner is a sad place

(if (and (unhappy' e1 x)
	 (etc1_moveTo 0.5 e1 e x))
    (moveTo' e x CORNER))

;; moveTo 2 (behindbox): maybe you are hiding

(if (and (hiding' e1 x)
	 (etc2_moveTo 0.8 e1 e x))
    (moveTo' e x BEHINDBOX))


;; nod

(if (etc0_nod 0.01 e x) (nod' e x))

;; nod 1: Maybe you agree with someone you are talking to

(if (and (talkTo' e1 x y)
	 (agree' e2 x y)
	 (etc1_nod 0.1 e1 e2 e x y))
    (nod' e x))

;; nod 2: Maybe you agree with someone

(if (and (agree' e1 x y)
	 (etc2_nod 0.1 e1 e x y))
    (nod' e x))

;; not

(if (etc0_not 1.0 e1 e2) (not' e1 e2))

;; open

(if (etc0_open 0.05 e x d) (open' e x d)) ;; reduced from 0.1

;; open 1: maybe because you don't know who knocked

;(if (and (knock' e1 y d)
;	 (know' e2 x e1)
;	 (not' e3 e2)
;	 (etc1_open 0.9 e1 e2 e3 x y d))
;    (open' e x d))

(if (and (knock' e1 y d)
	 (know' e2 x e1)
	 (not' e3 e2)
	 (inside' e4 x)
	 (etc1_open 0.9 e1 e2 e3 e4 e x y d))
    (open' e x d))

;; open 2: maybe you are opening it for someone else

(if (and (polite' e1 x)
	 (etc2_open 0.11 e1 e x d))
    (open' e x d))

;; outside

(if (etc0_outside 0.01 e x) (outside' e x))


;; par

(if (etc0_par2 1.0 e0 e1 e2) (par' e0 e1 e2))

(if (etc0_par3 1.0 e0 e1 e2 e3) (par' e0 e1 e2 e3))

(if (etc0_par4 1.0 e0 e1 e2 e3 e4) (par' e0 e1 e2 e3 e4))

(if (etc0_par5 1.0 e0 e1 e2 e3 e4 e5) (par' e0 e1 e2 e3 e4 e5))

(if (etc0_par6 1.0 e0 e1 e2 e3 e4 e5 e6) (par' e0 e1 e2 e3 e4 e5 e6))

(if (etc0_par7 1.0 e0 e1 e2 e3 e4 e5 e6 e7) (par' e0 e1 e2 e3 e4 e5 e6 e7))

;; parent

(if (etc0_parent 0.2 e x y) (parent' e x y))

;; playWith

(if (etc0_playWith 0.01 e x y) (playWith' e x y))

;; playWith 1 : Maybe you are both happy

(if (and (happy' e1 x)
	 (happy' e2 y)
	 (etc1_playWith 0.1 e1 e2 e x y))
    (playWith' e x y))

;; poke

(if (etc0_poke 0.01 e x y) (poke' e x y))

;; poke 1 : maybe playing tag

(if (and (playWith' e1 x y)
	 (etc1_poke 0.6 e1 e x y))
    (poke' e x y))

;; poke 2: maybe you want them to see you
(if (and (goal' e1 e2 x)
	 (see' e2 y x)
	 (etc2_poke 0.1 e1 e2 e x y))
    (poke' e x y))

;; poke 3: maybe your goal is to annoy
(if (and (goal' e1 e2 x)
	 (annoy' e2 x y)
	 (etc3_poke 0.1 e1 e2 e x y))
    (poke' e x y))

;; poke 4: maybe to wake them up

(if (and (goal' e1 e2 x)
	 (wakeUp' e2 y)
	 (asleep' e3 y)
	 (etc4_poke 0.9 e1 e2 e3 e x y))
    (poke' e x y))

;; poke 5: maybe to wake them up (2-character wakeup)

(if (and (goal' e1 e2 x)
	 (wakeUp' e2 x y)
	 (asleep' e3 y)
	 (etc5_poke 0.9 e1 e2 e3 e x y))
    (poke' e x y))

;; poke 6: maybe to get involved in an argument (Q80)
;; Explodes.
;(if (and (argueWith' e1 y z)
;	 (goal' e2 e3 x)
;	 (argueWith' e3 x z)
;	 (etc6_poke 0.1 e1 e2 e3 x y z))
;    (poke' e x y))

;; polite

(if (etc0_polite 0.1 e x) (polite' e x))

;; possess

(if (etc0_possess 0.1 e x y) (possess' e x y))

;; prevent

(if (etc0_prevent 0.1 e1 x e2) (prevent' e1 x e2))

;; pull

(if (etc0_pull 0.01 e x y) (pull' e x y))

;; pull 1: maybe your goal is to prevent them from doing something

(if (and (goal' e1 e2 x)
	 (prevent' e2 x e3)
	 (goal' e4 e3 y)
	 (etc1_pull 0.9 e1 e2 e3 e4 e x y))
    (pull' e x y))

;; pull 2: maybe your goal is to discipline

(if (and (goal' e1 e2 x)
	 (discipline' e2 x y)
	 (etc2_pull 0.8 e1 e2 e x y))
    (pull' e x y))

;; push

(if (etc0_push 0.01 e x y) (push' e x y))

;; push 1: maybe your goal is to attack

(if (and (goal' e1 e2 x)
	 (attack' e2 x y)
	 (etc1_push 0.1 e1 e2 e x y))
    (push' e x y))

;; push 2: maybe to breakup an argument

(if (and (argueWith' e1 y z)
	 (goal' e2 e3 x)
	 (prevent' e3 x e1)
	 (etc2_push 0.5 e1 e2 e3 e x y z))
    (push' e x y))

;; push 3: maybe you are a bully

(if (and (bully' e1 x y)
	 (etc3_push 0.1 e1 e x y))
    (push' e x y))

;; push 4: maybe you are trying to rob them (#90)

(if (and (goal' e1 e2 x)
	 (rob' e2 x y)
	 (etc4_push 0.2 e1 e2 e x y))
    (push' e x y))

;; push 5: maybe to breakup a fight

;;(if (and (fight' e1 y z)
;;	 (goal' e2 e3 x)
;;	 (prevent' e3 x e1)
;;	 (etc5_push 0.5 e1 e2 e3 x y z))
;;    (push' e x y))

;; push 6: maybe you are trying to stop them from arguing (with someone)
;; weird, I know. For Q80
(if (and (goal' e1 e2 x)
	 (not' e2 e3)
	 (argueWith' e3 y z)
	 (etc6_push 0.1 e1 e2 e3 e x y z))
    (push' e x y))



;; quickly

(if (etc0_quickly 0.1 e1 e2) (quickly' e1 e2))

;; reject

(if (etc0_reject 0.1 e x y) (reject' e x y))

;; relaxed

(if (etc0_relaxed 0.1 e x) (relaxed' e x))

;; relief

(if (etc0_relief 0.1 e1 x e2) (relief' e1 x e2))

;; relief 1: maybe you were attacked
(if (and (attack' e1 y x)
	 (etc1_relief 0.11 e1 e2 e3 x y))
    (relief' e2 x e3))

;; relief 2: maybe someone prevented something
(if (and (prevent' e1 y e2)
	 (etc2_relief 0.1 e1 e2 e x y))
    (relief' e x e2))

;; relief 3: maybe you won a fight
(if (and (fight' e1 x y)
	 (etc3_relief 0.2 e1 e2 e x y))
    (relief' e x e2))

;; roam

(if (etc0_roam 0.01 e x) (roam' e x))

;; roam 1 : Maybe you are looking for something

(if (and (knowledgeGoal' e1 e2 x)
	 (atLoc' e2 y z)
	 (etc1_roam 0.8 e1 e2 e x y z))
    (roam' e x))

;; rob

(if (etc0_rob 0.05 e x y) (rob' e x y))

;; rob 1: because they have something you want

(if (and (possess' e1 y z)
	 (goal' e2 e3 x)
	 (possess' e3 x z)
	 (etc1_rob 0.9 e1 e2 e3 e x y z))
    (rob' e x y))

;; run

(if (etc0_run 0.01 e x) (run' e x))

;; run 1: maybe you are excited

(if (and (excited' e1 x)
	 (etc1_run 0.1 e1 e x))
    (run' e x))

;; run 2: maybe you are energized

(if (and (energized' e1 x)
	 (etc2_run 0.15 e1 e x))
    (run' e x))

;; scratch

(if (etc0_scratch 0.01 e x y) (scratch' e x y))

;; see

(if (etc0_see 0.1 e x y) (see' e x y))

;; see 1: maybe because they are approaching

(if (and (approach' e1 x y)
	 (etc1_see 0.75 e1 e x y))
    (see' e y x))

;; see 2 : maybe it was an enter and you are inside

(if (and (inside' e1 x)
	 (enter' e2 y)
	 (etc2_see 0.75 e1 e2 e x y))
    (see' e x e2))

;; see 3 : maybe you opened the door and they are outide

(if (and (open' e1 x d)
	 (outside' e2 y)
	 (etc3_see 0.5 e1 e2 e x y d))
    (see' e x y))


;; seq

(if (etc0_seq2 1.0 e1 e2) (seq e1 e2))

(if (etc0_seq3 1.0 e1 e2 e3) (seq e1 e2 e3))

(if (etc0_seq4 1.0 e1 e2 e3 e4) (seq e1 e2 e3 e4))

(if (etc0_seq5 1.0 e1 e2 e3 e4 e5) (seq e1 e2 e3 e4 e5))

(if (etc0_seq6 1.0 e1 e2 e3 e4 e5 e6) (seq e1 e2 e3 e4 e5 e6))

;; shake

(if (etc0_shake 0.01 e x) (shake' e x))

;; shake 1: maybe you are afraid
(if (and (afraid' e1 x)
	 (etc1_shake 0.9 e1 e x))
    (shake' e x))

;; shake 2: maybe you are trying to defend yourself
(if (and (goal' e1 e2 x)
	 (defend' e2 x x)
	 (etc2_shake 0.4 e1 e2 e3 e x x))
    (shake' e x))

;; shake 3: maybe you are cold

(if (and (cold' e1 x)
	 (etc3_shake 0.5 e1 e x))
    (shake' e x))

;; sibling -1
(if (etc0_sibling 0.01 e x y) (sibling' e x y))

;; sleepy -1 

(if (etc0_sleepy 0.01 e x) (sleepy' e x))

;; startle

(if (etc0_startle 0.1 e x y) (startle' e x y))

;; startle 1: maybe you see something
(if (and (see' e1 x y) 
	 (etc1_startle 0.6 e1 e x y))
    (startle' e y x))

;; startle 2: maybe you scratched someone

(if (and (scratch' e1 x y)
	 (etc2_startle 0.3 e1 e x y))
    (startle' e x y))

;; stranger -1
(if (etc0_stranger 0.01 e x y) (stranger' e x y))

;; stroll

(if (etc0_stroll 0.01 e x) (stroll' e x))

;; stroll 1: maybe because you are relaxed

(if (and (relaxed' e1 x)
	 (etc1_stroll 0.1 e1 e x))
    (stroll' e x))

;; surprise

(if (etc0_surprise 0.01 e1 e2 x) (surprise' e1 e2 x))

;; surprise 1: maybe you see someone you didn't expect

(if (and (see' e1 x e2)
	 (unexpect' e3 e2 x)
	 (etc1_surprise 0.9 e1 e2 e3 e x))
    (surprise' e e2 x))

;; talkTo

(if (etc0_talkTo 0.05 e x y) (talkTo' e x y))

;; talkTo 1 : maybe you are friends

(if (and (friend' e1 x y)
	 (etc1_talkTo 0.1 e1 e x y))
    (talkTo' e x y))

;; talkTo 2 : maybe they are talking to you as well

(if (and (talkTo' e1 y x)
	 (etc2_talkTo 0.8 e1 e x y))
    (talkTo' e x y))

;; threat0

(if (etc0_threat0 0.1 e x y) (threat0' e x y))

;; tickle

(if (etc0_tickle 0.01 e x y) (tickle' e x y))

;; tickle 1 : maybe you are a parent

(if (and (parent' e1 x y)
	 (etc1_tickle 0.1 e1 e x y))
    (tickle' e x y))

;; tickle 2: maybe you want them to be happy

(if (and (goal' e1 e2 x)
	 (happy' e2 y)
	 (etc2_tickle 0.1 e1 e2 e x y))
    (tickle' e x y))

;; tickle 3: maybe you are happy yourself

(if (and (happy' e1 x)
	 (etc3_tickle 0.1 e1 e x y))
    (tickle' e x y))

;; tired -1

(if (etc0_tired 0.01 e x) (tired' e x))

;; turn

(if (etc0_turn 0.01 e x) (turn' e x))

;; turn 1: maybe you are surprised

(if (and (surprise' e1 e2 x)
	 (etc1_turn 0.1 e1 e2 e x))
    (turn' e x))

;; turn 2: maybe to see something you hear

(if (and (goal' e1 e2 x)
	 (see' e2 x e3)
	 (hear' e4 x e5)
	 (etc2_turn 0.6 e1 e2 e3 e4 e5 e x))
    (turn' e x))

;; turn 3: maybe to reject a kiss

(if (and (kiss' e1 y x)
	 (reject' e2 x y)
	 (etc3_turn 0.9 e1 e2 e x y))
    (turn' e x))

;; turn 4: maybe someone poked you

(if (and (poke' e1 y x)
	 (etc4_turn 0.1 e1 e x y))
    (turn' e x))

;; turn 5: maybe to look away from someone annoying

(if (and (annoy' e1 y x)
	 (etc5_turn 0.2 e1 e x y))
    (turn' e x))

;; turn 6: maybe you are going out and forgot something

(if (and (exit' e1 x)
	 (forgotToDo' e2 x e3)
	 (atLoc' e4 e3 INSIDE)
	 (enter' e5 x)
	 (etc6_turn 0.9 e1 e2 e3 e4 e5 e x))
    (turn' e x))

;; unexpect

(if (etc0_unexpect 0.75 e1 e2 x) (unexpect' e1 e2 x))

;; unhappy

(if (etc0_unhappy 0.1 e x) (unhappy' e x))

;; unhappy 1: maybe someone was arguing with you

(if (and (argueWith' e1 x y)
	 (etc1_unhappy 0.2 e1 e x y))
    (unhappy' e y))

;; waitFor

(if (etc0_waitFor 0.1 e1 x e2) (waitFor' e1 x e2))

;; wakeUp

(if (etc0_wakeUp 0.1 e x) (wakeUp' e x))

;; wakeup (2-args) -1

(if (etc0b_wakeUp 0.01 e x y) (wakeUp' e x y))

;; wave

(if (etc0_wave 0.01 e x) (wave' e x))

;; wave 1: maybe you see someone you like

(if (and (see' e1 x y)
	 (like' e2 x y)
	 (etc1_wave 0.5 e1 e2 e x y))
    (wave' e x))

;; wave 2: maybe you are expressing goodbye

(if (and (goodbye' e1 x y)
	 (etc2_wave 0.1 e1 e x y))
    (wave' e x))

;; wave 3: maybe you are expressing goodbye back to someone

(if (and (goodbye' e1 x y)
	 (etc3_wave 0.1 e1 e x y))
    (wave' e y))


