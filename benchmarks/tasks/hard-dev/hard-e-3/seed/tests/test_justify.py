import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from justify import justify_paragraph, justify_text, JustifyError


class JustifyBasicTests(unittest.TestCase):
    def test_single_line_fits(self):
        self.assertEqual(justify_paragraph("ab cd", 5), ["ab cd"])

    def test_empty_paragraph(self):
        self.assertEqual(justify_paragraph("", 10), [])

    def test_width_must_be_positive(self):
        with self.assertRaises(JustifyError):
            justify_paragraph("abc", 0)

    def test_justify_text_empty(self):
        self.assertEqual(justify_text("", 10), "")

    def test_justify_text_basic(self):
        out = justify_text("one two three", 20)
        self.assertIsInstance(out, str)


if __name__ == "__main__":
    unittest.main()
