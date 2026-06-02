'''
learning.py
a learning algorithm for probability-ordere logical abduction
Andrew S. Gordon'''

import etcabductionpy as etc
import tricopa as tc
import signal

print(f"{len(tc.questions)} questions, {len(tc.default_kb)} clauses")

LOWER_BOUND = 0.001
UPPER_BOUND = 0.999

def learn(orig_kb: etc.KnowledgeBase, 
          questions: tc.Question, 
          learning_rate: float = 0.05, 
          max_epochs: int = 100,
          maxdepth: int = 3,
          timeout: int = 10) -> etc.KnowledgeBase:
    current_kb = etc.KnowledgeBase(list(orig_kb)) # shallow copy
    current_epoch = 0
    print(f"epoch\tscore\tmods")
    while current_epoch < max_epochs:
        score: float = 0.0
        kb_modifications = 0

        for q in questions:
            acombined = q.given + q.alta
            bcombined = q.given + q.altb
            asolution = best_with_timeout(acombined, current_kb, maxdepth, timeout)
            bsolution = best_with_timeout(bcombined, current_kb, maxdepth, timeout)
            ajlpr = etc.joint_log_probability(asolution)
            bjlpr = etc.joint_log_probability(bsolution)
            if ajlpr > bjlpr and q.answer == 'a':
                score += 1.0 # good job, no change
            elif ajlpr < bjlpr and q.answer == 'b':
                score += 1.0 # good job, no change
            else: # update probabilities in current_kb
                if ajlpr == bjlpr: score += 0.5
                if q.answer == 'a':
                    current_kb, mods = update_kb(current_kb, asolution, bsolution, learning_rate)
                else:
                    current_kb, mods = update_kb(current_kb, bsolution, asolution, learning_rate)
                kb_modifications += mods
        print(f"{current_epoch + 1}\t{score}\t{kb_modifications}")
        if kb_modifications == 0: # no progress
            return current_kb
        current_epoch += 1
    return current_kb

def update_kb(current_kb, correct_solution, incorrect_solution, learning_rate):
    correct_solution = correct_solution or []
    incorrect_solution = incorrect_solution or []
    new_clauses = []
    correct_predicates = [lit.predicate for lit in correct_solution]
    incorrect_predicates = [lit.predicate for lit in incorrect_solution]
    total_modifications = 0
    for current_clause in current_kb:
        new_antecedents = []
        for ant in current_clause.antecedents:
            if ant.predicate in correct_predicates: # increase it!
                new_probablity = ant.probability + learning_rate
                new_probablity = min(new_probablity, UPPER_BOUND)
                new_antecedents.append(etc.EtceteraLiteral(ant.predicate, (etc.Term(new_probablity), *ant.arguments[1:])))
                total_modifications += 1
            elif ant.predicate in incorrect_predicates: # decrease it!
                new_probablity = ant.probability - learning_rate
                new_probablity = max(LOWER_BOUND, new_probablity)
                new_antecedents.append(etc.EtceteraLiteral(ant.predicate, (etc.Term(new_probablity), *ant.arguments[1:])))
                total_modifications += 1
            else: # leave alone
                new_antecedents.append(ant)
        new_clauses.append(etc.DefiniteClause(new_antecedents, current_clause.consequent))
    return(etc.KnowledgeBase(new_clauses), total_modifications)


def timeout_handler(signum, frame):
    raise TimeoutError("timeout")

def best_with_timeout(obs, kb, maxdepth, timeout) -> list[etc.Literal] | None:
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout)
    try:
        best = etc.nbest(obs, kb, maxdepth, n=1)
        if len(best) > 0: 
            best = best[0] 
        else:
            best = None
    except TimeoutError as e:
        best = None
    finally:
        signal.alarm(0)
    return best

def main():
    result_kb: etc.KnowledgeBase = learn(tc.default_kb, tc.questions, learning_rate=0.01, timeout=1)

if __name__ == "__main__":
    main()