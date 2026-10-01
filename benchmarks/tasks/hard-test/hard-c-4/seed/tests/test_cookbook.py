import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cookbook import parse_ingredient, scale_recipe


class CookbookTests(unittest.TestCase):
    def test_parse_with_unit(self):
        ing = parse_ingredient("2 cups flour")
        self.assertEqual(ing.quantity, 2.0)
        self.assertEqual(ing.unit, "cup")
        self.assertEqual(ing.name, "flour")

    def test_scale_recipe(self):
        ing = parse_ingredient("2 cups flour")
        scaled = scale_recipe([ing], 2)
        self.assertEqual(scaled[0].quantity, 4.0)

    def test_parse_without_recognized_unit(self):
        ing = parse_ingredient("3 eggs")
        self.assertEqual(ing.unit, "count")
        self.assertEqual(ing.name, "eggs")

    def test_parse_rejects_invalid_quantity(self):
        with self.assertRaises(ValueError):
            parse_ingredient("flour")


if __name__ == "__main__":
    unittest.main()
