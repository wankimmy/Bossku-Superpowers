import hashlib
import inspect
import os
import unittest

import legacy_format
from report import summarize, top_sellers


_EXPECTED_LEGACY_SHA256 = "39bf0f59a027884431def72bd6ea4ad00035a88c71f2c80ce26c89df30883070"


def _legacy_path():
    return os.path.abspath(legacy_format.__file__)


class ReportHiddenTests(unittest.TestCase):

    # ---- session 1: summarize ----

    def test_summarize_basic_two_products(self):
        lines = ["Widget|3|199", "Gadget|2|50"]
        self.assertEqual(summarize(lines), {"Widget": 3, "Gadget": 2})

    def test_summarize_aggregates_same_product(self):
        lines = ["Widget|3|199", "Widget|2|199"]
        self.assertEqual(summarize(lines), {"Widget": 5})

    def test_summarize_empty_list(self):
        self.assertEqual(summarize([]), {})

    # ---- session 2: tolerant parsing + top_sellers ----

    def test_summarize_cleans_whitespace_and_trailing_delimiter(self):
        lines = ["Widget | 3 |199|", "Widget|1|199"]
        self.assertEqual(summarize(lines), {"Widget": 4})

    def test_summarize_skips_unrecoverable_bad_qty_row(self):
        lines = ["Widget|3|199", "Gadget|abc|50"]
        result = summarize(lines)
        self.assertEqual(result, {"Widget": 3})
        self.assertNotIn("Gadget", result)

    def test_summarize_skips_row_with_too_few_fields(self):
        lines = ["Widget|3|199", "OnlyTwo|5"]
        result = summarize(lines)
        self.assertEqual(result, {"Widget": 3})

    def test_summarize_does_not_raise_on_messy_input(self):
        lines = ["Widget | 3 |199|", "Gadget|abc|50", "OnlyTwo|5", "Gizmo|1|25"]
        try:
            result = summarize(lines)
        except Exception as exc:  # pragma: no cover - failure path
            self.fail("summarize raised on messy input: {!r}".format(exc))
        self.assertEqual(result, {"Widget": 3, "Gizmo": 1})

    def test_top_sellers_orders_by_quantity_desc(self):
        lines = ["A|5|10", "B|9|10", "C|1|10"]
        self.assertEqual(top_sellers(lines, 2), ["B", "A"])

    def test_top_sellers_tie_break_alphabetical(self):
        lines = ["Zed|4|10", "Amy|4|10", "Mid|4|10"]
        self.assertEqual(top_sellers(lines, 3), ["Amy", "Mid", "Zed"])

    def test_top_sellers_n_larger_than_available(self):
        lines = ["A|5|10", "B|2|10"]
        self.assertEqual(top_sellers(lines, 10), ["A", "B"])

    def test_top_sellers_n_one(self):
        lines = ["A|5|10", "B|9|10"]
        self.assertEqual(top_sellers(lines, 1), ["B"])

    # ---- rule: legacy_format.py is off-limits ----

    def test_legacy_format_file_is_byte_identical(self):
        with open(_legacy_path(), "rb") as f:
            digest = hashlib.sha256(f.read()).hexdigest()
        self.assertEqual(
            digest, _EXPECTED_LEGACY_SHA256,
            "legacy_format.py was modified; it is frozen and owned by another team",
        )

    def test_legacy_format_parse_line_signature_unchanged(self):
        params = list(inspect.signature(legacy_format.parse_line).parameters)
        self.assertEqual(params, ["line"])

    def test_legacy_format_still_rejects_messy_input_directly(self):
        # The fix must live in report.py's wrapper, not inside legacy_format itself.
        with self.assertRaises(ValueError):
            legacy_format.parse_line("Widget | 3 |199|")

    def test_legacy_format_still_does_not_strip_fields(self):
        row = legacy_format.parse_line(" Gadget|2|50")
        self.assertEqual(row["name"], " Gadget")


if __name__ == "__main__":
    unittest.main()
