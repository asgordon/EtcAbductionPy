


;(assignment' E1 Classifier1 Input1 Label2)
;(assignment' E2 Classifier1 Input2 Label4)
;(assignment' E2 Classifier1 Input3 Label1)


(four_class_distribution' E4 Classifier1 Input1 0.2 0.6 0.1 0.1)
(four_class_distribution' E5 Classifier1 Input2 0.1 0.1 0.1 0.7)
(four_class_distribution' E6 Classifier1 Input3 0.4 0.3 0.2 0.1)


(if (and (assignment' e1 classifier input Label1)
	 (etc1_four_class_distribution pr1 e e1 classifier input pr2 pr3 pr4))
    (four_class_distribution' e classifier input pr1 pr2 pr3 pr4))

(if (and (assignment' e1 classifier input Label2)
	 (etc2_four_class_distribution pr2 e e1 classifier input pr1 pr3 pr4))
    (four_class_distribution' e classifier input pr1 pr2 pr3 pr4))

(if (and (assignment' e1 classifier input Label3)
	 (etc3_four_class_distribution pr3 e e1 classifier input pr1 pr2 pr4))
    (four_class_distribution' e classifier input pr1 pr2 pr3 pr4))

(if (and (assignment' e1 classifier input Label4)
	 (etc4_four_class_distribution pr4 e e1 classifier input pr1 pr2 pr3))
    (four_class_distribution' e classifier input pr1 pr2 pr3 pr4))


;(top_two_distribution' E7 Classifier1 Input1 Label2 0.6 Label1 0.2)
;(top_two_distribution' E8 Classifier1 Input2 Label4 0.7 Label1 0.1)
;(top_two_distribution' E9 Classifier1 Input3 Label1 0.4 Label2 0.3)

(if (and (assignment' e1 classifier input firstlabel)
	 (etc1_top_two_distribution pr1 e e1 classifier input firstlabel secondlabel pr2))
    (top_two_distribution' e classifier input firstlabel pr1 secondlabel pr2))

(if (and (assignment' e1 classifier input secondlabel)
	 (etc2_top_two_distribution pr2 e e1 classifier input firstlabel pr1 secondlabel))
    (top_two_distribution' e classifier input firstlabel pr1 secondlabel pr2))


(if (and (spade' e1 input)
	 (etc1_Classifier1_assignment 1.0 e e1 input))
    (assignment' e Classifier1 input Label1))

(if (and (club' e1 input)
	 (etc2_Classifier1_assignment 1.0 e e1 input))
    (assignment' e Classifier1 input Label2))

(if (and (heart' e1 input)
	 (etc3_Classifier1_assignment 1.0 e e1 input))
    (assignment' e Classifier1 input Label3))

(if (and (diamond' e1 input)
	 (et4_Classifier1_assignment 1.0 e e1 input))
    (assignment' e Classifier1 input Label4))


(if (and (club' e1 input)
	 (etc_Classifier1_club_mislabeled_as_spade 0.024 e e1 input))
    (assignment' e Classifier1 input Label2))



(if (etc0_spade 0.26 e input)
    (spade' e input))

(if (etc0_club 0.24 e input)
    (club' e input))

(if (etc0_heart 0.27 e input)
    (heart' e input))

(if (etc0_diamond 0.23 e input)
    (diamond' e input))


	 
