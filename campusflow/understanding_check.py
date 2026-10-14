QUESTION_BANK = [
    {
        "prompt": "An open ticket with no assignee tries to move to in_progress.",
        "options": {
            "A": "Accept",
            "B": "Reject and preserve all data",
            "C": "Resolve it automatically",
            "D": "Remove ticket",
        },
        "correct": "B",
    },
    {
        "prompt": "A zero-ticket report should show resolution percent as:",
        "options": {
            "A": "Crash",
            "B": "100%",
            "C": "0%",
            "D": "Divide by one without explanation",
        },
        "correct": "C",
    },
    {
        "prompt": "A search with title='wifi', category='Network', status='open' should match:",
        "options": {
            "A": "Any record matching one filter",
            "B": "Only records matching all supplied filters",
            "C": "All network records",
            "D": "All open records",
        },
        "correct": "B",
    },
    {
        "prompt": "A note added to a resolved ticket should:",
        "options": {
            "A": "Append anyway",
            "B": "Delete old notes",
            "C": "Reject until reopened",
            "D": "Change status silently",
        },
        "correct": "C",
    },
    {
        "prompt": "A JSON file with two tickets sharing the same ID should:",
        "options": {
            "A": "Keep both",
            "B": "Replace memory with duplicates",
            "C": "Reject the load without changing current memory",
            "D": "Rename IDs silently",
        },
        "correct": "C",
    },
    {
        "prompt": "A PR changes validation but has no negative tests. Best response:",
        "options": {
            "A": "Approve because it runs",
            "B": "Request focused tests and reasoning",
            "C": "Merge immediately",
            "D": "Ask AI to approve it",
        },
        "correct": "B",
    },
]


def parse_choice(raw):
    if raw is None:
        return None
    normalized = str(raw).strip()
    if not normalized:
        return None
    value = normalized.upper()
    if value in {"A", "B", "C", "D"}:
        return value
    return None


def score_answers(bank, answers):
    if bank is None:
        return 0

    if isinstance(answers, dict):
        ordered = {}
        for question_index, answer in answers.items():
            ordered[int(question_index)] = answer
    elif isinstance(answers, (list, tuple)):
        ordered = {}
        for index, answer in enumerate(answers):
            if index not in ordered:
                ordered[index] = answer
    else:
        ordered = {}

    score = 0
    for index, question in enumerate(bank):
        submitted = ordered.get(index)
        if submitted is None:
            continue
        if parse_choice(submitted) == question["correct"]:
            score += 1
    return score


def run_check(bank, input_fn, output_fn, notes_path):
    answers = {}
    for index, question in enumerate(bank):
        while True:
            output_fn(f"\nQ{index + 1}: {question['prompt']}")
            for choice, text in question['options'].items():
                output_fn(f"  {choice}. {text}")
            raw = input_fn("Choose A-D: ")
            choice = parse_choice(raw)
            if choice is None:
                output_fn("Please enter a valid choice: A, B, C, or D.")
                continue
            answers[index] = choice
            break

    score = score_answers(bank, answers)
    output_fn(f"\nFinal score: {score}/{len(bank)}")

    explanations = []
    for index in range(min(2, len(bank))):
        question = bank[index]
        explanation = input_fn(f"Brief explanation for Q{index + 1}: ")
        cleaned = explanation.strip()
        if not cleaned:
            cleaned = "No explanation provided."
        explanations.append(f"Q{index + 1}: {cleaned}")

    if notes_path:
        with open(notes_path, "a", encoding="utf-8") as handle:
            for line in explanations:
                handle.write(line + "\n")

    return score
