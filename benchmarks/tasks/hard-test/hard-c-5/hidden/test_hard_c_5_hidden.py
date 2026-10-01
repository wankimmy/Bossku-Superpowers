import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout

import cli
import pipeline
from redactor import DEFAULT_RULES, RedactionRule, redact


SAMPLE = (
    "Contact Alice at alice@example.com or 555-123-4567, and Bob at "
    "bob@example.org too."
)
SAMPLE_REDACTED = (
    "Contact Alice at [REDACTED-EMAIL] or [REDACTED-PHONE], "
    "and Bob at [REDACTED-EMAIL] too."
)


class RedactTests(unittest.TestCase):
    def test_str_input_returns_str_and_counts(self):
        result, counts = redact(SAMPLE)
        self.assertEqual(result, SAMPLE_REDACTED)
        self.assertEqual(counts, {"email": 2, "phone": 1})

    def test_bytes_input_returns_bytes_and_matching_counts(self):
        result, counts = redact(SAMPLE.encode("utf-8"))
        self.assertIsInstance(result, bytes)
        self.assertEqual(result, SAMPLE_REDACTED.encode("utf-8"))
        self.assertEqual(counts, {"email": 2, "phone": 1})

    def test_counts_include_zero_for_unmatched_rules(self):
        result, counts = redact("nothing interesting here")
        self.assertEqual(result, "nothing interesting here")
        self.assertEqual(counts, {"email": 0, "phone": 0})

    def test_empty_string(self):
        self.assertEqual(redact(""), ("", {"email": 0, "phone": 0}))

    def test_empty_bytes(self):
        self.assertEqual(redact(b""), (b"", {"email": 0, "phone": 0}))

    def test_invalid_type_raises_typeerror(self):
        with self.assertRaises(TypeError):
            redact(42)

    def test_invalid_utf8_bytes_raises_unicodedecodeerror(self):
        with self.assertRaises(UnicodeDecodeError):
            redact(b"\xff\xfe")

    def test_unicode_content_roundtrips(self):
        content = "José's email is jose@example.com".encode("utf-8")
        result, counts = redact(content)
        self.assertEqual(counts, {"email": 1, "phone": 0})
        self.assertEqual(result, "José's email is [REDACTED-EMAIL]".encode("utf-8"))

    def test_rules_apply_sequentially_not_independently(self):
        rules = (
            RedactionRule("a", "cat", "[A]"),
            RedactionRule("b", "category", "[B]"),
        )
        result, counts = redact("category", rules=rules)
        self.assertEqual(result, "[A]egory")
        self.assertEqual(counts, {"a": 1, "b": 0})

    def test_rules_apply_sequentially_reversed_order_differs(self):
        rules = (
            RedactionRule("b", "category", "[B]"),
            RedactionRule("a", "cat", "[A]"),
        )
        result, counts = redact("category", rules=rules)
        self.assertEqual(result, "[B]")
        self.assertEqual(counts, {"b": 1, "a": 0})

    def test_redactionrule_is_immutable(self):
        rule = RedactionRule("x", "y", "z")
        with self.assertRaises(Exception):
            rule.name = "a"

    def test_default_rules_is_tuple_of_redactionrule(self):
        self.assertIsInstance(DEFAULT_RULES, tuple)
        self.assertTrue(all(isinstance(r, RedactionRule) for r in DEFAULT_RULES))


class ScanDocumentsTests(unittest.TestCase):
    def test_preserves_per_document_type(self):
        docs = ["email one: a@b.com", b"email two: c@d.com and phone 555-123-4567"]
        results, totals = pipeline.scan_documents(docs)
        self.assertIsInstance(results[0][0], str)
        self.assertIsInstance(results[1][0], bytes)
        self.assertEqual(results[0][1], {"email": 1, "phone": 0})
        self.assertEqual(results[1][1], {"email": 1, "phone": 1})

    def test_aggregates_totals_across_documents(self):
        docs = ["email one: a@b.com", b"email two: c@d.com and phone 555-123-4567"]
        _, totals = pipeline.scan_documents(docs)
        self.assertEqual(totals, {"email": 2, "phone": 1})

    def test_empty_document_list(self):
        results, totals = pipeline.scan_documents([])
        self.assertEqual(results, [])
        self.assertEqual(totals, {"email": 0, "phone": 0})

    def test_default_rules_consistent_with_redact(self):
        docs = [SAMPLE, SAMPLE.encode("utf-8")]
        results, totals = pipeline.scan_documents(docs)
        expected0 = redact(docs[0], DEFAULT_RULES)
        expected1 = redact(docs[1], DEFAULT_RULES)
        self.assertEqual(results[0], expected0)
        self.assertEqual(results[1], expected1)


class CliTests(unittest.TestCase):
    def test_cli_handles_text_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "note.txt")
            with open(path, "w", encoding="utf-8") as handle:
                handle.write("Email: a@b.com")
            buf = io.StringIO()
            with redirect_stdout(buf):
                cli.main([path])
        self.assertEqual(
            buf.getvalue().splitlines(),
            ["redacted: Email: [REDACTED-EMAIL]", "email: 1", "phone: 0"],
        )

    def test_cli_handles_bin_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "note.bin")
            with open(path, "wb") as handle:
                handle.write(b"Email: a@b.com and phone 555-123-4567")
            buf = io.StringIO()
            with redirect_stdout(buf):
                cli.main([path])
        self.assertEqual(
            buf.getvalue().splitlines(),
            [
                "redacted: Email: [REDACTED-EMAIL] and phone [REDACTED-PHONE]",
                "email: 1",
                "phone: 1",
            ],
        )


if __name__ == "__main__":
    unittest.main()
