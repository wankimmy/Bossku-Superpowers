import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from units import convert


class UnitsTests(unittest.TestCase):
    def test_km_to_m(self):
        self.assertEqual(convert(1, "km", "m"), 1000)

    def test_cm_to_m(self):
        self.assertEqual(convert(100, "cm", "m"), 1.0)


if __name__ == "__main__":
    unittest.main()
