# Use etcetera abduction to solve TriCOPA problems
# Andrew S. Gordon October 2025

from pathlib import Path
import etcabductionpy as etc
import signal

# Verify that these required files exist
script_directory = Path(__file__).parent
question_file = script_directory / "TriCOPA.txt"
answer_file = script_directory / "TriCOPA-answers.txt"
default_kb_file = script_directory / "tricopa-kb.lisp"

for required in [question_file, answer_file, default_kb_file]:
    if not required.exists():
        raise RuntimeError(f"Required file not found: {required}")

class Question:
    def __init__(self, number, given_text, question_text, given, alta_text, alta, altb_text, altb, answer):
        self.number = number
        self.given_text = given_text
        self.question_text = question_text
        self.given = given
        self.alta_text = alta_text
        self.alta = alta
        self.altb_text = altb_text
        self.altb = altb
        self.answer = answer


# Load the answers
with open(answer_file) as f:
    answers = []
    lines = f.readlines()
    if len(lines) != 100:
        raise RuntimeError(f"Answer file is not 100 lines!")
    for line in lines:
        parts = line.strip().split("\t")
        if len(parts) != 2:
            raise RuntimeError(f"Answer in answer not formatted correctly: {line.strip()}")
        answers.append(parts[1])

# Load the questions
with open(question_file) as f:
    questions = []
    lines = f.readlines()
    if len(lines) < 703:
        raise RuntimeError(f"Question file is not at least 703 lines long") # 3 header, then 100 * 7
    for index in range(100):
        number = index + 1

        blank_line = lines[3 + (index * 7)]
        if blank_line.strip() != '':
            raise RuntimeError(f"This line in the question file should be blank: {blank_line}")
        
        question_line = lines[3 + (index * 7) + 1]
        question_line_number = question_line.split(".")[0]
        if str(number) != question_line_number:
            raise RuntimeError(f"{str(number)} does not match this line: {question_line}")
        question_text = question_line.split(".")[-1].strip()
        given_text = question_line.split(question_text)[0].split('.', 1)[1].strip()
        
        given_line = lines[3 + (index * 7) + 2]
        _, given = etc.parse(given_line)
        
        alta_text_line = lines[3 + (index * 7) + 3]
        if alta_text_line[:3] != 'a. ':
            raise RuntimeError(f"This alternative is formatted incorrectly: {alta_text_line}")
        alta_text = alta_text_line[3:].strip()

        alta_line = lines[3 + (index * 7) + 4]
        _, alta = etc.parse(alta_line)

        altb_text_line = lines[3 + (index * 7) + 5]
        if altb_text_line[:3] != 'b. ':
            raise RuntimeError(f"This alternative is formatted incorrectly: {altb_text_line}")
        altb_text = altb_text_line[3:].strip()

        altb_line = lines[3 + (index * 7) + 6]
        _, altb = etc.parse(altb_line)

        answer = answers[index]

        questions.append(Question(number, given_text, question_text, given, alta_text, alta, altb_text, altb, answer))


# Load the default knowledgebase
with open(default_kb_file) as f:
    kb_text = f.read()
    default_kb, _ = etc.parse(kb_text)

# score 1 question
def score1q(number, kb, depth):
    if number < 1 or number > 100: 
        raise RuntimeError(f"Question out of range 1-100: {number}")
    question = questions[number - 1]
    # Which is more probable, combined_a or combined_b?
    combined_a = question.given + question.alta
    combined_a_best = etc.nbest(combined_a, kb, depth, 1)[0]
    combined_a_probability = etc.joint_probability(combined_a_best)
    combined_b = question.given + question.altb
    combined_b_best = etc.nbest(combined_b, kb, depth, 1)[0]
    combined_b_probability = etc.joint_probability(combined_b_best)
    if question.answer == 'a' and combined_a_probability > combined_b_probability:
        score = 1.0
    elif question.answer == 'b' and combined_b_probability > combined_a_probability:
        score = 1.0
    elif combined_a_probability == combined_b_probability:
        score = 0.5
    else:
        score = 0.0
    print(f"{number} {question.answer} {combined_a_probability:.15f} {combined_b_probability:.15f} {score}")
    return score

# score all questions
def scoreall(kb, depth):
    score = 0.0
    for q in range(1, 101):
        score += score1q(q, kb, depth)
    return(score)

# score all with timeout
def timeout_handler(signum, frame):
    raise TimeoutError("timeout")

def scoreall2(kb, depth, timeout=10):
    score = 0.0
    correct = 0
    equal = 0
    timeouts = 0
    for q in range(1, 101):
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(timeout)
        try:
            value = score1q(q, kb, depth)
            score += value
            if value == 1: correct += 1
            if value == 0.5: equal += 1
        except TimeoutError as e:
            print(f"{q} {e} 0.5")
            score += 0.5
            timeouts += 1
        finally:
            signal.alarm(0)
    print(f"score={score} correct={correct} equal={equal} timeouts={timeouts}")
    return(score)
    

# go
scoreall2(default_kb, 3) # scores 88.5 with default kb and 10-second timeout # score=88.5 correct=77 equal=16 timeouts=7