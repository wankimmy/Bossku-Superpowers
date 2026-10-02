"""Tests for converting between weight units (kg, lb, oz)."""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from units import WEIGHT_FACTORS, convert


class WeightUnitsTests(unittest.TestCase):
    def test_kg_to_lb(self):
        self.assertAlmostEqual(convert(1, "kg", "lb"), 2.2046, places=3)

    def test_lb_to_kg(self):
        self.assertAlmostEqual(convert(1, "lb", "kg"), 0.4536, places=3)

    def test_weight_factors_has_expected_units(self):
        self.assertTrue({"kg", "lb", "oz"} <= set(WEIGHT_FACTORS))


if __name__ == "__main__":
    unittest.main()
