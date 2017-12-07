# eval.py
# October 23, 2017
# Calculates precision, recall, and f1 score of solution given gold-standard literals

import abduction
import unify

def evaluate(solution, gold):
    #return evalute1(solution, gold)
    return evaluate2(solution, gold)

def evaluate1(solution, gold):
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

def evaluate2(solution, gold): # simpler, faster, permissive
    if len(solution) == 0:
        raise ValueError('The solution is zero-length')
    if len(gold) == 0:
        raise ValueError('The gold is zero-length')
    goldcount = float(len(gold))
    solutioncount = float(len(solution))
    unifiableInGold = 0.0
    unifiableInSolution = 0.0
    for sliteral in solution:
        for gliteral in gold:
            if unify.unify(sliteral, gliteral):
                unifiableInSolution += 1.0
                break;
    for gliteral in gold:
        for sliteral in solution:
            if unify.unify(sliteral, gliteral):
                unifiableInGold += 1.0
                break;

    # precision is unifiable in solution / solution count
    precision = unifiableInSolution / solutioncount
    # recall is unifiable in gold / gold count
    recall = unifiableInGold / goldcount
    # f1 is harmonic mean
    f1 = 2.0 * (precision * recall) / (precision + recall)
    print("goldcount", goldcount,
          "solutioncount", solutioncount,
          "unifiableInSolution", unifiableInSolution,
          "unifiableInGold", unifiableInGold,
          "precision", precision,
          "recall", recall,
          "f1", f1)

    return(precision, recall, f1)

    
