import json

from benchmark.paths import QUESTIONS_JSON


def test_questions_are_fixed_at_fifty():
    questions = json.loads(QUESTIONS_JSON.read_text(encoding="utf-8"))
    assert len(questions) == 50
    assert len({item["id"] for item in questions}) == 50
    assert all(item["question"].endswith("?") for item in questions)

