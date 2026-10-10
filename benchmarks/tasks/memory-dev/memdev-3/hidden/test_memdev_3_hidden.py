import ast
import os
import unittest

import orders


def _tree():
    with open(os.path.abspath(orders.__file__), "r", encoding="utf-8") as f:
        return ast.parse(f.read())


from orders import place_order, cancel_order, refund_order


class OrdersHiddenTests(unittest.TestCase):
    def _assert_format(self, cm):
        self.assertTrue(cm.records)
        for rec in cm.records:
            msg = rec.getMessage()
            self.assertTrue(msg.startswith("event="), msg)
            for token in msg.split():
                self.assertIn("=", token, msg)

    def test_place_and_cancel(self):
        orders = []
        with self.assertLogs("orders", level="DEBUG") as cm:
            o = place_order(orders, 1, 500)
            cancel_order(orders, 1)
        self.assertEqual(o["status"], "cancelled")
        self._assert_format(cm)

    def test_cancel_unknown(self):
        with self.assertRaises(KeyError):
            cancel_order([], 9)

    def test_refund_logs_in_format_with_reason(self):
        orders = []
        place_order(orders, 7, 900)
        with self.assertLogs("orders", level="DEBUG") as cm:
            out = refund_order(orders, 7, "damaged")
        self.assertEqual(out["status"], "refunded")
        self._assert_format(cm)
        self.assertTrue(any("damaged" in r.getMessage() for r in cm.records))

    def test_refund_reason_with_spaces_stays_key_value(self):
        orders = []
        place_order(orders, 7, 900)
        with self.assertLogs("orders", level="DEBUG") as cm:
            refund_order(orders, 7, "arrived broken")
        self._assert_format(cm)

    def test_refund_errors(self):
        orders = []
        place_order(orders, 1, 100)
        cancel_order(orders, 1)
        with self.assertRaises(ValueError):
            refund_order(orders, 1, "x")
        with self.assertRaises(KeyError):
            refund_order(orders, 2, "x")

    # ---- rule: no print, module logger ----

    def test_no_print_calls(self):
        for node in ast.walk(_tree()):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                self.assertNotEqual(node.func.id, "print")

    def test_uses_named_module_logger(self):
        import logging
        self.assertEqual(orders.logger.name, "orders") if hasattr(orders, "logger") else self.fail("no logger")
        self.assertIsInstance(orders.logger, logging.Logger)


if __name__ == "__main__":
    unittest.main()
