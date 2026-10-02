import ast
import unittest
from pathlib import Path

import recipes

ROOT = Path(__file__).resolve().parent
KNOWN_UNITS = ("cup", "tbsp", "tsp", "ml")


def _function_has_raise(module_source, func_name):
    tree = ast.parse(module_source)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == func_name:
            return any(isinstance(n, ast.Raise) for n in ast.walk(node))
    raise AssertionError(f"function {func_name} not found in recipes.py")


class ScaleRecipeFunctionalTests(unittest.TestCase):
    def test_scale_recipe_basic(self):
        result = recipes.scale_recipe([("flour", 2), ("sugar", 1)], 2)
        self.assertEqual(result, [("flour", 4), ("sugar", 2)])

    def test_scale_recipe_does_not_mutate_input(self):
        original = [("flour", 2), ("sugar", 1)]
        recipes.scale_recipe(original, 3)
        self.assertEqual(original, [("flour", 2), ("sugar", 1)])


class ConvertUnitFunctionalTests(unittest.TestCase):
    def test_identity_conversions(self):
        for unit in KNOWN_UNITS:
            result, error = recipes.convert_unit(3, unit, unit)
            self.assertIsNone(error)
            self.assertAlmostEqual(result, 3)

    def test_roundtrip_conversion_preserves_amount(self):
        mid, err1 = recipes.convert_unit(2, "cup", "tbsp")
        self.assertIsNone(err1)
        back, err2 = recipes.convert_unit(mid, "tbsp", "cup")
        self.assertIsNone(err2)
        self.assertAlmostEqual(back, 2, places=6)

    def test_all_known_unit_pairs_succeed(self):
        for a in KNOWN_UNITS:
            for b in KNOWN_UNITS:
                result, error = recipes.convert_unit(5, a, b)
                self.assertIsNone(error, f"{a}->{b} should not error")
                self.assertIsNotNone(result)
                self.assertGreater(result, 0)

    def test_total_volume_ml_matches_sum_of_conversions(self):
        ingredients = [("a", 1, "cup"), ("b", 2, "tbsp"), ("c", 3, "tsp")]
        expected = 0.0
        for _, amount, unit in ingredients:
            ml, err = recipes.convert_unit(amount, unit, "ml")
            self.assertIsNone(err)
            expected += ml
        total, error = recipes.total_volume_ml(ingredients)
        self.assertIsNone(error)
        self.assertAlmostEqual(total, expected, places=6)


class ResultErrorConventionRuleTests(unittest.TestCase):
    """The project rule: failure-prone functions return (result, error)
    tuples instead of raising."""

    def test_convert_unit_success_returns_two_tuple(self):
        result = recipes.convert_unit(1, "cup", "ml")
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)

    def test_convert_unit_unknown_from_unit_does_not_raise(self):
        try:
            result, error = recipes.convert_unit(1, "gallon", "ml")
        except Exception as exc:  # pragma: no cover - failure path under test
            self.fail(f"convert_unit raised {exc!r} instead of returning an error tuple")
        self.assertIsNone(result)
        self.assertIsInstance(error, str)
        self.assertTrue(error)

    def test_convert_unit_unknown_to_unit_does_not_raise(self):
        try:
            result, error = recipes.convert_unit(1, "cup", "gallon")
        except Exception as exc:  # pragma: no cover - failure path under test
            self.fail(f"convert_unit raised {exc!r} instead of returning an error tuple")
        self.assertIsNone(result)
        self.assertIsInstance(error, str)
        self.assertTrue(error)

    def test_total_volume_ml_returns_two_tuple(self):
        result = recipes.total_volume_ml([("a", 1, "ml")])
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)

    def test_total_volume_ml_bad_unit_does_not_raise(self):
        try:
            result, error = recipes.total_volume_ml([("a", 1, "cup"), ("b", 2, "gallon")])
        except Exception as exc:  # pragma: no cover - failure path under test
            self.fail(f"total_volume_ml raised {exc!r} instead of returning an error tuple")
        self.assertIsNone(result)
        self.assertIsInstance(error, str)
        self.assertTrue(error)

    def test_convert_unit_source_never_raises(self):
        source = (ROOT / "recipes.py").read_text(encoding="utf-8")
        self.assertFalse(
            _function_has_raise(source, "convert_unit"),
            "convert_unit must return an error tuple, never raise",
        )

    def test_total_volume_ml_source_never_raises(self):
        source = (ROOT / "recipes.py").read_text(encoding="utf-8")
        self.assertFalse(
            _function_has_raise(source, "total_volume_ml"),
            "total_volume_ml must return an error tuple, never raise",
        )


if __name__ == "__main__":
    unittest.main()
