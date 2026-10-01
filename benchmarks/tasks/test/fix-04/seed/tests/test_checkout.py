import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from checkout import checkout_summary


class CheckoutTests(unittest.TestCase):
    def test_no_bulk_discount_tax_is_simple(self):
        total, lines = checkout_summary([("Widget", 10.0, 2, 0)], 0.10)
        self.assertEqual(total, 22.0)
        self.assertEqual(lines, ["Widget: 2 x 10.00 -0% = 20.00", "Tax: 2.00", "Total: 22.00"])

    def test_bulk_discount_tax_is_charged_after_the_discount(self):
        total, lines = checkout_summary([("A", 80.0, 1, 0), ("B", 40.0, 1, 0)], 0.10)
        self.assertEqual(total, 118.8)
        self.assertIn("Tax: 10.80", lines)


if __name__ == "__main__":
    unittest.main()
