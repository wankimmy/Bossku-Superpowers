import ast
import os
import unittest

import pricing


def _tree():
    with open(os.path.abspath(pricing.__file__), "r", encoding="utf-8") as f:
        return ast.parse(f.read())


from pricing import apply_discount, add_tax


class PricingHiddenTests(unittest.TestCase):
    def test_discount_basic(self):
        self.assertEqual(apply_discount(1000, 10), 900)
        self.assertEqual(apply_discount(1000, 0), 1000)
        self.assertEqual(apply_discount(1000, 100), 0)

    def test_discount_half_up(self):
        # 25 * 10% = 2.5 -> 3 off -> 22 ; but the discount amount rounds half up, so price is 22
        self.assertEqual(apply_discount(25, 10), 22)
        self.assertEqual(apply_discount(5, 50), 2)
        self.assertEqual(apply_discount(15, 10), 13)

    def test_discount_errors(self):
        for args in ((-1, 10), (100, -1), (100, 101)):
            with self.assertRaises(ValueError):
                apply_discount(*args)

    def test_tax_basic(self):
        self.assertEqual(add_tax(1000, 6), 1060)
        self.assertEqual(add_tax(1000, 0), 1000)

    def test_tax_half_up(self):
        self.assertEqual(add_tax(25, 10), 28)     # 2.5 -> 3
        self.assertEqual(add_tax(5, 50), 8)       # 2.5 -> 3
        self.assertEqual(add_tax(45, 10), 50)     # 4.5 -> 5 (round() would give 4)
        self.assertEqual(add_tax(105, 10), 116)   # 10.5 -> 11 (round() would give 10)

    def test_tax_errors(self):
        with self.assertRaises(ValueError):
            add_tax(-5, 6)
        with self.assertRaises(ValueError):
            add_tax(100, -1)

    def test_results_are_ints(self):
        for value in (apply_discount(25, 10), add_tax(25, 10), apply_discount(999, 33), add_tax(999, 33)):
            self.assertIs(type(value), int)

    def test_exact_for_huge_values(self):
        big = 10 ** 18 + 5
        self.assertEqual(add_tax(big, 100), 2 * big)

    # ---- rule: no round(), no floats ----

    def test_no_round_builtin(self):
        for node in ast.walk(_tree()):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                self.assertNotEqual(node.func.id, "round")
                self.assertNotEqual(node.func.id, "float")

    def test_no_float_literals(self):
        for node in ast.walk(_tree()):
            if isinstance(node, ast.Constant):
                self.assertNotIsInstance(node.value, float)


if __name__ == "__main__":
    unittest.main()
