import os
import sys
import unittest
from dataclasses import FrozenInstanceError
from decimal import Decimal

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import errors
import rubric


class ScoreQuestionTests(unittest.TestCase):
    """Shows the style this project expects: frozen dataclasses built
    directly, and errors checked against the shared base class rather
    than a bare builtin exception."""

    def setUp(self):
        self.question = rubric.Question(id="q1", max_points=Decimal("10"), category="homework")

    def test_full_credit_is_100_percent(self):
        self.assertEqual(
            rubric.score_question(self.question, Decimal("10")), Decimal("100")
        )

    def test_zero_credit_is_0_percent(self):
        self.assertEqual(
            rubric.score_question(self.question, Decimal("0")), Decimal("0")
        )

    def test_partial_credit_is_unrounded(self):
        q = rubric.Question(id="q2", max_points=Decimal("3"), category="homework")
        result = rubric.score_question(q, Decimal("1"))
        self.assertGreater(result, Decimal("33.33"))
        self.assertLess(result, Decimal("33.34"))

    def test_points_earned_above_max_raises(self):
        with self.assertRaises(errors.GradebookError):
            rubric.score_question(self.question, Decimal("11"))

    def test_question_is_frozen(self):
        with self.assertRaises(FrozenInstanceError):
            self.question.max_points = Decimal("5")


if __name__ == "__main__":
    unittest.main()
