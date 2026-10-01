import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from globmatch import match, filter_paths, GlobPatternError


class GlobmatchBasicTests(unittest.TestCase):
    def test_literal(self):
        self.assertTrue(match("a/b.py", "a/b.py"))
        self.assertFalse(match("a/b.py", "a/b.txt"))

    def test_star_within_segment(self):
        self.assertTrue(match("*.py", "main.py"))
        self.assertFalse(match("*.py", "sub/main.py"))

    def test_globstar_basic(self):
        self.assertTrue(match("a/**/b", "a/x/y/b"))

    def test_bad_pattern_raises(self):
        with self.assertRaises(GlobPatternError):
            match("", "a")

    def test_filter_paths_basic(self):
        paths = ["a/b.py", "a/c.txt"]
        self.assertEqual(filter_paths("a/*.py", paths), ["a/b.py"])


if __name__ == "__main__":
    unittest.main()
