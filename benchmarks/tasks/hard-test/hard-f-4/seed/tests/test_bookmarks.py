import io
import json
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cli import main


class BookmarkCliTests(unittest.TestCase):
    def setUp(self):
        self.db_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "_tmp_bookmarks.json"
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
        code, out, _ = self.run_cli([
            "add", "https://example.com/a", "--title", "Example A", "--tag", "ref",
        ])
        self.assertEqual(code, 0)
        bookmark = json.loads(out)
        self.assertEqual(bookmark["url"], "https://example.com/a")
        self.assertEqual(bookmark["title"], "Example A")
        self.assertEqual(bookmark["tags"], ["ref"])
        self.assertEqual(bookmark["visits"], 0)

        code, out, _ = self.run_cli(["show", str(bookmark["id"])])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out), bookmark)

    def test_add_without_title_defaults_to_url(self):
        code, out, _ = self.run_cli(["add", "https://example.com/b"])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out)["title"], "https://example.com/b")

    def test_add_rejects_bad_scheme(self):
        code, out, err = self.run_cli(["add", "ftp://example.com"])
        self.assertEqual(code, 2)
        self.assertEqual(out, "")
        self.assertIn("validation", err)

    def test_add_same_url_again_merges_instead_of_duplicating(self):
        _, out, _ = self.run_cli(["add", "https://example.com/c", "--tag", "x"])
        first = json.loads(out)
        code, out, _ = self.run_cli(["add", "https://example.com/c", "--tag", "y"])
        self.assertEqual(code, 0)
        second = json.loads(out)
        self.assertEqual(second["id"], first["id"])
        self.assertEqual(second["tags"], ["x", "y"])

        code, out, _ = self.run_cli(["list"])
        self.assertEqual(len(json.loads(out)), 1)

    def test_visit_increments_each_time(self):
        _, out, _ = self.run_cli(["add", "https://example.com/d"])
        bid = json.loads(out)["id"]
        self.run_cli(["visit", str(bid)])
        code, out, _ = self.run_cli(["visit", str(bid)])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out)["visits"], 2)

    def test_delete_then_show_not_found(self):
        _, out, _ = self.run_cli(["add", "https://example.com/e"])
        bid = json.loads(out)["id"]
        self.run_cli(["delete", str(bid)])
        code, out, err = self.run_cli(["show", str(bid)])
        self.assertEqual(code, 3)
        self.assertEqual(out, "")
        self.assertIn("not_found", err)

    def test_stats(self):
        _, out, _ = self.run_cli(["add", "https://example.com/f"])
        bid = json.loads(out)["id"]
        self.run_cli(["add", "https://example.com/g"])
        self.run_cli(["visit", str(bid)])
        code, out, _ = self.run_cli(["stats"])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out), {"bookmarks": 2, "total_visits": 1})


if __name__ == "__main__":
    unittest.main()
