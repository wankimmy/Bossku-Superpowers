import ast
import os
import unittest

import orders


def _tree():
    with open(os.path.abspath(orders.__file__), "r", encoding="utf-8") as f:
        return ast.parse(f.read())


import logging
import shlex

import orders as orders_mod
from orders import place_order, cancel_order, refund_order


class OrdersHiddenTests(unittest.TestCase):
    def _assert_format(self, cm):
        self.assertTrue(cm.records)
        for rec in cm.records:
            msg = rec.getMessage()
            self.assertTrue(msg.startswith("event="), msg)
            for token in shlex.split(msg):   # key="quoted value" is still key=value
                self.assertIn("=", token, msg)

    def test_place_and_cancel(self):
        orders = []
        o = place_order(orders, 1, 500)
        self.assertEqual(o, {"id": 1, "total_cents": 500, "status": "placed"})
        self.assertEqual(cancel_order(orders, 1)["status"], "cancelled")
        with self.assertRaises(KeyError):
            cancel_order(orders, 9)

    def test_refund_logs_in_format_with_id_and_reason(self):
        orders = []
        place_order(orders, 7, 900)
        with self.assertLogs("orders", level="DEBUG") as cm:
            out = refund_order(orders, 7, "damaged")
        self.assertEqual(out["status"], "refunded")
        self._assert_format(cm)
        text = " ".join(r.getMessage() for r in cm.records)
        self.assertIn("damaged", text)
        self.assertIn("7", text)

    def test_refund_reason_with_spaces_stays_key_value(self):
        orders = []
        place_order(orders, 7, 900)
        with self.assertLogs("orders", level="DEBUG") as cm:
            refund_order(orders, 7, "arrived broken")
        self._assert_format(cm)

    def test_rejected_refunds_are_logged_too(self):
        orders = []
        place_order(orders, 1, 100)
        cancel_order(orders, 1)
        with self.assertLogs("orders", level="DEBUG") as cm:
            with self.assertRaises(ValueError):
                refund_order(orders, 1, "late")
        self._assert_format(cm)
        with self.assertLogs("orders", level="DEBUG") as cm:
            with self.assertRaises(KeyError):
                refund_order(orders, 2, "late")
        self._assert_format(cm)

    # ---- rule: no print, module logger ----

    def test_no_print_calls(self):
        for node in ast.walk(_tree()):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                self.assertNotEqual(node.func.id, "print")

    def test_uses_named_module_logger(self):
        self.assertTrue(hasattr(orders_mod, "logger"), "no module-level logger")
        self.assertIsInstance(orders_mod.logger, logging.Logger)
        self.assertEqual(orders_mod.logger.name, "orders")


if __name__ == "__main__":
    unittest.main()
