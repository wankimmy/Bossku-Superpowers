import ast
import os
import unittest

import skuparse


def _tree():
    with open(os.path.abspath(skuparse.__file__), "r", encoding="utf-8") as f:
        return ast.parse(f.read())


from skuparse import parse_sku, is_valid_sku, parse_order_line


class SkuHiddenTests(unittest.TestCase):
    def test_parse_sku(self):
        self.assertEqual(parse_sku("AB-1234"), ("AB", 1234))
        self.assertEqual(parse_sku("ZZ-0007"), ("ZZ", 7))

    def test_parse_sku_bad(self):
        for bad in ("ab-1234", "AB1234", "AB-123", "AB-12345", "ABC-1234", "AB-12a4", "", "AB-1234\n", "A\u0e51-1234"):
            with self.assertRaises(ValueError, msg=repr(bad)):
                parse_sku(bad)

    def test_is_valid_sku(self):
        self.assertTrue(is_valid_sku("QR-9999"))
        self.assertFalse(is_valid_sku("qr-9999"))
        self.assertFalse(is_valid_sku(None))

    def test_order_line(self):
        self.assertEqual(parse_order_line("3x AB-1234"), (3, "AB", 1234))
        self.assertEqual(parse_order_line("  12x CD-0001 "), (12, "CD", 1))

    def test_order_line_bad(self):
        for bad in ("0x AB-1234", "x AB-1234", "3 AB-1234", "3xAB-1234", "3x ab-1234", "-3x AB-1234", "3x AB-1234 extra", ""):
            with self.assertRaises(ValueError, msg=repr(bad)):
                parse_order_line(bad)

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
