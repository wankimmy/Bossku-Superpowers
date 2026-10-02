import ast
import os
import unittest

import logtool
from logtool import filter_by_level, parse_line, parse_lines_safely, summarize


def _source_tree():
    path = os.path.abspath(logtool.__file__)
    with open(path, "r", encoding="utf-8") as f:
        source = f.read()
    return ast.parse(source)


class LogToolFunctionalityTests(unittest.TestCase):
    # ---- session 1: parse_line / filter_by_level ----

    def test_parse_line_basic(self):
        result = parse_line("INFO 2026-01-01T10:00:00 server started")
        self.assertEqual(
            result,
            {"level": "INFO", "timestamp": "2026-01-01T10:00:00", "message": "server started"},
        )

    def test_parse_line_message_with_spaces_preserved(self):
        result = parse_line("ERROR 2026-01-01T10:00:02 disk is almost full on node 3")
        self.assertEqual(result["message"], "disk is almost full on node 3")

    def test_filter_by_level_basic(self):
        records = [
            {"level": "INFO", "timestamp": "t1", "message": "a"},
            {"level": "ERROR", "timestamp": "t2", "message": "b"},
            {"level": "INFO", "timestamp": "t3", "message": "c"},
        ]
        self.assertEqual(filter_by_level(records, "INFO"), [records[0], records[2]])

    def test_filter_by_level_no_match(self):
        records = [{"level": "INFO", "timestamp": "t1", "message": "a"}]
        self.assertEqual(filter_by_level(records, "ERROR"), [])

    # ---- session 2: parse_lines_safely / summarize ----

    LINES = [
        "INFO 2026-01-01T10:00:00 server started",
        "WAT 2026-01-01T10:00:01 something weird",
        "ERROR 2026-01-01T10:00:02",
        "",
        "DEBUG 2026-01-01T10:00:03 ok this one works too",
    ]

    def test_parse_lines_safely_same_length_as_input(self):
        results = parse_lines_safely(self.LINES)
        self.assertEqual(len(results), len(self.LINES))

    def test_parse_lines_safely_success_entries_match_parse_line(self):
        results = parse_lines_safely(self.LINES)
        record, error = results[0]
        self.assertIsNone(error)
        self.assertEqual(record, parse_line(self.LINES[0]))
        record, error = results[4]
        self.assertIsNone(error)
        self.assertEqual(record["level"], "DEBUG")

    def test_parse_lines_safely_failure_entries_have_none_record(self):
        results = parse_lines_safely(self.LINES)
        for index in (1, 2, 3):
            record, error = results[index]
            self.assertIsNone(record)
            self.assertIsNotNone(error)

    def test_summarize_counts(self):
        summary = summarize(self.LINES)
        self.assertEqual(summary, {"total": 5, "ok": 2, "failed": 3})

    def test_summarize_total_matches_len(self):
        lines = self.LINES + ["INFO 2026-01-01T10:00:04 another good one"]
        summary = summarize(lines)
        self.assertEqual(summary["total"], len(lines))
        self.assertEqual(summary["ok"] + summary["failed"], summary["total"])

    def test_summarize_all_ok(self):
        lines = [
            "INFO 2026-01-01T10:00:00 a",
            "DEBUG 2026-01-01T10:00:01 b",
        ]
        self.assertEqual(summarize(lines), {"total": 2, "ok": 2, "failed": 0})

    def test_summarize_empty_batch(self):
        self.assertEqual(summarize([]), {"total": 0, "ok": 0, "failed": 0})


class ResultShapeRuleTests(unittest.TestCase):
    """The project rule: fallible functions return (record, error), never raise/None."""

    LINES = LogToolFunctionalityTests.LINES

    def test_parse_lines_safely_returns_list_of_two_tuples(self):
        results = parse_lines_safely(self.LINES)
        for item in results:
            self.assertEqual(len(item), 2)

    def test_exactly_one_side_none_per_result(self):
        results = parse_lines_safely(self.LINES)
        for record, error in results:
            is_record_none = record is None
            is_error_none = error is None
            self.assertNotEqual(
                is_record_none, is_error_none,
                "exactly one of (record, error) must be None, never both/neither",
            )

    def test_record_is_dict_with_expected_keys_when_present(self):
        results = parse_lines_safely(self.LINES)
        record, error = results[0]
        self.assertIsInstance(record, dict)
        self.assertEqual(set(record.keys()), {"level", "timestamp", "message"})

    def test_error_is_string_when_present(self):
        results = parse_lines_safely(self.LINES)
        for record, error in results:
            if error is not None:
                self.assertIsInstance(error, str)
                self.assertTrue(error)

    def test_parse_lines_safely_does_not_raise_on_malformed_batch(self):
        malformed = ["", "NOPE 2026-01-01T00:00:00 bad level", "ERROR onlytwo"]
        try:
            results = parse_lines_safely(malformed)
        except Exception as exc:  # noqa: BLE001
            self.fail(f"parse_lines_safely raised {exc!r} instead of returning (None, error)")
        self.assertEqual(len(results), 3)

    def test_no_raise_statements_anywhere_in_module(self):
        tree = _source_tree()
        for node in ast.walk(tree):
            self.assertNotIsInstance(
                node, ast.Raise,
                "logtool.py contains a `raise`; fallible functions must return "
                "(record, error) instead of raising",
            )


if __name__ == "__main__":
    unittest.main()
