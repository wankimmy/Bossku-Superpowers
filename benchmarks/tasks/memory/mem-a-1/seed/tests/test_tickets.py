import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tickets import VALID_STATUSES


class TicketsBasicTests(unittest.TestCase):
    def test_valid_statuses_present(self):
        self.assertIn("open", VALID_STATUSES)
        self.assertEqual(len(VALID_STATUSES), 4)


if __name__ == "__main__":
    unittest.main()
