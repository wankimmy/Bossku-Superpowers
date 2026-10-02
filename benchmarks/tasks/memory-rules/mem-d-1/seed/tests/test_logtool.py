import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logtool import LEVELS


class LogToolTests(unittest.TestCase):
    def test_levels_defined(self):
        self.assertEqual(LEVELS, ("DEBUG", "INFO", "WARN", "ERROR"))


if __name__ == "__main__":
    unittest.main()
