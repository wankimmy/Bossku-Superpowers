import os
import sys
from decimal import Decimal

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest

from pricing.cart import Cart
from pricing.receipt import build_receipt


class PricingTests(unittest.TestCase):
    def test_subtotal_multiple_lines(self):
        cart = Cart()
        cart.add_item("MUG", "9.00", 2)
        cart.add_item("PEN", "1.50", 4)
        self.assertEqual(cart.subtotal(), Decimal("24.00"))

    def test_unknown_code_is_ignored(self):
        cart = Cart()
        cart.add_item("MUG", "9.00", 1)
        receipt = build_receipt(cart, ["NOTACODE"])
        self.assertEqual(receipt["discount"], Decimal("0.00"))

    def test_single_percent_code_exact_math(self):
        cart = Cart()
        cart.add_item("WIDGET", "100.00", 1)
        receipt = build_receipt(cart, ["SAVE10"])
        self.assertEqual(receipt["discount"], Decimal("10.00"))
        self.assertEqual(receipt["shipping"], Decimal("0.00"))
        self.assertEqual(receipt["total"], Decimal("90.00"))

    def test_shipping_charged_below_threshold(self):
        cart = Cart()
        cart.add_item("GADGET", "20.00", 1)
        receipt = build_receipt(cart, [])
        self.assertEqual(receipt["shipping"], Decimal("6.99"))
        self.assertEqual(receipt["total"], Decimal("26.99"))


if __name__ == "__main__":
    unittest.main()
