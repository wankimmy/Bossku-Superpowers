import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sessions import DEFAULT_TIMEOUT_MINUTES


class SessionsBasicTests(unittest.TestCase):
    def test_default_timeout_is_positive(self):
        self.assertGreater(DEFAULT_TIMEOUT_MINUTES, 0)


if __name__ == "__main__":
    unittest.main()
