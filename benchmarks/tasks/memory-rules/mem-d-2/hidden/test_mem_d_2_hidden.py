import importlib
import inspect
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent

import pipeline
from pipeline import read_csv_rows, rows_to_json


class PipelineFunctionalityTests(unittest.TestCase):
    # ---- session 1: read_csv_rows / rows_to_json ----

    def test_read_csv_rows_empty_text(self):
        self.assertEqual(read_csv_rows(""), [])

    def test_read_csv_rows_header_only(self):
        self.assertEqual(read_csv_rows("name,age"), [])

    def test_read_csv_rows_preserves_row_order(self):
        text = "name,age\nAlice,30\nBob,25\nCara,40"
        rows = read_csv_rows(text)
        self.assertEqual([row["name"] for row in rows], ["Alice", "Bob", "Cara"])

    def test_rows_to_json_roundtrip(self):
        rows = [{"a": "1"}, {"a": "2"}]
        self.assertEqual(json.loads(rows_to_json(rows)), rows)

    # ---- session 2: cleanups wired into read_csv_rows ----

    def test_read_csv_rows_strips_whitespace_from_values(self):
        text = "name,age\n  Alice ,30 "
        rows = read_csv_rows(text)
        self.assertEqual(rows, [{"name": "Alice", "age": "30"}])

    def test_read_csv_rows_drops_empty_values_after_stripping(self):
        text = "name,age,nickname\nAlice,30,"
        rows = read_csv_rows(text)
        self.assertEqual(rows, [{"name": "Alice", "age": "30"}])
        self.assertNotIn("nickname", rows[0])

    def test_read_csv_rows_strip_before_drop_order(self):
        # a whitespace-only value must end up dropped too (strip happens first)
        text = "name,nickname\nAlice,   "
        rows = read_csv_rows(text)
        self.assertEqual(rows, [{"name": "Alice"}])

    def test_multiple_rows_each_cleaned_independently(self):
        text = "name,note\n Alice , hi \nBob, "
        rows = read_csv_rows(text)
        self.assertEqual(rows, [{"name": "Alice", "note": "hi"}, {"name": "Bob"}])


class TransformLayoutRuleTests(unittest.TestCase):
    """The project rule: row transforms live in transforms/, registered by name."""

    def test_transforms_package_exists(self):
        self.assertTrue((ROOT / "transforms").is_dir())
        self.assertTrue((ROOT / "transforms" / "__init__.py").is_file())

    def test_transform_order_is_nonempty_list_of_strings(self):
        import transforms

        self.assertIsInstance(transforms.TRANSFORM_ORDER, list)
        self.assertGreaterEqual(len(transforms.TRANSFORM_ORDER), 2)
        for name in transforms.TRANSFORM_ORDER:
            self.assertIsInstance(name, str)

    def test_transform_order_entries_resolve_to_modules_with_apply(self):
        import transforms

        for name in transforms.TRANSFORM_ORDER:
            module = importlib.import_module(f"transforms.{name}")
            self.assertTrue(
                hasattr(module, "apply"), f"transforms/{name}.py has no apply() function"
            )
            sig = inspect.signature(module.apply)
            self.assertEqual(
                len(sig.parameters), 1, f"transforms.{name}.apply should take exactly one row argument"
            )

    def test_transform_modules_are_files_directly_under_transforms(self):
        import transforms

        for name in transforms.TRANSFORM_ORDER:
            path = ROOT / "transforms" / f"{name}.py"
            self.assertTrue(path.is_file(), f"expected transforms/{name}.py to exist")

    def test_composing_transform_order_reproduces_pipeline_cleanup(self):
        # Rebuild the cleanup purely by walking the registry -- if a transform
        # lived somewhere else (e.g. inlined in pipeline.py) this wouldn't
        # reproduce read_csv_rows's own cleaned output.
        import transforms

        def apply_all(row):
            for name in transforms.TRANSFORM_ORDER:
                module = importlib.import_module(f"transforms.{name}")
                row = module.apply(row)
            return row

        raw_row = {"name": "  Alice ", "age": "30", "nickname": "   "}
        self.assertEqual(apply_all(raw_row), {"name": "Alice", "age": "30"})

        text = "name,age,nickname\n  Alice ,30,   "
        self.assertEqual(read_csv_rows(text), [apply_all(dict(raw_row))])


if __name__ == "__main__":
    unittest.main()
