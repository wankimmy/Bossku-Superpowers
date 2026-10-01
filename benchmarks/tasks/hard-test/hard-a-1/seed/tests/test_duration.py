import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from duration import parse_duration, format_duration, DurationError


class DurationBasicTests(unittest.TestCase):
    def test_parse_simple_hour(self):
        self.assertEqual(parse_duration("1h"), 3600)

    def test_parse_combo(self):
        self.assertEqual(parse_duration("1h30m"), 5400)

    def test_format_simple(self):
        self.assertEqual(format_duration(3600), "1h")

    def test_format_zero(self):
        self.assertEqual(format_duration(0), "0s")

    def test_empty_string_is_invalid(self):
        with self.assertRaises(DurationError):
            parse_duration("")


if __name__ == "__main__":
    unittest.main()
