import unittest

from campusflow.understanding_check import QUESTION_BANK, parse_choice, score_answers


class TestUnderstandingCheck(unittest.TestCase):
    def test_parse_choice_rejects_invalid_values(self):
        self.assertEqual(parse_choice("b"), "B")
        self.assertEqual(parse_choice("  c  "), "C")
        self.assertIsNone(parse_choice("E"))
        self.assertIsNone(parse_choice(""))

    def test_score_answers_uses_first_submission_for_each_question(self):
        answers = [
            "B",
            "C",
            "B",
            "C",
            "C",
            "B",
        ]
        self.assertEqual(score_answers(QUESTION_BANK, answers), 6)

        answers_with_duplicates = ["A", "B", "C", "D", "C", "B", "A"]
        self.assertEqual(score_answers(QUESTION_BANK, answers_with_duplicates), 2)


if __name__ == "__main__":
    unittest.main()
