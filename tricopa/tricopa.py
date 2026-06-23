"""
tricopa.py
Evaluates Etcetera Abduction on the Triangle-COPA benchmark.
"""

import argparse
import signal
import itertools
from pathlib import Path
from typing import Any

import etcabductionpy as etc

# Constants
SCRIPT_DIR = Path(__file__).parent
KB_PATH = SCRIPT_DIR / "tricopa-kb.lisp"
QUESTIONS_PATH = SCRIPT_DIR / "TriCOPA.txt"
ANSWERS_PATH = SCRIPT_DIR / "TriCOPA-answers.txt"
CLOSE_ENOUGH = 1e-6


class Question:
    def __init__(self, number: int, given: list[etc.Literal], alta: list[etc.Literal], altb: list[etc.Literal], answer: str) -> None:
        self.number = number
        self.given = given
        self.alta = alta
        self.altb = altb
        self.answer = answer


def load_questions() -> list[Question]:
    """Load TriCOPA questions and answers."""
    with open(ANSWERS_PATH) as f:
        answers = [line.strip().split("\t")[1] for line in f]

    with open(QUESTIONS_PATH) as f:
        lines = f.readlines()

    questions: list[Question] = []
    for i in range(100):
        base = 3 + i * 7
        _, given = etc.KnowledgeBase.from_src(lines[base + 2])
        _, alta = etc.KnowledgeBase.from_src(lines[base + 4])
        _, altb = etc.KnowledgeBase.from_src(lines[base + 6])
        questions.append(Question(i + 1, given, alta, altb, answers[i]))
    return questions


def load_kb() -> etc.KnowledgeBase:
    """Load the default knowledge base."""
    with open(KB_PATH) as f:
        kb, _ = etc.KnowledgeBase.from_src(f.read())
    return kb


def score_prob(q: Question, kb: etc.KnowledgeBase, depth: int) -> tuple[float, str]:
    """Score using joint log probability of the best solution."""
    sol_a = etc.nbest(q.given + q.alta, kb, depth, 1)
    sol_b = etc.nbest(q.given + q.altb, kb, depth, 1)

    if not sol_a or not sol_b:
        return 0.0, "fail"

    pa = etc.joint_log_probability(sol_a[0])
    pb = etc.joint_log_probability(sol_b[0])

    if abs(pa - pb) < CLOSE_ENOUGH:
        return 0.5, "tie"
    elif (q.answer == 'a' and pa > pb) or (q.answer == 'b' and pb > pa):
        return 1.0, "correct"
    return 0.0, "wrong"


def score_unify(q: Question, kb: etc.KnowledgeBase, depth: int, n: int) -> tuple[float, str]:
    """Score by finding the rank of the first solution that unifies with the target."""
    sols = etc.nbest(q.given, kb, depth, n)
    if not sols:
        return 0.0, "fail"

    rank_a = find_rank(sols, q.alta, kb)
    rank_b = find_rank(sols, q.altb, kb)

    if rank_a is None and rank_b is None:
        return 0.0, "fail"
    
    if rank_a is None:
        return (0.0, "wrong") if q.answer == 'a' else (1.0, "correct")
    if rank_b is None:
        return (0.0, "wrong") if q.answer == 'b' else (1.0, "correct")
        
    if rank_a < rank_b:
        return (1.0, "correct") if q.answer == 'a' else (0.0, "wrong")
    elif rank_b < rank_a:
        return (1.0, "correct") if q.answer == 'b' else (0.0, "wrong")
    return 0.5, "tie"


def find_rank(solutions: list[list[etc.Literal]], targets: list[etc.Literal], kb: etc.KnowledgeBase) -> int | None:
    """Find the rank (1-indexed) of the first solution that unifies with all targets."""
    for i, sol in enumerate(solutions):
        entailed = [e for e, _ in etc.forward(sol, kb)]
        if len(entailed) < len(targets):
            continue
        for combo in itertools.combinations(entailed, len(targets)):
            theta: dict[etc.Term, etc.Term] = {}
            match = True
            for t, e in zip(targets, combo):
                sub = etc.unify(t, e)
                if sub is None:
                    match = False
                    break
                for k, v in sub.items():
                    if k in theta and theta[k] != v:
                        match = False
                        break
                    theta[k] = v
                if not match:
                    break
            if match:
                return i + 1
    return None


def _timeout_handler(signum: int, frame: Any) -> None:
    """Signal handler that raises a TimeoutError."""
    raise TimeoutError("Evaluation timed out")


def main() -> None:
    parser = argparse.ArgumentParser(description="Triangle-COPA Evaluation")
    parser.add_argument("--depth", type=int, default=3, help="Max backchaining depth (default=3)")
    parser.add_argument("--timeout", type=int, default=10, help="Timeout per question in seconds (default=10)")
    parser.add_argument("--verbose", action="store_true", help="Print per-question results")
    parser.add_argument("--nbest", type=int, default=None, help="Use unification scoring with N-best beam")
    args = parser.parse_args()

    kb = load_kb()
    questions = load_questions()

    total_score: float = 0.0
    correct: int = 0
    ties: int = 0
    wrong: int = 0
    timeouts: int = 0
    fails: int = 0

    signal.signal(signal.SIGALRM, _timeout_handler)

    for q in questions:
        # 1. Set the alarm BEFORE calling the function
        signal.alarm(args.timeout)
        
        try:
            # 2. Call the pure function directly (no lambdas)
            if args.nbest is not None:
                score, status = score_unify(q, kb, args.depth, args.nbest)
            else:
                score, status = score_prob(q, kb, args.depth)
            
            # 3. Cancel the alarm on success
            signal.alarm(0)
            
        except TimeoutError:
            # 4. Handle timeout (alarm might still be set, so cancel it)
            signal.alarm(0)
            score = 0.0
            status = "timeout"

        # Aggregate results
        total_score += score
        
        if status == "correct":
            correct += 1
        elif status == "tie":
            ties += 1
        elif status == "wrong":
            wrong += 1
        elif status == "timeout":
            timeouts += 1
        else:
            fails += 1

        if args.verbose:
            print(f"Q{q.number}: ans={q.answer} status={status} score={score}")

    print(f"score={total_score} correct={correct} ties={ties} wrong={wrong} timeouts={timeouts} fails={fails}")


if __name__ == "__main__":
    main()
