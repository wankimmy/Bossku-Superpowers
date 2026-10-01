import copy
import unittest
from decimal import Decimal

from invoice import line_item_subtotal, compute_invoice_total, InvoiceError


class LineItemSubtotalTests(unittest.TestCase):
    def test_no_discount_default(self):
        self.assertEqual(line_item_subtotal(1, "10.00"), "10.00")

    def test_basic_discount(self):
        self.assertEqual(line_item_subtotal(2, "19.99", "10"), "35.98")

    def test_half_up_rounding_tie(self):
        # 1 * 0.125 = 0.125 exactly. ROUND_HALF_UP -> 0.13.
        # (Python Decimal's default context is ROUND_HALF_EVEN, which would
        # wrongly give 0.12 here.)
        self.assertEqual(line_item_subtotal(1, "0.125", "0"), "0.13")

    def test_full_discount_boundary_is_zero(self):
        self.assertEqual(line_item_subtotal(5, "10.00", "100"), "0.00")

    def test_accepts_int_and_decimal_inputs_directly(self):
        self.assertEqual(line_item_subtotal(1, 100, 0), "100.00")
        self.assertEqual(line_item_subtotal(2, Decimal("4.995"), 0), "9.99")

    def test_quantity_zero_raises_invoice_error(self):
        with self.assertRaises(InvoiceError):
            line_item_subtotal(0, "10.00")

    def test_quantity_negative_raises_invoice_error(self):
        with self.assertRaises(InvoiceError):
            line_item_subtotal(-1, "10.00")

    def test_quantity_wrong_type_raises_type_error(self):
        with self.assertRaises(TypeError):
            line_item_subtotal(2.0, "10.00")
        with self.assertRaises(TypeError):
            line_item_subtotal("2", "10.00")
        with self.assertRaises(TypeError):
            line_item_subtotal(True, "10.00")  # bool is a subclass of int

    def test_unit_price_float_raises_type_error(self):
        with self.assertRaises(TypeError):
            line_item_subtotal(2, 10.0)

    def test_unit_price_negative_raises_invoice_error(self):
        with self.assertRaises(InvoiceError):
            line_item_subtotal(2, "-5.00")

    def test_unit_price_non_numeric_string_raises_invoice_error(self):
        with self.assertRaises(InvoiceError):
            line_item_subtotal(2, "abc")

    def test_unit_price_nan_and_infinity_raise_invoice_error(self):
        with self.assertRaises(InvoiceError):
            line_item_subtotal(1, "NaN")
        with self.assertRaises(InvoiceError):
            line_item_subtotal(1, "Infinity")

    def test_discount_percent_out_of_range_raises_invoice_error(self):
        with self.assertRaises(InvoiceError):
            line_item_subtotal(2, "10.00", "-1")
        with self.assertRaises(InvoiceError):
            line_item_subtotal(2, "10.00", "101")


class ComputeInvoiceTotalTests(unittest.TestCase):
    def test_single_item_matches_line_item_subtotal(self):
        items = [{"quantity": 2, "unit_price": "19.99", "discount_percent": "10"}]
        self.assertEqual(
            compute_invoice_total(items),
            line_item_subtotal(2, "19.99", "10"),
        )

    def test_multi_line_with_invoice_discount_and_tax(self):
        items = [
            {"quantity": 1, "unit_price": "33.33"},
            {"quantity": 3, "unit_price": "5.00", "discount_percent": "50"},
        ]
        result = compute_invoice_total(items, invoice_discount_percent=15, tax_percent=7)
        self.assertEqual(result, "37.14")

    def test_empty_list_is_zero(self):
        self.assertEqual(compute_invoice_total([]), "0.00")
        self.assertEqual(compute_invoice_total([], 50, 20), "0.00")

    def test_empty_list_still_validates_percents(self):
        with self.assertRaises(InvoiceError):
            compute_invoice_total([], invoice_discount_percent=-1)
        with self.assertRaises(InvoiceError):
            compute_invoice_total([], tax_percent=101)

    def test_not_a_list_raises_type_error(self):
        with self.assertRaises(TypeError):
            compute_invoice_total("not a list")

    def test_item_not_a_dict_raises_type_error(self):
        with self.assertRaises(TypeError):
            compute_invoice_total([1, 2, 3])

    def test_missing_required_keys_raise_invoice_error(self):
        with self.assertRaises(InvoiceError):
            compute_invoice_total([{"unit_price": "10.00"}])
        with self.assertRaises(InvoiceError):
            compute_invoice_total([{"quantity": 1}])

    def test_invoice_level_percents_out_of_range_raise(self):
        base = [{"quantity": 1, "unit_price": "10.00"}]
        with self.assertRaises(InvoiceError):
            compute_invoice_total(base, invoice_discount_percent=-1)
        with self.assertRaises(InvoiceError):
            compute_invoice_total(base, tax_percent=101)

    def test_does_not_mutate_input(self):
        items = [{"quantity": 1, "unit_price": "10.00"}]
        snapshot = copy.deepcopy(items)
        compute_invoice_total(items, invoice_discount_percent=10, tax_percent=5)
        self.assertEqual(items, snapshot)

    def test_ignores_unknown_keys_in_line_item(self):
        items = [{"quantity": 1, "unit_price": "10.00", "sku": "ABC123"}]
        self.assertEqual(compute_invoice_total(items), "10.00")

    def test_result_always_has_two_decimal_places(self):
        items = [{"quantity": 4, "unit_price": "25"}]
        self.assertEqual(compute_invoice_total(items), "100.00")


class ExceptionHierarchyTests(unittest.TestCase):
    def test_invoice_error_is_value_error(self):
        self.assertTrue(issubclass(InvoiceError, ValueError))


if __name__ == "__main__":
    unittest.main()
