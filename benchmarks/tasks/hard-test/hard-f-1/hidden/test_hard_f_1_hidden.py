import io
import itertools
import json
import os
import re
import unittest

from cli import main
from repository import IssueRepository

README_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md")


class CliTestBase(unittest.TestCase):
    def setUp(self):
        self.db_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), f"_hidden_{self.id().split('.')[-1]}.json"
        )
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        self.addCleanup(self._cleanup)
        self.clock = itertools.count(1700000000.0).__next__

    def _cleanup(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def run_cli(self, argv):
        out, err = io.StringIO(), io.StringIO()
        code = main(argv, stdout=out, stderr=err, db_path=self.db_path, clock=self.clock)
        return code, out.getvalue(), err.getvalue()

    def seed_dataset(self):
        """5 issues: id3 ends up closed, everything else open.

        id1 Write release notes   medium  open    (none)       []
        id2 Fix login bug         high    open    ren          [auth]
        id3 Crash on logout       high    closed  kai          [auth, bug]
        id4 Polish settings UI    low     open    ren          [ui]
        id5 Investigate mem leak  high    open    (none)       [bug, perf]
        """
        self.run_cli(["add", "Write release notes", "--priority", "medium"])
        self.run_cli(["add", "Fix login bug", "--priority", "high",
                      "--assignee", "ren", "--tag", "auth"])
        self.run_cli(["add", "Crash on logout", "--priority", "high",
                      "--assignee", "kai", "--tag", "auth", "--tag", "bug"])
        self.run_cli(["add", "Polish settings UI", "--priority", "low",
                      "--assignee", "ren", "--tag", "ui"])
        self.run_cli(["add", "Investigate memory leak", "--priority", "high",
                      "--tag", "bug", "--tag", "perf"])
        self.run_cli(["close", "3"])

    def ids_of(self, items):
        return [item["id"] for item in items]


# ---------------------------------------------------------------------------
# Preserving existing repository behavior while repository.py is extended
# ---------------------------------------------------------------------------

class ExistingRepositoryBehaviorTests(CliTestBase):
    def test_id_never_reused_after_deleting_highest(self):
        repo = IssueRepository(self.db_path, clock=self.clock)
        repo.add("A")
        second = repo.add("B")
        repo.delete(second["id"])
        third = repo.add("C")
        self.assertEqual(third["id"], 3)

    def test_returned_issue_is_independent_copy(self):
        repo = IssueRepository(self.db_path, clock=self.clock)
        created = repo.add("Something", tags=["x"])
        created["tags"].append("hack")
        created["title"] = "corrupted"
        fetched = repo.get(created["id"])
        self.assertEqual(fetched["tags"], ["x"])
        self.assertEqual(fetched["title"], "Something")

    def test_summary_unaffected_by_list_filters(self):
        self.seed_dataset()
        self.run_cli(["list", "--status", "closed"])
        code, out, _ = self.run_cli(["summary"])
        self.assertEqual(code, 0)
        summary = json.loads(out)
        self.assertEqual(summary["open"], 4)
        self.assertEqual(summary["closed"], 1)
        self.assertEqual(summary["total"], 5)

    def test_list_and_show_do_not_modify_file(self):
        self.seed_dataset()
        with open(self.db_path, "rb") as f:
            before = f.read()
        self.run_cli(["list", "--status", "open", "--sort-by", "title", "--page", "1", "--page-size", "2"])
        self.run_cli(["show", "1"])
        self.run_cli(["summary"])
        with open(self.db_path, "rb") as f:
            after = f.read()
        self.assertEqual(before, after)

    def test_add_unknown_priority_is_validation_error(self):
        code, out, err = self.run_cli(["add", "X", "--priority", "bogus"])
        self.assertEqual(code, 2)
        self.assertEqual(out, "")
        self.assertIn("error: validation:", err)

    def test_show_missing_is_not_found(self):
        code, out, err = self.run_cli(["show", "999"])
        self.assertEqual(code, 3)
        self.assertEqual(out, "")
        self.assertIn("error: not_found:", err)

    def test_delete_missing_is_not_found(self):
        code, out, err = self.run_cli(["delete", "999"])
        self.assertEqual(code, 3)
        self.assertIn("error: not_found:", err)


# ---------------------------------------------------------------------------
# Filtering
# ---------------------------------------------------------------------------

class FilterTests(CliTestBase):
    def test_filter_by_status_only(self):
        self.seed_dataset()
        _, out, _ = self.run_cli(["list", "--status", "open"])
        self.assertEqual(self.ids_of(json.loads(out)["items"]), [1, 2, 4, 5])

    def test_filter_by_priority_only(self):
        self.seed_dataset()
        _, out, _ = self.run_cli(["list", "--priority", "high"])
        self.assertEqual(self.ids_of(json.loads(out)["items"]), [2, 3, 5])

    def test_filter_by_assignee_exact_case_sensitive(self):
        self.seed_dataset()
        _, out, _ = self.run_cli(["list", "--assignee", "ren"])
        self.assertEqual(self.ids_of(json.loads(out)["items"]), [2, 4])

        code, out, _ = self.run_cli(["list", "--assignee", "Ren"])
        envelope = json.loads(out)
        self.assertEqual(envelope["items"], [])
        self.assertEqual(envelope["total"], 0)
        self.assertEqual(envelope["pages"], 0)
        self.assertEqual(envelope["page_size"], 20)

    def test_filter_by_assignee_empty_string_means_unassigned(self):
        self.seed_dataset()
        _, out, _ = self.run_cli(["list", "--assignee", ""])
        self.assertEqual(self.ids_of(json.loads(out)["items"]), [1, 5])

    def test_tag_filter_single(self):
        self.seed_dataset()
        _, out, _ = self.run_cli(["list", "--tag", "auth"])
        self.assertEqual(self.ids_of(json.loads(out)["items"]), [2, 3])

    def test_tag_filter_multiple_is_and_not_or(self):
        self.seed_dataset()
        _, out, _ = self.run_cli(["list", "--tag", "auth", "--tag", "bug"])
        self.assertEqual(self.ids_of(json.loads(out)["items"]), [3])

    def test_combined_filters_use_and_semantics(self):
        self.seed_dataset()
        _, out, _ = self.run_cli([
            "list", "--status", "open", "--priority", "high", "--tag", "auth",
        ])
        self.assertEqual(self.ids_of(json.loads(out)["items"]), [2])

    def test_unknown_status_filter_is_validation_error(self):
        self.seed_dataset()
        code, out, err = self.run_cli(["list", "--status", "bogus"])
        self.assertEqual(code, 2)
        self.assertEqual(out, "")
        self.assertIn("error: validation:", err)

    def test_unknown_priority_filter_is_validation_error(self):
        self.seed_dataset()
        code, out, err = self.run_cli(["list", "--priority", "bogus"])
        self.assertEqual(code, 2)
        self.assertIn("error: validation:", err)

    def test_empty_tag_filter_is_validation_error(self):
        self.seed_dataset()
        code, out, err = self.run_cli(["list", "--tag", ""])
        self.assertEqual(code, 2)
        self.assertIn("error: validation:", err)


# ---------------------------------------------------------------------------
# Sorting
# ---------------------------------------------------------------------------

class SortTests(CliTestBase):
    def test_sort_by_title_ascending(self):
        self.seed_dataset()
        _, out, _ = self.run_cli(["list", "--sort-by", "title"])
        self.assertEqual(self.ids_of(json.loads(out)["items"]), [3, 2, 5, 4, 1])

    def test_sort_by_title_descending(self):
        self.seed_dataset()
        _, out, _ = self.run_cli(["list", "--sort-by", "title", "--order", "desc"])
        self.assertEqual(self.ids_of(json.loads(out)["items"]), [1, 4, 5, 2, 3])

    def test_sort_by_status_tie_break_is_id_ascending(self):
        self.seed_dataset()
        _, out, _ = self.run_cli(["list", "--sort-by", "status"])
        # "closed" < "in_progress" < "open"; the four open issues tie and
        # must stay in id-ascending order among themselves.
        self.assertEqual(self.ids_of(json.loads(out)["items"]), [3, 1, 2, 4, 5])

    def test_sort_by_priority_uses_severity_not_alphabetical(self):
        self.seed_dataset()
        _, out, _ = self.run_cli(["list", "--sort-by", "priority"])
        # low(4) < medium(1) < high(2,3,5); alphabetical would put "high"
        # first, which is wrong.
        self.assertEqual(self.ids_of(json.loads(out)["items"]), [4, 1, 2, 3, 5])

    def test_sort_by_priority_descending_keeps_tie_break_ascending(self):
        self.seed_dataset()
        _, out, _ = self.run_cli(["list", "--sort-by", "priority", "--order", "desc"])
        # high group (2,3,5) must stay id-ascending even though the overall
        # order is reversed by severity.
        self.assertEqual(self.ids_of(json.loads(out)["items"]), [2, 3, 5, 1, 4])

    def test_sort_by_created_at(self):
        self.seed_dataset()
        _, out, _ = self.run_cli(["list", "--sort-by", "created_at", "--order", "desc"])
        self.assertEqual(self.ids_of(json.loads(out)["items"]), [5, 4, 3, 2, 1])

    def test_unknown_sort_field_is_validation_error(self):
        self.seed_dataset()
        code, out, err = self.run_cli(["list", "--sort-by", "bogus"])
        self.assertEqual(code, 2)
        self.assertIn("error: validation:", err)

    def test_unknown_order_is_validation_error(self):
        self.seed_dataset()
        code, out, err = self.run_cli(["list", "--order", "sideways"])
        self.assertEqual(code, 2)
        self.assertIn("error: validation:", err)


# ---------------------------------------------------------------------------
# Pagination
# ---------------------------------------------------------------------------

class PaginationTests(CliTestBase):
    def test_pagination_basic_slicing(self):
        self.seed_dataset()
        _, out, _ = self.run_cli(["list", "--page", "1", "--page-size", "3"])
        envelope = json.loads(out)
        self.assertEqual(self.ids_of(envelope["items"]), [1, 2, 3])
        self.assertEqual(envelope["total"], 5)
        self.assertEqual(envelope["pages"], 2)

    def test_pagination_total_and_pages_consistent_across_pages(self):
        self.seed_dataset()
        _, out1, _ = self.run_cli(["list", "--page", "1", "--page-size", "3"])
        _, out2, _ = self.run_cli(["list", "--page", "2", "--page-size", "3"])
        e1, e2 = json.loads(out1), json.loads(out2)
        self.assertEqual(e1["total"], e2["total"])
        self.assertEqual(e1["pages"], e2["pages"])
        self.assertEqual(self.ids_of(e2["items"]), [4, 5])

    def test_pagination_out_of_range_page_returns_empty_not_error(self):
        self.seed_dataset()
        code, out, err = self.run_cli(["list", "--page", "5", "--page-size", "3"])
        self.assertEqual(code, 0)
        envelope = json.loads(out)
        self.assertEqual(envelope["items"], [])
        self.assertEqual(envelope["total"], 5)
        self.assertEqual(envelope["pages"], 2)

    def test_pagination_default_page_size_is_20(self):
        self.seed_dataset()
        _, out, _ = self.run_cli(["list", "--sort-by", "id"])
        envelope = json.loads(out)
        self.assertEqual(envelope["page_size"], 20)
        self.assertEqual(envelope["page"], 1)
        self.assertEqual(envelope["pages"], 1)
        self.assertEqual(len(envelope["items"]), 5)

    def test_page_size_over_100_is_validation_error(self):
        self.seed_dataset()
        code, out, err = self.run_cli(["list", "--page-size", "101"])
        self.assertEqual(code, 2)
        self.assertIn("error: validation:", err)

    def test_page_size_zero_is_validation_error(self):
        self.seed_dataset()
        code, out, err = self.run_cli(["list", "--page-size", "0"])
        self.assertEqual(code, 2)
        self.assertIn("error: validation:", err)

    def test_nonnumeric_page_is_validation_error(self):
        self.seed_dataset()
        code, out, err = self.run_cli(["list", "--page", "abc"])
        self.assertEqual(code, 2)
        self.assertEqual(out, "")
        self.assertIn("error: validation:", err)

    def test_zero_page_is_validation_error(self):
        self.seed_dataset()
        code, out, err = self.run_cli(["list", "--page", "0"])
        self.assertEqual(code, 2)
        self.assertIn("error: validation:", err)

    def test_filter_sort_then_page_order_of_operations(self):
        self.seed_dataset()
        # Filtering to the 4 open issues, sorting by title, then taking
        # page 1 of size 2 must give the first two *open* issues in title
        # order - not "the first two issues ever created, filtered and
        # sorted afterwards" (which would wrongly include the closed id 3
        # or drop id 5).
        code, out, _ = self.run_cli([
            "list", "--status", "open", "--sort-by", "title",
            "--page", "1", "--page-size", "2",
        ])
        envelope = json.loads(out)
        self.assertEqual(self.ids_of(envelope["items"]), [2, 5])
        self.assertEqual(envelope["total"], 4)
        self.assertEqual(envelope["pages"], 2)


# ---------------------------------------------------------------------------
# Legacy vs. paginated output switch
# ---------------------------------------------------------------------------

class OutputFormatSwitchTests(CliTestBase):
    def test_list_no_flags_returns_legacy_array(self):
        self.seed_dataset()
        code, out, _ = self.run_cli(["list"])
        self.assertEqual(code, 0)
        data = json.loads(out)
        self.assertIsInstance(data, list)
        self.assertEqual(self.ids_of(data), [1, 2, 3, 4, 5])

    def test_list_json_flag_alone_still_legacy_array(self):
        self.seed_dataset()
        _, plain, _ = self.run_cli(["list"])
        _, with_json, _ = self.run_cli(["list", "--json"])
        self.assertEqual(plain, with_json)
        self.assertIsInstance(json.loads(with_json), list)

    def test_order_asc_explicit_still_triggers_envelope(self):
        self.seed_dataset()
        code, out, _ = self.run_cli(["list", "--order", "asc"])
        self.assertEqual(code, 0)
        data = json.loads(out)
        self.assertIsInstance(data, dict)
        self.assertEqual(self.ids_of(data["items"]), [1, 2, 3, 4, 5])

    def test_json_flag_combined_with_real_flag_still_envelopes(self):
        self.seed_dataset()
        code, out, _ = self.run_cli(["list", "--json", "--status", "open"])
        data = json.loads(out)
        self.assertIsInstance(data, dict)
        self.assertEqual(self.ids_of(data["items"]), [1, 2, 4, 5])

    def test_each_new_flag_alone_triggers_envelope(self):
        self.seed_dataset()
        flag_sets = [
            ["--status", "open"],
            ["--priority", "high"],
            ["--assignee", "ren"],
            ["--tag", "auth"],
            ["--sort-by", "title"],
            ["--order", "desc"],
            ["--page", "1"],
            ["--page-size", "10"],
        ]
        for flags in flag_sets:
            with self.subTest(flags=flags):
                code, out, err = self.run_cli(["list", *flags])
                self.assertEqual(code, 0, err)
                data = json.loads(out)
                self.assertIsInstance(data, dict)
                self.assertEqual(
                    set(data.keys()), {"items", "total", "page", "page_size", "pages"}
                )

    def test_envelope_key_order_and_item_key_order(self):
        self.seed_dataset()
        _, out, _ = self.run_cli(["list", "--page", "1", "--page-size", "2"])
        envelope = json.loads(out)
        self.assertEqual(
            list(envelope.keys()), ["items", "total", "page", "page_size", "pages"]
        )
        self.assertEqual(
            list(envelope["items"][0].keys()),
            ["id", "title", "status", "priority", "assignee", "tags", "created_at"],
        )


# ---------------------------------------------------------------------------
# README
# ---------------------------------------------------------------------------

class ReadmeTests(unittest.TestCase):
    def setUp(self):
        self.db_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "_hidden_readme.json"
        )
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        self.addCleanup(self._cleanup)

    def _cleanup(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def run_cli(self, argv, clock):
        out, err = io.StringIO(), io.StringIO()
        code = main(argv, stdout=out, stderr=err, db_path=self.db_path, clock=clock)
        return code, out.getvalue(), err.getvalue()

    def test_readme_documents_the_example_commands(self):
        with open(README_PATH, "r", encoding="utf-8") as f:
            text = f.read()
        self.assertIn("list --status open --sort-by priority", text)
        self.assertIn("list --page 2 --page-size 1", text)

    def test_readme_examples_produce_their_documented_output(self):
        clock = itertools.count(1705320000.0).__next__
        self.run_cli(["add", "Fix login bug", "--priority", "high",
                      "--assignee", "ren", "--tag", "auth"], clock)
        self.run_cli(["add", "Write onboarding docs", "--priority", "low",
                      "--tag", "docs"], clock)
        self.run_cli(["add", "Crash on logout", "--priority", "high",
                      "--assignee", "kai", "--tag", "auth", "--tag", "bug"], clock)
        self.run_cli(["close", "2"], clock)

        code, out, _ = self.run_cli(["list", "--status", "open", "--sort-by", "priority"], clock)
        self.assertEqual(code, 0)
        envelope = json.loads(out)
        self.assertEqual([i["id"] for i in envelope["items"]], [1, 3])
        self.assertEqual(envelope["total"], 2)
        self.assertEqual(envelope["pages"], 1)

        code, out, _ = self.run_cli(["list", "--page", "2", "--page-size", "1"], clock)
        self.assertEqual(code, 0)
        envelope = json.loads(out)
        self.assertEqual([i["id"] for i in envelope["items"]], [2])
        self.assertEqual(envelope["items"][0]["status"], "closed")
        self.assertEqual(envelope["total"], 3)
        self.assertEqual(envelope["pages"], 3)


if __name__ == "__main__":
    unittest.main()
