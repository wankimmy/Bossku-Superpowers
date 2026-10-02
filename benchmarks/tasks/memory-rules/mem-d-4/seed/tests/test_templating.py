import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from templating import PLACEHOLDER_PATTERN


class TemplatingTests(unittest.TestCase):
    def test_placeholder_pattern_matches_simple_case(self):
        self.assertTrue(re.search(PLACEHOLDER_PATTERN, "hello {{ name }}"))


if __name__ == "__main__":
    unittest.main()
