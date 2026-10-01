import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipedelim import parse_records, format_records, PipeFormatError


class PipedelimBasicTests(unittest.TestCase):
    def test_parse_basic_grid(self):
        self.assertEqual(parse_records("a|b\nc|d"), [["a", "b"], ["c", "d"]])

    def test_format_basic_grid(self):
        self.assertEqual(format_records([["a", "b"]]), "a|b\n")

    def test_empty_text_is_zero_records(self):
        self.assertEqual(parse_records(""), [])

    def test_invalid_escape_raises(self):
        with self.assertRaises(PipeFormatError):
            parse_records("a\\xb")


if __name__ == "__main__":
    unittest.main()
