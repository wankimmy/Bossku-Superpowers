import io
import json
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cli import main


class ExpenseCliTests(unittest.TestCase):
    def setUp(self):
        self.db_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "_tmp_expenses.json"
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
        code, out, _ = self.run_cli(["add", "2024-01-10", "Food", "12.5", "--note", "lunch"])
        self.assertEqual(code, 0)
        expense = json.loads(out)
        self.assertEqual(expense["date"], "2024-01-10")
        self.assertEqual(expense["category"], "Food")
        self.assertEqual(expense["amount"], 12.5)
        self.assertEqual(expense["note"], "lunch")

        code, out, _ = self.run_cli(["show", str(expense["id"])])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out), expense)

    def test_add_invalid_date_is_validation_error(self):
        code, out, err = self.run_cli(["add", "not-a-date", "Food", "10"])
        self.assertEqual(code, 2)
        self.assertEqual(out, "")
        self.assertIn("validation", err)

    def test_add_nonpositive_amount_is_validation_error(self):
        code, out, err = self.run_cli(["add", "2024-01-10", "Food", "0"])
        self.assertEqual(code, 2)
        self.assertIn("validation", err)

    def test_recategorize_is_idempotent(self):
        _, out, _ = self.run_cli(["add", "2024-01-10", "Food", "10"])
        eid = json.loads(out)["id"]
        code, out, _ = self.run_cli(["recategorize", str(eid), "Dining"])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out)["category"], "Dining")
        code, out, _ = self.run_cli(["recategorize", str(eid), "Dining"])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out)["category"], "Dining")

    def test_delete_then_show_not_found(self):
        _, out, _ = self.run_cli(["add", "2024-01-10", "Food", "10"])
        eid = json.loads(out)["id"]
        self.run_cli(["delete", str(eid)])
        code, out, err = self.run_cli(["show", str(eid)])
        self.assertEqual(code, 3)
        self.assertEqual(out, "")
        self.assertIn("not_found", err)

    def test_list_returns_all_in_id_order(self):
        self.run_cli(["add", "2024-01-01", "Food", "1"])
        self.run_cli(["add", "2024-01-02", "Travel", "2"])
        code, out, _ = self.run_cli(["list"])
        self.assertEqual(code, 0)
        expenses = json.loads(out)
        self.assertEqual([e["category"] for e in expenses], ["Food", "Travel"])

    def test_count(self):
        self.run_cli(["add", "2024-01-01", "Food", "1"])
        self.run_cli(["add", "2024-01-02", "Travel", "2"])
        code, out, _ = self.run_cli(["count"])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out), {"count": 2})


if __name__ == "__main__":
    unittest.main()
