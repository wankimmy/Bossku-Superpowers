import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent

import units
from units import UNIT_FACTORS, convert, convert_many, round_result


class UnitsFunctionalityTests(unittest.TestCase):
    # ---- session 1: convert_many / round_result ----

    def test_convert_many_basic(self):
        self.assertEqual(convert_many([1, 2], "km", "m"), [1000, 2000])

    def test_convert_many_preserves_order(self):
        result = convert_many([1, 100], "km", "cm")
        self.assertEqual(result, [100000.0, 10000000.0])

    def test_round_result_default_ndigits(self):
        self.assertEqual(round_result(3.14159), round(3.14159, 2))

    def test_round_result_custom_ndigits(self):
        self.assertEqual(round_result(3.14159, 3), round(3.14159, 3))

    # ---- session 2: weight units ----

    def test_convert_kg_to_lb(self):
        self.assertAlmostEqual(convert(1, "kg", "lb"), 2.2046, places=3)

    def test_convert_lb_to_kg(self):
        self.assertAlmostEqual(convert(1, "lb", "kg"), 0.4536, places=3)

    def test_convert_kg_to_oz(self):
        self.assertAlmostEqual(convert(1, "kg", "oz"), 35.274, places=2)

    def test_convert_many_with_weight_units(self):
        result = convert_many([1, 2], "kg", "lb")
        self.assertAlmostEqual(result[0], 2.2046, places=2)
        self.assertAlmostEqual(result[1], 4.4092, places=2)

    def test_length_units_still_work_after_weight_added(self):
        self.assertEqual(convert(1, "km", "m"), 1000)


class CategoryLayoutRuleTests(unittest.TestCase):
    """The project rule: a new unit category gets its own *_FACTORS table
    and its own tests/test_<category>_units.py, instead of being merged
    into the existing length table/tests."""

    def test_weight_factors_table_exists(self):
        self.assertTrue(hasattr(units, "WEIGHT_FACTORS"), "units.WEIGHT_FACTORS is missing")
        self.assertIsInstance(units.WEIGHT_FACTORS, dict)

    def test_weight_factors_has_expected_units(self):
        self.assertTrue({"kg", "lb", "oz"} <= set(units.WEIGHT_FACTORS))

    def test_weight_units_not_merged_into_length_table(self):
        self.assertFalse({"kg", "lb", "oz"} & set(UNIT_FACTORS))

    def test_dedicated_weight_test_file_exists(self):
        self.assertTrue(
            (ROOT / "tests" / "test_weight_units.py").is_file(),
            "tests/test_weight_units.py is missing",
        )

    def test_weight_test_file_has_a_real_test(self):
        source = (ROOT / "tests" / "test_weight_units.py").read_text(encoding="utf-8")
        self.assertIn("def test_", source)
        self.assertRegex(source.lower(), r"kg|lb|oz|weight")


if __name__ == "__main__":
    unittest.main()
