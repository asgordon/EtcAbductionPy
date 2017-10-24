# eval.py
# October 23, 2017
# Calculates precision, recall, and f1 score of solution given gold-standard literals

import abduction

def evaluate(solution, gold):
    if len(solution) == 0:
        raise ValueError('The solution is zero-length')
    if len(gold) == 0:
        raise ValueError('The gold is zero-length')
    gold = sorted(abduction.crunch(gold), key = len)[0] # remove duplicates in gold
    combined = sorted(abduction.crunch(gold + solution), key = len)[0] # finds best match
    overlapping = len(solution) + len(gold) - len(combined)
    precision = float(overlapping) / float(len(solution))
    recall = float(overlapping) / float(len(gold))
    f1 = 2.0 * (precision * recall) / (precision + recall)
    return(precision, recall, f1)
    
