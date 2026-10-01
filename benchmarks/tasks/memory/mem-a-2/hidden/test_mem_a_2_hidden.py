import ast
import os
import unittest

import cart
from cart import Item, compute_subtotal_cents, apply_discount_cents, split_evenly_cents


def _source_tree():
    path = os.path.abspath(cart.__file__)
    with open(path, "r", encoding="utf-8") as f:
        source = f.read()
    return ast.parse(source)


class CartHiddenTests(unittest.TestCase):

    # ---- session 1: Item + compute_subtotal_cents ----

    def test_compute_subtotal_cents_basic(self):
        items = [Item("a", 250, 2), Item("b", 100, 1)]
        self.assertEqual(compute_subtotal_cents(items), 600)

    def test_compute_subtotal_cents_empty(self):
        self.assertEqual(compute_subtotal_cents([]), 0)

    def test_compute_subtotal_cents_single_item(self):
        self.assertEqual(compute_subtotal_cents([Item("a", 999, 1)]), 999)

    def test_item_stores_fields(self):
        item = Item("widget", 150, 3)
        self.assertEqual(item.name, "widget")
        self.assertEqual(item.unit_price_cents, 150)
        self.assertEqual(item.quantity, 3)

    # ---- session 2: apply_discount_cents + split_evenly_cents ----

    def test_apply_discount_cents_exact(self):
        self.assertEqual(apply_discount_cents(2000, 25), 1500)

    def test_apply_discount_cents_rounds_to_nearest_cent(self):
        # 999 * 10% = 99.9 -> rounds to 100 regardless of rounding direction
        self.assertEqual(apply_discount_cents(999, 10), 899)

    def test_apply_discount_cents_zero_percent(self):
        self.assertEqual(apply_discount_cents(500, 0), 500)

    def test_apply_discount_cents_full_discount(self):
        self.assertEqual(apply_discount_cents(500, 100), 0)

    def test_split_evenly_cents_exact_division(self):
        self.assertEqual(split_evenly_cents(900, 3), [300, 300, 300])

    def test_split_evenly_cents_with_remainder(self):
        self.assertEqual(split_evenly_cents(1000, 3), [334, 333, 333])

    def test_split_evenly_cents_single_person(self):
        self.assertEqual(split_evenly_cents(7, 1), [7])

    def test_split_evenly_cents_sums_to_total(self):
        shares = split_evenly_cents(10, 4)
        self.assertEqual(sum(shares), 10)
        self.assertEqual(shares, [3, 3, 2, 2])

    # ---- rule: integer cents, never floats ----

    def test_no_float_literals_in_source(self):
        tree = _source_tree()
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, float):
                self.fail("found a float literal in cart.py; money must stay integer cents")

    def test_no_float_builtin_calls(self):
        tree = _source_tree()
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "float":
                self.fail("found a call to float() in cart.py; money must stay integer cents")

    def test_no_true_division_operator(self):
        # `/` on ints gives a float. Exact arithmetic (fractions / decimal) is within the rule, so a
        # module that imports one of them may use `/` on those exact types.
        tree = _source_tree()
        exact = any(
            (isinstance(n, ast.Import) and any(a.name in ("fractions", "decimal") for a in n.names))
            or (isinstance(n, ast.ImportFrom) and n.module in ("fractions", "decimal"))
            for n in ast.walk(tree)
        )
        if exact:
            return
        for node in ast.walk(tree):
            if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
                self.fail("found `/` (true division) in cart.py; use integer // and % for cents")

    def test_discount_and_split_results_are_ints(self):
        self.assertIsInstance(apply_discount_cents(1000, 15), int)
        for share in split_evenly_cents(1000, 3):
            self.assertIsInstance(share, int)


if __name__ == "__main__":
    unittest.main()
