import ast
import inspect
import io
import json
import unittest
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HIDDEN_FILENAME = Path(__file__).name


def _project_py_files(exclude_names=frozenset()):
    """All first-party .py files in the merged project, excluding this
    grader file and anything under a tests/ directory."""
    files = []
    for path in sorted(ROOT.rglob("*.py")):
        if path.name == HIDDEN_FILENAME:
            continue
        if path.name in exclude_names:
            continue
        if "tests" in path.relative_to(ROOT).parts[:-1]:
            continue
        files.append(path)
    return files


def _bare_print_calls(tree):
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "print":
            yield node


class ReportRuleTests(unittest.TestCase):
    """The project rule: never print()/logging directly, use report()."""

    def test_no_print_calls_outside_report_helper(self):
        # report.py is the one sanctioned place that is allowed to print,
        # since it IS the stdout-writing helper everything else must call.
        for path in _project_py_files(exclude_names={"report.py"}):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            offenders = list(_bare_print_calls(tree))
            self.assertEqual(
                offenders,
                [],
                f"{path.name} calls print() directly; it should call report() instead",
            )

    def test_no_logging_module_anywhere(self):
        for path in _project_py_files():
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    names = {alias.name for alias in node.names}
                    self.assertNotIn("logging", names, f"{path.name} imports logging")
                if isinstance(node, ast.ImportFrom):
                    self.assertNotEqual(
                        node.module, "logging", f"{path.name} imports from logging"
                    )

    def test_report_helper_has_event_and_kwargs_signature(self):
        import report as report_module

        sig = inspect.signature(report_module.report)
        params = list(sig.parameters.values())
        self.assertGreaterEqual(len(params), 1, "report() needs an `event` parameter")
        self.assertTrue(
            any(p.kind == inspect.Parameter.VAR_KEYWORD for p in params),
            "report() needs a **fields parameter",
        )

    def test_report_emits_exactly_one_json_line(self):
        import report as report_module

        buf = io.StringIO()
        with redirect_stdout(buf):
            report_module.report("widget_count", count=3, unit="boxes")
        lines = [line for line in buf.getvalue().splitlines() if line.strip()]
        self.assertEqual(len(lines), 1)
        payload = json.loads(lines[0])
        self.assertEqual(payload["event"], "widget_count")
        self.assertEqual(payload["count"], 3)
        self.assertEqual(payload["unit"], "boxes")

    def test_summarize_import_stdout_is_json_lines_only(self):
        import importer

        rows = [
            {"order_id": "A1", "amount": 10},
            {"order_id": "A1", "amount": 10},
            {"order_id": "A2", "amount": 5},
            {"amount": 7},
        ]
        buf = io.StringIO()
        with redirect_stdout(buf):
            importer.summarize_import(rows)
        lines = [line for line in buf.getvalue().splitlines() if line.strip()]
        self.assertGreaterEqual(len(lines), 1, "summarize_import should report something")
        for line in lines:
            parsed = json.loads(line)  # fails if a plain-text print() leaked through
            self.assertIn("event", parsed)


class ImporterFunctionalityTests(unittest.TestCase):
    def test_import_rows_accepts_valid_rows_in_order(self):
        import importer

        rows = [{"order_id": "A1", "amount": 10}, {"order_id": "A2", "amount": 20}]
        accepted, rejected = importer.import_rows(rows)
        self.assertEqual(accepted, rows)
        self.assertEqual(rejected, [])

    def test_import_rows_rejects_missing_order_id(self):
        import importer

        rows = [{"amount": 10}]
        accepted, rejected = importer.import_rows(rows)
        self.assertEqual(accepted, [])
        self.assertEqual(rejected, rows)

    def test_import_rows_rejects_missing_amount(self):
        import importer

        rows = [{"order_id": "A1"}]
        accepted, rejected = importer.import_rows(rows)
        self.assertEqual(accepted, [])
        self.assertEqual(rejected, rows)

    def test_import_rows_empty_input(self):
        import importer

        self.assertEqual(importer.import_rows([]), ([], []))

    def test_dedupe_rows_keeps_first_occurrence(self):
        import importer

        rows = [
            {"order_id": "A1", "amount": 10},
            {"order_id": "A2", "amount": 5},
            {"order_id": "A1", "amount": 99},
        ]
        unique_rows, duplicate_rows = importer.dedupe_rows(rows)
        self.assertEqual(unique_rows, [rows[0], rows[1]])
        self.assertEqual(duplicate_rows, [rows[2]])

    def test_dedupe_rows_no_duplicates(self):
        import importer

        rows = [{"order_id": "A1", "amount": 1}, {"order_id": "A2", "amount": 2}]
        unique_rows, duplicate_rows = importer.dedupe_rows(rows)
        self.assertEqual(unique_rows, rows)
        self.assertEqual(duplicate_rows, [])

    def test_summarize_import_counts(self):
        import importer

        rows = [
            {"order_id": "A1", "amount": 10},
            {"order_id": "A1", "amount": 10},
            {"order_id": "A2", "amount": 5},
            {"amount": 7},
        ]
        buf = io.StringIO()
        with redirect_stdout(buf):
            summary = importer.summarize_import(rows)
        self.assertEqual(
            summary, {"total": 4, "accepted": 2, "duplicates": 1, "rejected": 1}
        )

    def test_summarize_import_counts_are_internally_consistent(self):
        import importer

        rows = [{"order_id": str(i), "amount": i} for i in range(5)]
        rows.append({"order_id": "0", "amount": 999})  # duplicate
        rows.append({"no": "id"})  # rejected
        buf = io.StringIO()
        with redirect_stdout(buf):
            summary = importer.summarize_import(rows)
        self.assertEqual(
            summary["accepted"] + summary["duplicates"] + summary["rejected"],
            summary["total"],
        )
        self.assertEqual(summary["total"], len(rows))


if __name__ == "__main__":
    unittest.main()
