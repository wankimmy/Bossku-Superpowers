import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from currency import is_supported_currency


class CurrencyTests(unittest.TestCase):
    def test_supported(self):
        self.assertTrue(is_supported_currency("USD"))

    def test_unsupported(self):
        self.assertFalse(is_supported_currency("XXX"))


if __name__ == "__main__":
    unittest.main()
