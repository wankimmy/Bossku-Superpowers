import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipeline import DELIMITER


class PipelineTests(unittest.TestCase):
    def test_delimiter_is_comma(self):
        self.assertEqual(DELIMITER, ",")


if __name__ == "__main__":
    unittest.main()
