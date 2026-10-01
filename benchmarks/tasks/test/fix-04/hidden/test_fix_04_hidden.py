import unittest

from checkout import checkout_summary


class CheckoutHiddenTests(unittest.TestCase):
    def test_single_item_no_discount_no_bulk(self):
        total, lines = checkout_summary([("Widget", 10.0, 2, 0)], 0.10)
        self.assertEqual(total, 22.0)
        self.assertEqual(lines, ["Widget: 2 x 10.00 -0% = 20.00", "Tax: 2.00", "Total: 22.00"])

    def test_per_item_discount_applied(self):
        total, lines = checkout_summary([("Widget", 10.0, 2, 10)], 0.0)
        self.assertEqual(total, 18.0)
        self.assertEqual(lines, ["Widget: 2 x 10.00 -10% = 18.00", "Tax: 0.00", "Total: 18.00"])

    def test_multiple_items_subtotal(self):
        total, lines = checkout_summary([("A", 10.0, 1, 0), ("B", 20.0, 1, 0)], 0.0)
        self.assertEqual(total, 30.0)
        self.assertEqual(
            lines,
            ["A: 1 x 10.00 -0% = 10.00", "B: 1 x 20.00 -0% = 20.00", "Tax: 0.00", "Total: 30.00"],
        )

    def test_tax_without_bulk_discount(self):
        total, lines = checkout_summary([("A", 50.0, 1, 0)], 0.08)
        self.assertEqual(total, 54.0)
        self.assertEqual(lines, ["A: 1 x 50.00 -0% = 50.00", "Tax: 4.00", "Total: 54.00"])

    def test_bulk_discount_tax_charged_after_discount(self):
        total, lines = checkout_summary([("A", 80.0, 1, 0), ("B", 40.0, 1, 0)], 0.10)
        self.assertEqual(total, 118.8)
        self.assertEqual(
            lines,
            [
                "A: 1 x 80.00 -0% = 80.00",
                "B: 1 x 40.00 -0% = 40.00",
                "Bulk discount: -12.00",
                "Tax: 10.80",
                "Total: 118.80",
            ],
        )

    def test_exactly_at_threshold_no_discount(self):
        total, lines = checkout_summary([("A", 100.0, 1, 0)], 0.10, bulk_threshold=100.0)
        self.assertEqual(total, 110.0)
        self.assertNotIn("Bulk discount: -0.00", "".join(lines))
        self.assertEqual(lines, ["A: 1 x 100.00 -0% = 100.00", "Tax: 10.00", "Total: 110.00"])

    def test_just_above_threshold_triggers_discount(self):
        total, lines = checkout_summary([("A", 100.01, 1, 0)], 0.10, bulk_threshold=100.0)
        self.assertEqual(total, 99.01)
        self.assertEqual(
            lines,
            [
                "A: 1 x 100.01 -0% = 100.01",
                "Bulk discount: -10.00",
                "Tax: 9.00",
                "Total: 99.01",
            ],
        )

    def test_custom_bulk_threshold_and_discount(self):
        total, lines = checkout_summary(
            [("A", 60.0, 1, 0)], 0.05, bulk_threshold=50.0, bulk_discount=0.2
        )
        self.assertEqual(total, 50.4)
        self.assertEqual(
            lines,
            ["A: 1 x 60.00 -0% = 60.00", "Bulk discount: -12.00", "Tax: 2.40", "Total: 50.40"],
        )

    def test_zero_discount_percent_item(self):
        total, lines = checkout_summary([("A", 19.99, 3, 0)], 0.0)
        self.assertEqual(total, 59.97)
        self.assertEqual(lines, ["A: 3 x 19.99 -0% = 59.97", "Tax: 0.00", "Total: 59.97"])

    def test_zero_tax_rate(self):
        total, lines = checkout_summary([("A", 30.0, 1, 0)], 0.0)
        self.assertEqual(total, 30.0)
        self.assertEqual(lines, ["A: 1 x 30.00 -0% = 30.00", "Tax: 0.00", "Total: 30.00"])

    def test_rounding_happens_per_step_not_only_at_the_end(self):
        total, lines = checkout_summary(
            [("A", 33.335, 1, 0), ("B", 33.335, 1, 0), ("C", 33.335, 1, 0)], 0.10
        )
        self.assertEqual(total, 99.02)
        self.assertEqual(
            lines,
            [
                "A: 1 x 33.34 -0% = 33.34",
                "B: 1 x 33.34 -0% = 33.34",
                "C: 1 x 33.34 -0% = 33.34",
                "Bulk discount: -10.00",
                "Tax: 9.00",
                "Total: 99.02",
            ],
        )

    def test_discounted_items_with_bulk_discount_and_tax(self):
        total, lines = checkout_summary(
            [("A", 59.99, 2, 5)], 0.075, bulk_threshold=100.0, bulk_discount=0.15
        )
        self.assertEqual(total, 104.15)
        self.assertEqual(
            lines,
            [
                "A: 2 x 59.99 -5% = 113.98",
                "Bulk discount: -17.10",
                "Tax: 7.27",
                "Total: 104.15",
            ],
        )

    def test_default_bulk_threshold_and_discount_used_when_omitted(self):
        total, _ = checkout_summary([("A", 80.0, 1, 0), ("B", 40.0, 1, 0)], 0.10)
        # defaults are bulk_threshold=100.0, bulk_discount=0.1 -- same as the explicit test above
        self.assertEqual(total, 118.8)


if __name__ == "__main__":
    unittest.main()
