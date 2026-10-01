import unittest

from catalog import ProductCatalog


class ProductCatalogHiddenTests(unittest.TestCase):
    def setUp(self):
        self.catalog = ProductCatalog()
        self.red_mug = self.catalog.add_product("Red Mug", "Home", 9.99)
        self.blue_mug = self.catalog.add_product("Blue Mug", "Home", 11.50)
        self.notebook = self.catalog.add_product("Notebook", "Office", 3.25)
        self.diary = self.catalog.add_product("O'Brien's Diary", "Office", 7.00)
        self.figure = self.catalog.add_product("Action Figure", "Toys", 15.00)

    def names(self, results):
        return [r["name"] for r in results]

    def test_search_with_no_filters_returns_everything(self):
        self.assertEqual(len(self.catalog.search()), 5)

    def test_search_by_exact_category(self):
        results = self.catalog.search(category="Home")
        self.assertEqual(self.names(results), ["Blue Mug", "Red Mug"])

    def test_search_by_name_substring_is_case_insensitive(self):
        results = self.catalog.search(name_contains="MUG")
        self.assertEqual(self.names(results), ["Blue Mug", "Red Mug"])

    def test_search_by_price_range_is_inclusive(self):
        results = self.catalog.search(min_price=7.00, max_price=11.50)
        self.assertEqual(self.names(results), ["Blue Mug", "O'Brien's Diary", "Red Mug"])

    def test_filters_combine_with_and(self):
        results = self.catalog.search(category="Office", min_price=5.00)
        self.assertEqual(self.names(results), ["O'Brien's Diary"])

    def test_result_shape(self):
        results = self.catalog.search(category="Toys")
        self.assertEqual(results, [{"id": self.figure, "name": "Action Figure",
                                     "category": "Toys", "price": 15.00}])

    def test_add_product_returns_a_new_id_each_time(self):
        new_id = self.catalog.add_product("Pen", "Office", 1.00)
        self.assertNotIn(new_id, (self.red_mug, self.blue_mug, self.notebook, self.diary, self.figure))

    def test_add_product_rejects_negative_price(self):
        with self.assertRaises(ValueError):
            self.catalog.add_product("Broken", "Misc", -1.0)

    def test_apostrophe_in_name_is_searchable_unchanged(self):
        results = self.catalog.search(name_contains="o'brien")
        self.assertEqual(self.names(results), ["O'Brien's Diary"])

    def test_apostrophe_in_added_name_round_trips_exactly(self):
        new_id = self.catalog.add_product("D'Arcy's", "Misc", 2.5)
        results = self.catalog.search(name_contains="d'arcy")
        self.assertEqual(results, [{"id": new_id, "name": "D'Arcy's", "category": "Misc", "price": 2.5}])

    def test_category_boolean_bypass_payload_matches_nothing(self):
        self.assertEqual(self.catalog.search(category="Home' OR '1'='1"), [])

    def test_category_payload_does_not_corrupt_later_searches(self):
        self.catalog.search(category="Home' OR '1'='1")
        results = self.catalog.search(category="Home")
        self.assertEqual(self.names(results), ["Blue Mug", "Red Mug"])

    def test_name_contains_boolean_bypass_payload_matches_nothing(self):
        self.assertEqual(self.catalog.search(name_contains="x' OR '1'='1"), [])

    def test_name_contains_quote_payload_does_not_leak_rows(self):
        # a stray quote must never break the query or leak unrelated rows
        results = self.catalog.search(name_contains="mug' --")
        self.assertEqual(results, [])

    def test_category_drop_table_payload_leaves_table_usable(self):
        self.catalog.search(category="x'; DROP TABLE products; --")
        # the table must still be there and queryable afterwards
        self.assertEqual(len(self.catalog.search()), 5)


if __name__ == "__main__":
    unittest.main()
