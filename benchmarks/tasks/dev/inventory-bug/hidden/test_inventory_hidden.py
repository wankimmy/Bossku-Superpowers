import unittest

from inventory import Inventory, Item


class HiddenInventoryTests(unittest.TestCase):
    def setUp(self):
        self.inv = Inventory()
        self.inv.add_item("A1", "Widget", 10, 2.50)
        self.inv.add_item("B2", "Gadget", 3, 10.00)
        self.inv.add_item("C3", "Gizmo", 5, 1.00)

    def test_total_value_updates_after_remove(self):
        self.assertEqual(self.inv.total_value(), 60.00)
        self.inv.remove_item("A1", 4)
        self.assertEqual(self.inv.total_value(), 50.00)

    def test_total_value_updates_after_removing_everything_of_an_item(self):
        self.inv.total_value()
        self.inv.remove_item("B2", 3)
        self.assertEqual(self.inv.total_value(), 30.00)

    def test_total_value_updates_after_add(self):
        self.inv.total_value()
        self.inv.add_item("D4", "Doohickey", 2, 4.25)
        self.assertEqual(self.inv.total_value(), 68.50)

    def test_discounted_value_follows_removal(self):
        self.inv.discounted_value(10)
        self.inv.remove_item("A1", 10)
        self.assertEqual(self.inv.discounted_value(10), 31.5)

    def test_low_stock_includes_exact_threshold(self):
        self.assertEqual(self.inv.low_stock(5), ["B2", "C3"])

    def test_low_stock_excludes_items_above_threshold(self):
        self.assertEqual(self.inv.low_stock(3), ["B2"])
        self.assertEqual(self.inv.low_stock(2), [])

    def test_low_stock_is_sorted(self):
        self.inv.add_item("0Z", "Zero", 1, 1.0)
        self.assertEqual(self.inv.low_stock(10), sorted(["0Z", "A1", "B2", "C3"]))

    def test_removing_all_stock_drops_the_item(self):
        self.inv.remove_item("B2", 3)
        self.assertEqual(self.inv.low_stock(5), ["C3"])

    def test_remove_errors_are_unchanged(self):
        with self.assertRaises(KeyError):
            self.inv.remove_item("nope", 1)
        with self.assertRaises(ValueError):
            self.inv.remove_item("A1", 11)
        self.assertEqual(self.inv.total_value(), 60.00)

    def test_add_validation_is_unchanged(self):
        with self.assertRaises(ValueError):
            self.inv.add_item("E5", "Bad", -1, 1.0)
        with self.assertRaises(ValueError):
            self.inv.add_item("E5", "Bad", 1, -1.0)

    def test_readding_a_sku_adds_quantity_and_takes_the_new_price(self):
        self.inv.add_item("A1", "Widget", 5, 3.00)
        self.assertEqual(self.inv.total_value(), 15 * 3.00 + 30.00 + 5.00)

    def test_item_dataclass_is_still_available(self):
        self.assertEqual(Item("S", "N", 1, 2.0).sku, "S")


if __name__ == "__main__":
    unittest.main()
