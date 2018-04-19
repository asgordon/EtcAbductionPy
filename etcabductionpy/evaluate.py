# eval.py
# Andrew S. Gordon

import abduction
import unify

def evaluate(solution, gold): # simpler, faster, permissive
    '''Calculates precision, recall, and f1 score of solution given gold-standard literals'''
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
            if unify.unify(sliteral, gliteral) != None:
                unifiableInSolution += 1.0
                break;
    for gliteral in gold:
        for sliteral in solution:
            if unify.unify(sliteral, gliteral) != None:
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

    
