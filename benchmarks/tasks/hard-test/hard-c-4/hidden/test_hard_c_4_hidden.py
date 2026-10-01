import importlib.util
import io
import os
import re
import tempfile
import unittest
from contextlib import redirect_stdout

import cookbook
import menu
import parsing
import planning
from parsing import Ingredient, parse_ingredient
from planning import build_shopping_list, scale_recipe


ROOT = os.path.dirname(os.path.abspath(__file__))


def _load_script():
    path = os.path.join(ROOT, "scripts", "print_shopping_list.py")
    spec = importlib.util.spec_from_file_location("print_shopping_list_script", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ParseIngredientTests(unittest.TestCase):
    def test_basic_with_unit(self):
        ing = parse_ingredient("2 cups flour")
        self.assertEqual(ing, Ingredient(2.0, "cup", "flour"))

    def test_unit_token_case_insensitive(self):
        ing = parse_ingredient("1.5 TBSP olive oil")
        self.assertEqual(ing, Ingredient(1.5, "tbsp", "olive oil"))

    def test_no_unit_single_word_name(self):
        ing = parse_ingredient("3 eggs")
        self.assertEqual(ing, Ingredient(3.0, "count", "eggs"))

    def test_no_unit_multi_word_name(self):
        ing = parse_ingredient("3 large eggs")
        self.assertEqual(ing, Ingredient(3.0, "count", "large eggs"))

    def test_collapses_extra_whitespace(self):
        ing = parse_ingredient("2   cups   flour")
        self.assertEqual(ing, Ingredient(2.0, "cup", "flour"))

    def test_missing_name_raises(self):
        with self.assertRaises(ValueError):
            parse_ingredient("2 cups")

    def test_invalid_quantity_raises(self):
        with self.assertRaises(ValueError):
            parse_ingredient("flour")

    def test_zero_quantity_raises(self):
        with self.assertRaises(ValueError):
            parse_ingredient("0 cup flour")

    def test_negative_quantity_raises(self):
        with self.assertRaises(ValueError):
            parse_ingredient("-1 cup flour")

    def test_ingredient_is_immutable(self):
        ing = parse_ingredient("2 cups flour")
        with self.assertRaises(Exception):
            ing.quantity = 10


class ScaleRecipeTests(unittest.TestCase):
    def test_multiplies_quantities(self):
        ings = [parse_ingredient("2 cups flour"), parse_ingredient("1 cup milk")]
        scaled = scale_recipe(ings, 1.5)
        self.assertEqual(
            scaled, [Ingredient(3.0, "cup", "flour"), Ingredient(1.5, "cup", "milk")]
        )

    def test_does_not_mutate_input(self):
        ings = [parse_ingredient("2 cups flour")]
        original = ings[0]
        scale_recipe(ings, 3)
        self.assertEqual(ings[0], original)
        self.assertEqual(ings[0].quantity, 2.0)

    def test_nonpositive_factor_raises(self):
        ings = [parse_ingredient("2 cups flour")]
        with self.assertRaises(ValueError):
            scale_recipe(ings, 0)

    def test_empty_list(self):
        self.assertEqual(scale_recipe([], 2), [])


class BuildShoppingListTests(unittest.TestCase):
    def test_aggregates_same_name_and_unit(self):
        recipe1 = [Ingredient(2.0, "cup", "Flour")]
        recipe2 = [Ingredient(1.0, "cup", "flour")]
        result = build_shopping_list([recipe1, recipe2])
        self.assertEqual(result, [Ingredient(3.0, "cup", "Flour")])

    def test_keeps_units_separate_no_conversion(self):
        recipe1 = [parse_ingredient("500 g sugar")]
        recipe2 = [parse_ingredient("1 kg sugar")]
        result = build_shopping_list([recipe1, recipe2])
        self.assertEqual(
            result,
            [Ingredient(500.0, "g", "sugar"), Ingredient(1.0, "kg", "sugar")],
        )

    def test_sorted_output(self):
        recipe = [
            parse_ingredient("1 cup milk"),
            parse_ingredient("1 cup flour"),
            parse_ingredient("1 cup eggs"),
        ]
        result = build_shopping_list([recipe])
        self.assertEqual([ing.name for ing in result], ["eggs", "flour", "milk"])

    def test_empty_recipes(self):
        self.assertEqual(build_shopping_list([]), [])
        self.assertEqual(build_shopping_list([[], []]), [])


class CookbookShimTests(unittest.TestCase):
    def test_reexports_identity(self):
        self.assertIs(cookbook.Ingredient, parsing.Ingredient)
        self.assertIs(cookbook.UNIT_ALIASES, parsing.UNIT_ALIASES)
        self.assertIs(cookbook.parse_ingredient, parsing.parse_ingredient)
        self.assertIs(cookbook.scale_recipe, planning.scale_recipe)
        self.assertIs(cookbook.build_shopping_list, planning.build_shopping_list)

    def test_star_import_exposes_exact_public_names(self):
        namespace = {}
        exec("from cookbook import *", namespace)
        names = {k for k in namespace if not k.startswith("__")}
        self.assertEqual(
            names,
            {
                "Ingredient",
                "UNIT_ALIASES",
                "parse_ingredient",
                "scale_recipe",
                "build_shopping_list",
            },
        )


class CallSiteTests(unittest.TestCase):
    def test_menu_plan_week_still_works(self):
        recipes = [["2 cups flour", "1 cup milk"], ["1 cup flour"]]
        result = menu.plan_week(recipes, servings_factor=2)
        self.assertEqual(
            result,
            [Ingredient(6.0, "cup", "flour"), Ingredient(2.0, "cup", "milk")],
        )

    def test_scripts_print_shopping_list_cli(self):
        script = _load_script()
        with tempfile.TemporaryDirectory() as tmp:
            path1 = os.path.join(tmp, "r1.txt")
            path2 = os.path.join(tmp, "r2.txt")
            with open(path1, "w", encoding="utf-8") as handle:
                handle.write("2 cups flour\n1 cup milk\n")
            with open(path2, "w", encoding="utf-8") as handle:
                handle.write("1 cup flour\n")
            buf = io.StringIO()
            with redirect_stdout(buf):
                script.main([path1, path2])
        lines = buf.getvalue().splitlines()
        self.assertEqual(lines, ["3 cup flour", "1 cup milk"])

    def test_readme_example_still_executes(self):
        readme_path = os.path.join(ROOT, "README.md")
        with open(readme_path, encoding="utf-8") as handle:
            text = handle.read()
        match = re.search(r"```python\n(.*?)```", text, re.DOTALL)
        self.assertIsNotNone(match, "README should contain a python example")
        namespace = {}
        exec(match.group(1), namespace)
        self.assertEqual(namespace.get("result"), [Ingredient(6.0, "cup", "flour")])


if __name__ == "__main__":
    unittest.main()
