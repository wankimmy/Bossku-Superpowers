import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from invoice import line_item_subtotal, compute_invoice_total, InvoiceError


class InvoiceBasicTests(unittest.TestCase):
    def test_line_item_no_discount(self):
        self.assertEqual(line_item_subtotal(1, "10.00"), "10.00")

    def test_line_item_with_discount(self):
        self.assertEqual(line_item_subtotal(2, "19.99", "10"), "35.98")

    def test_compute_invoice_total_empty(self):
        self.assertEqual(compute_invoice_total([]), "0.00")

    def test_quantity_must_be_positive(self):
        with self.assertRaises(InvoiceError):
            line_item_subtotal(0, "10.00")


if __name__ == "__main__":
    unittest.main()
