import ast
import os
import unittest

import stock


def _tree():
    with open(os.path.abspath(stock.__file__), "r", encoding="utf-8") as f:
        return ast.parse(f.read())


from stock import Inventory, transfer


class StockHiddenTests(unittest.TestCase):
    def _msg(self, fn, *args):
        with self.assertRaises(ValueError) as ctx:
            fn(*args)
        return str(ctx.exception)

    def test_add_remove_quantity(self):
        inv = Inventory()
        inv.add("A", 5)
        inv.remove("A", 2)
        self.assertEqual(inv.quantity("A"), 3)
        self.assertEqual(inv.quantity("nope"), 0)

    def test_bad_qty(self):
        inv = Inventory()
        for bad in (0, -1, 1.5):
            self.assertTrue(self._msg(inv.add, "A", bad).startswith("[stock] "))
            self.assertTrue(self._msg(inv.remove, "A", bad).startswith("[stock] "))

    def test_remove_too_much(self):
        inv = Inventory()
        inv.add("A", 1)
        self.assertTrue(self._msg(inv.remove, "A", 2).startswith("[stock] "))
        self.assertEqual(inv.quantity("A"), 1)

    def test_transfer_moves(self):
        a, b = Inventory(), Inventory()
        a.add("A", 5)
        transfer(a, b, "A", 3)
        self.assertEqual((a.quantity("A"), b.quantity("A")), (2, 3))

    def test_transfer_insufficient_leaves_both_unchanged(self):
        a, b = Inventory(), Inventory()
        a.add("A", 2)
        msg = self._msg(transfer, a, b, "A", 3)
        self.assertTrue(msg.startswith("[stock] "), msg)
        self.assertEqual((a.quantity("A"), b.quantity("A")), (2, 0))

    def test_transfer_same_inventory(self):
        a = Inventory()
        a.add("A", 2)
        msg = self._msg(transfer, a, a, "A", 1)
        self.assertTrue(msg.startswith("[stock] "), msg)
        self.assertEqual(a.quantity("A"), 2)

    def test_transfer_bad_qty(self):
        a, b = Inventory(), Inventory()
        a.add("A", 2)
        self.assertTrue(self._msg(transfer, a, b, "A", 0).startswith("[stock] "))

    # ---- rule: every raised message carries the tag ----

    def test_every_raise_literal_has_tag(self):
        for node in ast.walk(_tree()):
            if isinstance(node, ast.Raise) and isinstance(node.exc, ast.Call) and node.exc.args:
                first = node.exc.args[0]
                if isinstance(first, ast.JoinedStr) and first.values:
                    first = first.values[0]
                if isinstance(first, ast.BinOp):
                    first = first.left
                if isinstance(first, ast.Constant) and isinstance(first.value, str):
                    self.assertTrue(first.value.startswith("[stock] "), first.value)


if __name__ == "__main__":
    unittest.main()
