import unittest

from catalog import Catalog

HEX = set("0123456789abcdef")


class CatalogHiddenTests(unittest.TestCase):
    def test_create_get_all_len(self):
        c = Catalog()
        a = c.create_item("Kopi", 350)
        b = c.create_item("Teh", 300)
        self.assertEqual((a["name"], a["price_cents"]), ("Kopi", 350))
        self.assertEqual(c.get(a["id"]), a)
        self.assertEqual(c.all(), [a, b])
        self.assertEqual(len(c), 2)
        with self.assertRaises(KeyError):
            c.get("nope")

    def test_validation(self):
        c = Catalog()
        for args in (("", 1), (None, 1), ("x", -1), ("x", 1.5)):
            with self.assertRaises(ValueError):
                c.create_item(*args)
        self.assertEqual(len(c), 0)

    # ---- rule: ids are uuid4 hex, 32 lowercase chars, no dashes ----

    def test_id_is_32_lowercase_hex(self):
        item = Catalog().create_item("Kopi", 350)
        self.assertIsInstance(item["id"], str)
        self.assertEqual(len(item["id"]), 32)
        self.assertTrue(set(item["id"]) <= HEX)

    def test_ids_are_unique_and_random(self):
        c = Catalog()
        ids = [c.create_item("x", 1)["id"] for _ in range(50)]
        self.assertEqual(len(set(ids)), 50)
        self.assertNotEqual(ids, sorted(ids))

    def test_id_is_version_4(self):
        item = Catalog().create_item("Kopi", 350)
        self.assertEqual(item["id"][12], "4")


if __name__ == "__main__":
    unittest.main()
