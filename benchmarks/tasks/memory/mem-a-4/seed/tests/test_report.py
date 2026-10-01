import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import legacy_format


class LegacyFormatBasicTests(unittest.TestCase):
    def test_parse_line_basic(self):
        row = legacy_format.parse_line("Widget|3|199")
        self.assertEqual(row, {"name": "Widget", "qty": 3, "price_cents": 199})


if __name__ == "__main__":
    unittest.main()
