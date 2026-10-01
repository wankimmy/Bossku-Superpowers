import ast
import os
import sys
import unittest

import catalog
from catalog import add_product, import_products, make_slug, merge_product_lists


def _source_tree():
    path = os.path.abspath(catalog.__file__)
    with open(path, "r", encoding="utf-8") as f:
        source = f.read()
    return ast.parse(source)


def _call_name(node):
    func = node.func
    if isinstance(func, ast.Name):
        return func.id
    if isinstance(func, ast.Attribute):
        return func.attr
    return None


def _function_calls(tree, function_name):
    calls = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == function_name:
            for sub in ast.walk(node):
                if isinstance(sub, ast.Call):
                    name = _call_name(sub)
                    if name:
                        calls.add(name)
    return calls


def _transitive_calls(tree, function_name, _seen=None):
    """Names reachable by following calls to other locally-defined functions.

    This lets `import_products` satisfy "must key products through make_slug" either
    by calling it directly, or by calling `add_product` (which itself calls make_slug) -
    both are legitimate reuse of the one mandatory normalizer; only a fresh, ad hoc
    normalization written inline would fail to reach make_slug at all.
    """
    if _seen is None:
        _seen = set()
    if function_name in _seen:
        return set()
    _seen.add(function_name)
    direct = _function_calls(tree, function_name)
    reachable = set(direct)
    for name in direct:
        reachable |= _transitive_calls(tree, name, _seen)
    return reachable


class CatalogHiddenTests(unittest.TestCase):

    # ---- session 1: make_slug / add_product ----

    def test_make_slug_basic(self):
        self.assertEqual(make_slug("Blue Shirt"), "blue-shirt")

    def test_make_slug_collapses_punctuation_and_spaces(self):
        self.assertEqual(make_slug("Blue   Shirt!!"), "blue-shirt")

    def test_make_slug_strips_leading_trailing_hyphens(self):
        self.assertEqual(make_slug("  --Blue Shirt--  "), "blue-shirt")

    def test_add_product_inserts_under_slug_key(self):
        cat = {}
        add_product(cat, "Blue Shirt", 1000)
        self.assertIn("blue-shirt", cat)
        self.assertEqual(cat["blue-shirt"]["price_cents"], 1000)

    def test_add_product_duplicate_raises(self):
        cat = {}
        add_product(cat, "Blue Shirt", 1000)
        with self.assertRaises(ValueError):
            add_product(cat, "blue shirt", 1200)

    # ---- session 2: import_products ----

    def test_import_products_builds_catalog(self):
        cat = import_products(["Blue Shirt,1000", "Red Hat,500"])
        self.assertEqual(cat["blue-shirt"]["price_cents"], 1000)
        self.assertEqual(cat["red-hat"]["price_cents"], 500)

    def test_import_products_keys_are_slugs(self):
        cat = import_products(["Blue  Shirt!!,1000"])
        self.assertEqual(set(cat.keys()), {"blue-shirt"})

    # ---- session 2: merge_product_lists ----

    def test_merge_product_lists_keeps_b_price_on_conflict(self):
        merged = merge_product_lists([("Blue Shirt", 1000)], [("blue-shirt", 1200)])
        self.assertEqual(len(merged), 1)
        self.assertEqual(merged[make_slug("Blue Shirt")]["price_cents"], 1200)

    def test_merge_product_lists_normalizes_like_make_slug(self):
        merged = merge_product_lists(
            [("Men's Shirt!! ", 500)],
            [(" men's   shirt", 700)],
        )
        self.assertEqual(len(merged), 1)
        self.assertEqual(merged[make_slug("men's shirt")]["price_cents"], 700)

    def test_merge_product_lists_keeps_unique_products_from_both(self):
        merged = merge_product_lists([("Blue Shirt", 1000)], [("Red Hat", 500)])
        self.assertEqual(set(merged.keys()), {"blue-shirt", "red-hat"})

    # ---- rule: make_slug is the one mandatory normalizer; stdlib only ----

    def test_import_products_calls_make_slug(self):
        tree = _source_tree()
        calls = _transitive_calls(tree, "import_products")
        self.assertIn(
            "make_slug", calls,
            "import_products must key products through make_slug (directly, or via "
            "add_product), not its own normalization",
        )

    def test_merge_product_lists_calls_make_slug(self):
        tree = _source_tree()
        calls = _transitive_calls(tree, "merge_product_lists")
        self.assertIn(
            "make_slug", calls,
            "merge_product_lists must key products through make_slug, not its own normalization",
        )

    def test_only_stdlib_imports(self):
        tree = _source_tree()
        stdlib = getattr(sys, "stdlib_module_names", None)
        self.assertIsNotNone(stdlib, "this check needs Python 3.10+'s sys.stdlib_module_names")
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    top = alias.name.split(".")[0]
                    self.assertIn(top, stdlib, "non-stdlib import: {}".format(alias.name))
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    top = node.module.split(".")[0]
                    self.assertIn(top, stdlib, "non-stdlib import: {}".format(node.module))


if __name__ == "__main__":
    unittest.main()
