import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inventory import Inventory


class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.inv = Inventory()
        self.inv.add_item("A1", "Widget", 10, 2.50)
        self.inv.add_item("B2", "Gadget", 3, 10.00)

    def test_total_value(self):
        self.assertEqual(self.inv.total_value(), 55.00)

    def test_total_value_after_remove(self):
        self.inv.total_value()
        self.inv.remove_item("A1", 4)
        self.assertEqual(self.inv.total_value(), 40.00)

    def test_low_stock_below_threshold(self):
        self.assertEqual(self.inv.low_stock(5), ["B2"])

    def test_low_stock_includes_threshold(self):
        self.inv.remove_item("A1", 5)
        self.assertEqual(self.inv.low_stock(5), ["A1", "B2"])

    def test_remove_too_many(self):
        with self.assertRaises(ValueError):
            self.inv.remove_item("A1", 11)


if __name__ == "__main__":
    unittest.main()
