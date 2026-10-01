import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from catalog import is_known_sku


class CatalogTests(unittest.TestCase):
    def test_known_sku(self):
        self.assertTrue(is_known_sku("SKU-1"))

    def test_unknown_sku(self):
        self.assertFalse(is_known_sku("nope"))


if __name__ == "__main__":
    unittest.main()
