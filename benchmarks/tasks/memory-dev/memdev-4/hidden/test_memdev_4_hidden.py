import ast
import os
import unittest

import skuparse


def _tree():
    with open(os.path.abspath(skuparse.__file__), "r", encoding="utf-8") as f:
        return ast.parse(f.read())


from skuparse import parse_sku, is_valid_sku, find_skus


class SkuHiddenTests(unittest.TestCase):
    def test_parse_sku(self):
        self.assertEqual(parse_sku("AB-1234"), ("AB", 1234))
        self.assertEqual(parse_sku("ZZ-0007"), ("ZZ", 7))

    def test_parse_sku_bad(self):
        for bad in ("ab-1234", "AB1234", "AB-123", "AB-12345", "ABC-1234", "AB-12a4", "", "AB-1234\n"):
            with self.assertRaises(ValueError, msg=repr(bad)):
                parse_sku(bad)

    def test_is_valid_sku(self):
        self.assertTrue(is_valid_sku("QR-9999"))
        self.assertFalse(is_valid_sku("qr-9999"))
        self.assertFalse(is_valid_sku(None))

    def test_find_skus_example(self):
        text = "Please ship AB-1234 and CD-0007, plus ef-1234 (typo) and XY-12345."
        self.assertEqual(find_skus(text), [("AB", 1234), ("CD", 7)])

    def test_find_skus_punctuation_and_order(self):
        self.assertEqual(find_skus("(GH-0001) then ZZ-9999. Finally KL-0042; MN-0003:"),
                         [("GH", 1), ("ZZ", 9999), ("KL", 42), ("MN", 3)])

    def test_find_skus_repeats_kept(self):
        self.assertEqual(find_skus("AB-1234 AB-1234"), [("AB", 1234), ("AB", 1234)])

    def test_find_skus_rejects_partial_words(self):
        self.assertEqual(find_skus("XXAB-1234 AB-12345 AB-123 ab-1234 AB_1234"), [])

    def test_find_skus_empty_and_odd_input(self):
        self.assertEqual(find_skus(""), [])
        self.assertEqual(find_skus("nothing to see here"), [])
        self.assertEqual(find_skus("---- ,,, ()"), [])

    # ---- rule: no regular expressions ----

    def test_no_regex_imports(self):
        banned = {"re", "regex", "sre_parse", "sre_compile"}
        for node in ast.walk(_tree()):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self.assertNotIn(alias.name.split(".")[0], banned)
            if isinstance(node, ast.ImportFrom):
                self.assertNotIn((node.module or "").split(".")[0], banned)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "__import__":
                self.fail("dynamic import")


if __name__ == "__main__":
    unittest.main()
