import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from checker import check_strength


class CheckerTests(unittest.TestCase):
    def test_strong_password_scores_five(self):
        score, reasons = check_strength("Abcdef1234!@")
        self.assertEqual(score, 5)
        self.assertEqual(reasons, [])

    def test_too_short_password(self):
        score, reasons = check_strength("Ab1!")
        self.assertIn("too short (needs at least 12 characters)", reasons)

    def test_whitespace_password_scores_zero(self):
        score, reasons = check_strength("has a space 123!")
        self.assertEqual(score, 0)
        self.assertEqual(reasons, ["passwords may not contain whitespace"])

    def test_non_string_raises(self):
        with self.assertRaises(TypeError):
            check_strength(None)


if __name__ == "__main__":
    unittest.main()
