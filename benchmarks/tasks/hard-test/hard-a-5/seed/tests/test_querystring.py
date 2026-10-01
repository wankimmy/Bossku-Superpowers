import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from querystring import encode_query, decode_query, QueryStringError


class QuerystringBasicTests(unittest.TestCase):
    def test_encode_basic(self):
        self.assertEqual(encode_query([("a", "1"), ("b", "2")]), "a=1&b=2")

    def test_decode_basic(self):
        self.assertEqual(decode_query("a=1&b=2"), [("a", "1"), ("b", "2")])

    def test_encode_empty(self):
        self.assertEqual(encode_query([]), "")

    def test_decode_malformed_percent_raises(self):
        with self.assertRaises(QueryStringError):
            decode_query("k=%2g")


if __name__ == "__main__":
    unittest.main()
