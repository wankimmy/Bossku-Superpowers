import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from httpheader import split_list, parse_params, parse_quality_list, HeaderParseError


class HttpHeaderBasicTests(unittest.TestCase):
    def test_split_list_basic(self):
        self.assertEqual(split_list("a, b, c"), ["a", "b", "c"])

    def test_parse_params_basic(self):
        self.assertEqual(parse_params("text/html; charset=utf-8"), ("text/html", [("charset", "utf-8")]))

    def test_parse_quality_list_basic(self):
        self.assertEqual(parse_quality_list("en;q=0.8,fr;q=0.9"), [("fr", 0.9), ("en", 0.8)])

    def test_malformed_raises(self):
        with self.assertRaises(HeaderParseError):
            parse_params("")


if __name__ == "__main__":
    unittest.main()
