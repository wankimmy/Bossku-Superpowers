import unittest
from decimal import Decimal

from pricing.cart import Cart
from pricing.receipt import build_receipt


def make_cart(items):
    cart = Cart()
    for sku, price, qty in items:
        cart.add_item(sku, price, qty)
    return cart


class PricingHiddenTests(unittest.TestCase):
    def test_subtotal_multiple_lines_and_quantities(self):
        cart = make_cart([("A", "3.33", 3), ("B", "2.00", 5)])
        self.assertEqual(cart.subtotal(), Decimal("19.99"))

    def test_add_item_merges_same_sku_same_price(self):
        cart = Cart()
        cart.add_item("A", "5.00", 2)
        cart.add_item("A", "5.00", 3)
        self.assertEqual(len(cart.lines), 1)
        self.assertEqual(cart.subtotal(), Decimal("25.00"))

    def test_add_item_conflicting_price_raises(self):
        cart = Cart()
        cart.add_item("A", "5.00", 1)
        with self.assertRaises(ValueError):
            cart.add_item("A", "6.00", 1)

    def test_unknown_code_ignored_no_error(self):
        cart = make_cart([("A", "10.00", 1)])
        receipt = build_receipt(cart, ["BOGUS"])
        self.assertEqual(receipt["discount"], Decimal("0.00"))
        self.assertEqual(receipt["applied_codes"], [])

    def test_no_codes_default_shipping(self):
        cart = make_cart([("A", "30.00", 1)])
        receipt = build_receipt(cart, [])
        self.assertEqual(receipt["discount"], Decimal("0.00"))
        self.assertEqual(receipt["shipping"], Decimal("6.99"))
        self.assertEqual(receipt["total"], Decimal("36.99"))

    def test_free_shipping_exactly_at_threshold(self):
        cart = make_cart([("A", "50.00", 1)])
        receipt = build_receipt(cart, [])
        self.assertEqual(receipt["shipping"], Decimal("0.00"))
        self.assertEqual(receipt["total"], Decimal("50.00"))

    def test_shipping_charged_just_below_threshold(self):
        cart = make_cart([("A", "49.99", 1)])
        receipt = build_receipt(cart, [])
        self.assertEqual(receipt["shipping"], Decimal("6.99"))
        self.assertEqual(receipt["total"], Decimal("56.98"))

    def test_shipping_free_just_above_threshold(self):
        cart = make_cart([("A", "50.01", 1)])
        receipt = build_receipt(cart, [])
        self.assertEqual(receipt["shipping"], Decimal("0.00"))
        self.assertEqual(receipt["total"], Decimal("50.01"))

    def test_empty_cart_no_codes_all_zero(self):
        cart = Cart()
        receipt = build_receipt(cart, [])
        self.assertEqual(receipt["subtotal"], Decimal("0.00"))
        self.assertEqual(receipt["discount"], Decimal("0.00"))
        self.assertEqual(receipt["shipping"], Decimal("0.00"))
        self.assertEqual(receipt["total"], Decimal("0.00"))
        self.assertEqual(receipt["applied_codes"], [])

    def test_empty_cart_fixed_code_does_not_go_negative(self):
        cart = Cart()
        receipt = build_receipt(cart, ["10OFF"])
        self.assertEqual(receipt["discount"], Decimal("0.00"))
        self.assertEqual(receipt["shipping"], Decimal("0.00"))
        self.assertEqual(receipt["total"], Decimal("0.00"))
        self.assertEqual(receipt["applied_codes"], ["10OFF"])

    def test_percent_discount_rounds_half_up_on_exact_half_cent(self):
        cart = make_cart([("A", "17.50", 1)])
        receipt = build_receipt(cart, ["SAVE15"])
        self.assertEqual(receipt["discount"], Decimal("2.63"))
        self.assertEqual(receipt["total"], Decimal("21.86"))

    def test_percent_discount_exact_no_rounding_needed(self):
        cart = make_cart([("A", "40.00", 1)])
        receipt = build_receipt(cart, ["SAVE20"])
        self.assertEqual(receipt["discount"], Decimal("8.00"))
        self.assertEqual(receipt["total"], Decimal("38.99"))

    def test_two_percent_codes_best_wins(self):
        cart = make_cart([("A", "100.00", 1)])
        receipt = build_receipt(cart, ["SAVE10", "SAVE20"])
        self.assertEqual(receipt["discount"], Decimal("20.00"))
        self.assertEqual(receipt["applied_codes"], ["SAVE20"])

    def test_two_percent_codes_best_wins_reversed_entry_order(self):
        cart = make_cart([("A", "100.00", 1)])
        receipt = build_receipt(cart, ["SAVE20", "SAVE10"])
        self.assertEqual(receipt["discount"], Decimal("20.00"))
        self.assertEqual(receipt["applied_codes"], ["SAVE20"])

    def test_two_fixed_codes_best_wins(self):
        cart = make_cart([("A", "100.00", 1)])
        receipt = build_receipt(cart, ["5OFF", "10OFF"])
        self.assertEqual(receipt["discount"], Decimal("10.00"))
        self.assertEqual(receipt["applied_codes"], ["10OFF"])

    def test_two_fixed_codes_best_wins_reversed_entry_order(self):
        cart = make_cart([("A", "100.00", 1)])
        receipt = build_receipt(cart, ["10OFF", "5OFF"])
        self.assertEqual(receipt["discount"], Decimal("10.00"))
        self.assertEqual(receipt["applied_codes"], ["10OFF"])

    def test_percent_and_fixed_combine_sequentially(self):
        cart = make_cart([("A", "100.00", 1)])
        receipt = build_receipt(cart, ["SAVE10", "10OFF"])
        self.assertEqual(receipt["discount"], Decimal("20.00"))
        self.assertEqual(receipt["applied_codes"], ["SAVE10", "10OFF"])
        self.assertEqual(receipt["total"], Decimal("80.00"))

    def test_tie_break_equal_percent_codes_earlier_entry_wins(self):
        cart = make_cart([("A", "100.00", 1)])
        receipt = build_receipt(cart, ["WELCOME10", "SAVE10"])
        self.assertEqual(receipt["discount"], Decimal("10.00"))
        self.assertEqual(receipt["applied_codes"], ["WELCOME10"])

    def test_tie_break_equal_percent_codes_earlier_entry_wins_swapped(self):
        cart = make_cart([("A", "100.00", 1)])
        receipt = build_receipt(cart, ["SAVE10", "WELCOME10"])
        self.assertEqual(receipt["discount"], Decimal("10.00"))
        self.assertEqual(receipt["applied_codes"], ["SAVE10"])

    def test_code_matching_is_case_and_whitespace_insensitive(self):
        cart = make_cart([("A", "100.00", 1)])
        receipt = build_receipt(cart, [" save10 "])
        self.assertEqual(receipt["discount"], Decimal("10.00"))
        self.assertEqual(receipt["applied_codes"], ["SAVE10"])

    def test_lowercase_freeship_code_recognized_below_threshold(self):
        cart = make_cart([("A", "20.00", 1)])
        receipt = build_receipt(cart, ["freeship"])
        self.assertEqual(receipt["shipping"], Decimal("0.00"))
        self.assertEqual(receipt["applied_codes"], ["FREESHIP"])
        self.assertEqual(receipt["total"], Decimal("20.00"))

    def test_freeship_code_listed_even_when_already_free_by_threshold(self):
        cart = make_cart([("A", "100.00", 1)])
        receipt = build_receipt(cart, ["FREESHIP"])
        self.assertEqual(receipt["shipping"], Decimal("0.00"))
        self.assertEqual(receipt["applied_codes"], ["FREESHIP"])

    def test_fixed_discount_never_exceeds_subtotal(self):
        cart = make_cart([("A", "8.00", 1)])
        receipt = build_receipt(cart, ["10OFF"])
        self.assertEqual(receipt["discount"], Decimal("8.00"))
        self.assertEqual(receipt["total"], Decimal("6.99"))

    def test_new_cart_does_not_inherit_previous_carts_applied_codes(self):
        cart1 = make_cart([("A", "10.00", 1)])
        build_receipt(cart1, ["SAVE10"])
        self.assertIn("SAVE10", cart1.applied_codes)

        cart2 = make_cart([("B", "10.00", 1)])
        receipt2 = build_receipt(cart2, [])
        self.assertEqual(receipt2["applied_codes"], [])
        self.assertEqual(cart2.applied_codes, [])

    def test_applied_codes_order_is_percent_then_fixed_then_freeship(self):
        cart = make_cart([("A", "100.00", 1)])
        receipt = build_receipt(cart, ["FREESHIP", "10OFF", "SAVE10"])
        self.assertEqual(receipt["applied_codes"], ["SAVE10", "10OFF", "FREESHIP"])
        self.assertEqual(receipt["total"], Decimal("80.00"))


if __name__ == "__main__":
    unittest.main()
