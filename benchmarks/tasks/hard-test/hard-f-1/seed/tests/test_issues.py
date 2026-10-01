import io
import json
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cli import main


class IssueCliTests(unittest.TestCase):
    def setUp(self):
        self.db_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "_tmp_issues.json"
        )
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        self.addCleanup(self._cleanup)

    def _cleanup(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def run_cli(self, argv):
        out, err = io.StringIO(), io.StringIO()
        code = main(argv, stdout=out, stderr=err, db_path=self.db_path)
        return code, out.getvalue(), err.getvalue()

    def test_add_and_show(self):
        code, out, _ = self.run_cli(["add", "Fix login bug"])
        self.assertEqual(code, 0)
        issue = json.loads(out)
        self.assertEqual(issue["title"], "Fix login bug")
        self.assertEqual(issue["status"], "open")
        self.assertEqual(issue["priority"], "medium")
        self.assertIsNone(issue["assignee"])
        self.assertEqual(issue["tags"], [])

        code, out, _ = self.run_cli(["show", str(issue["id"])])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out), issue)

    def test_add_with_priority_assignee_and_tags(self):
        code, out, _ = self.run_cli([
            "add", "Add dark mode",
            "--priority", "low",
            "--assignee", "ren",
            "--tag", "ui", "--tag", "ui", "--tag", "polish",
        ])
        self.assertEqual(code, 0)
        issue = json.loads(out)
        self.assertEqual(issue["priority"], "low")
        self.assertEqual(issue["assignee"], "ren")
        self.assertEqual(issue["tags"], ["ui", "polish"])

    def test_close_and_delete(self):
        _, out, _ = self.run_cli(["add", "Temp"])
        issue_id = json.loads(out)["id"]

        code, out, _ = self.run_cli(["close", str(issue_id)])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out)["status"], "closed")

        code, out, _ = self.run_cli(["delete", str(issue_id)])
        self.assertEqual(code, 0)

        code, out, err = self.run_cli(["show", str(issue_id)])
        self.assertEqual(code, 3)
        self.assertEqual(out, "")
        self.assertIn("not_found", err)

    def test_list_returns_all_issues_in_id_order(self):
        self.run_cli(["add", "First"])
        self.run_cli(["add", "Second"])
        code, out, _ = self.run_cli(["list"])
        self.assertEqual(code, 0)
        issues = json.loads(out)
        self.assertEqual([i["title"] for i in issues], ["First", "Second"])

    def test_summary_counts(self):
        _, out, _ = self.run_cli(["add", "A"])
        a_id = json.loads(out)["id"]
        self.run_cli(["add", "B"])
        self.run_cli(["close", str(a_id)])

        code, out, _ = self.run_cli(["summary"])
        self.assertEqual(code, 0)
        summary = json.loads(out)
        self.assertEqual(summary["closed"], 1)
        self.assertEqual(summary["open"], 1)
        self.assertEqual(summary["total"], 2)

    def test_add_missing_title_is_validation_error(self):
        code, out, err = self.run_cli(["add", "   "])
        self.assertEqual(code, 2)
        self.assertEqual(out, "")
        self.assertIn("validation", err)


if __name__ == "__main__":
    unittest.main()
