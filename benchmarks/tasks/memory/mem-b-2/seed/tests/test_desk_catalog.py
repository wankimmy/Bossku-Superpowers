import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from desk_catalog import is_known_desk_id


class DeskCatalogTests(unittest.TestCase):
    def test_known_desk(self):
        self.assertTrue(is_known_desk_id("A1"))

    def test_unknown_desk(self):
        self.assertFalse(is_known_desk_id("Z9"))


if __name__ == "__main__":
    unittest.main()
