import io
import itertools
import json
import os
import unittest

from cli import main
from repository import BookmarkRepository

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
        """5 bookmarks, then some visits:

        id1 https://a.example.com/1  "Zebra Guide"      [ref, howto]  visits=3
        id2 https://b.example.com/2  "Beta Tools"       [howto]       visits=1
        id3 https://c.example.com/3  "Charlie Notes"    [ref]         visits=0
        id4 https://d.example.com/4  "delta reference"  [ref, extra]  visits=2
        id5 https://e.example.com/5  "apple five"        []           visits=0
        """
        self.run_cli(["add", "https://a.example.com/1", "--title", "Zebra Guide",
                      "--tag", "ref", "--tag", "howto"])
        self.run_cli(["add", "https://b.example.com/2", "--title", "Beta Tools",
                      "--tag", "howto"])
        self.run_cli(["add", "https://c.example.com/3", "--title", "Charlie Notes",
                      "--tag", "ref"])
        self.run_cli(["add", "https://d.example.com/4", "--title", "delta reference",
                      "--tag", "ref", "--tag", "extra"])
        self.run_cli(["add", "https://e.example.com/5", "--title", "apple five"])
        for _ in range(3):
            self.run_cli(["visit", "1"])
        self.run_cli(["visit", "2"])
        for _ in range(2):
            self.run_cli(["visit", "4"])

    def ids_of(self, items):
        return [item["id"] for item in items]


# ---------------------------------------------------------------------------
# Preserving existing repository behavior while repository.py is extended
# ---------------------------------------------------------------------------

class ExistingBehaviorTests(CliTestBase):
    def test_id_never_reused_after_deleting_highest(self):
        repo = BookmarkRepository(self.db_path, clock=self.clock)
        repo.add("https://x.example.com/a")
        second = repo.add("https://x.example.com/b")
        repo.delete(second["id"])
        third = repo.add("https://x.example.com/c")
        self.assertEqual(third["id"], 3)

    def test_returned_bookmark_is_independent_copy(self):
        repo = BookmarkRepository(self.db_path, clock=self.clock)
        created = repo.add("https://x.example.com/d", tags=["x"])
        created["tags"].append("hack")
        fetched = repo.get(created["id"])
        self.assertEqual(fetched["tags"], ["x"])

    def test_add_is_still_idempotent_merge_on_duplicate_url(self):
        repo = BookmarkRepository(self.db_path, clock=self.clock)
        first = repo.add("https://x.example.com/e", tags=["a"])
        second = repo.add("https://x.example.com/e", tags=["b"])
        self.assertEqual(second["id"], first["id"])
        self.assertEqual(second["tags"], ["a", "b"])
        third = repo.add("https://x.example.com/e", tags=["b"])
        self.assertEqual(third["tags"], ["a", "b"])

    def test_visit_still_increments_every_call(self):
        repo = BookmarkRepository(self.db_path, clock=self.clock)
        created = repo.add("https://x.example.com/f")
        repo.visit(created["id"])
        repo.visit(created["id"])
        self.assertEqual(repo.get(created["id"])["visits"], 2)

    def test_stats_unaffected_by_list_filters(self):
        self.seed_dataset()
        self.run_cli(["list", "--min-visits", "5"])
        code, out, _ = self.run_cli(["stats"])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out), {"bookmarks": 5, "total_visits": 6})

    def test_list_and_show_do_not_modify_file(self):
        self.seed_dataset()
        with open(self.db_path, "rb") as f:
            before = f.read()
        self.run_cli(["list", "--sort-by", "title", "--page", "1", "--page-size", "2"])
        self.run_cli(["show", "1"])
        self.run_cli(["stats"])
        with open(self.db_path, "rb") as f:
            after = f.read()
        self.assertEqual(before, after)

    def test_add_rejects_bad_scheme(self):
        code, out, err = self.run_cli(["add", "ftp://example.com"])
        self.assertEqual(code, 2)
        self.assertEqual(out, "")
        self.assertIn("error: validation:", err)

    def test_show_missing_is_not_found(self):
        code, out, err = self.run_cli(["show", "999"])
        self.assertEqual(code, 3)
        self.assertEqual(out, "")
        self.assertIn("error: not_found:", err)


# ---------------------------------------------------------------------------
# Filtering
# ---------------------------------------------------------------------------

class FilterTests(CliTestBase):
    def test_tag_filter_default_is_and(self):
        self.seed_dataset()
        _, out, _ = self.run_cli(["list", "--tag", "ref", "--tag", "howto"])
        self.assertEqual(self.ids_of(json.loads(out)["items"]), [1])

    def test_any_tag_flips_to_or(self):
        self.seed_dataset()
        _, out, _ = self.run_cli(["list", "--tag", "ref", "--tag", "howto", "--any-tag"])
        self.assertEqual(self.ids_of(json.loads(out)["items"]), [1, 2, 3, 4])

    def test_any_tag_alone_with_no_tag_changes_nothing_but_still_envelopes(self):
        self.seed_dataset()
        code, out, _ = self.run_cli(["list", "--any-tag"])
        self.assertEqual(code, 0)
        data = json.loads(out)
        self.assertIsInstance(data, dict)
        self.assertEqual(self.ids_of(data["items"]), [1, 2, 3, 4, 5])

    def test_min_visits_filter(self):
        self.seed_dataset()
        _, out, _ = self.run_cli(["list", "--min-visits", "2"])
        self.assertEqual(self.ids_of(json.loads(out)["items"]), [1, 4])

    def test_min_visits_zero_keeps_everyone(self):
        self.seed_dataset()
        _, out, _ = self.run_cli(["list", "--min-visits", "0"])
        self.assertEqual(len(json.loads(out)["items"]), 5)

    def test_negative_min_visits_is_validation_error(self):
        self.seed_dataset()
        code, out, err = self.run_cli(["list", "--min-visits", "-1"])
        self.assertEqual(code, 2)
        self.assertIn("error: validation:", err)

    def test_nonnumeric_min_visits_is_validation_error(self):
        self.seed_dataset()
        code, out, err = self.run_cli(["list", "--min-visits", "lots"])
        self.assertEqual(code, 2)
        self.assertIn("error: validation:", err)

    def test_empty_tag_value_is_validation_error(self):
        self.seed_dataset()
        code, out, err = self.run_cli(["list", "--tag", ""])
        self.assertEqual(code, 2)
        self.assertIn("error: validation:", err)


# ---------------------------------------------------------------------------
# Sorting
# ---------------------------------------------------------------------------

class SortTests(CliTestBase):
    def test_sort_by_title_is_case_insensitive(self):
        self.seed_dataset()
        _, out, _ = self.run_cli(["list", "--sort-by", "title"])
        # apple(5) < Beta(2) < Charlie(3) < delta(4) < Zebra(1); a naive
        # case-sensitive sort would put "Zebra" and "Charlie" and "Beta"
        # (capitalized) before "apple"/"delta" (lowercase).
        self.assertEqual(self.ids_of(json.loads(out)["items"]), [5, 2, 3, 4, 1])

    def test_sort_by_title_descending_is_exact_reverse(self):
        self.seed_dataset()
        _, out, _ = self.run_cli(["list", "--sort-by", "title", "--order", "desc"])
        self.assertEqual(self.ids_of(json.loads(out)["items"]), [1, 4, 3, 2, 5])

    def test_sort_by_visits(self):
        self.seed_dataset()
        _, out, _ = self.run_cli(["list", "--sort-by", "visits"])
        # 0(3) == 0(5) < 1(2) < 2(4) < 3(1); tie between id3 and id5
        # (both 0 visits) stays id-ascending.
        self.assertEqual(self.ids_of(json.loads(out)["items"]), [3, 5, 2, 4, 1])

    def test_sort_by_visits_descending_keeps_tie_break_ascending(self):
        self.seed_dataset()
        _, out, _ = self.run_cli(["list", "--sort-by", "visits", "--order", "desc"])
        self.assertEqual(self.ids_of(json.loads(out)["items"]), [1, 4, 2, 3, 5])

    def test_sort_by_added_at(self):
        self.seed_dataset()
        _, out, _ = self.run_cli(["list", "--sort-by", "added_at", "--order", "desc"])
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
        self.assertEqual(self.ids_of(e2["items"]), [4, 5])
        self.assertEqual(e1["total"], 5)
        self.assertEqual(e2["total"], 5)
        self.assertEqual(e1["pages"], 2)
        self.assertEqual(e2["pages"], 2)

    def test_pagination_out_of_range_page_returns_empty_not_error(self):
        self.seed_dataset()
        code, out, _ = self.run_cli(["list", "--page", "9", "--page-size", "3"])
        self.assertEqual(code, 0)
        envelope = json.loads(out)
        self.assertEqual(envelope["items"], [])
        self.assertEqual(envelope["total"], 5)

    def test_default_page_size_is_15(self):
        self.seed_dataset()
        _, out, _ = self.run_cli(["list", "--sort-by", "id"])
        envelope = json.loads(out)
        self.assertEqual(envelope["page_size"], 15)
        self.assertEqual(envelope["pages"], 1)

    def test_page_size_over_40_is_validation_error(self):
        self.seed_dataset()
        code, out, err = self.run_cli(["list", "--page-size", "41"])
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
        # Filtering to the 3 bookmarks with >=1 visit (ids 1, 2, 4),
        # sorting by visits ascending (2 < 4 < 1 by visit count: 1, 2,
        # 3), then taking page 2 of size 1 must return id 4 - not
        # whatever sits at raw index 1 of the unfiltered id-ordered list
        # (id 2, which *does* pass the filter on its own and would
        # wrongly look plausible under a paginate-before-filter bug).
        code, out, _ = self.run_cli([
            "list", "--min-visits", "1", "--sort-by", "visits",
            "--page", "2", "--page-size", "1",
        ])
        envelope = json.loads(out)
        self.assertEqual(self.ids_of(envelope["items"]), [4])
        self.assertEqual(envelope["total"], 3)


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

    def test_list_pretty_flag_alone_still_legacy_array(self):
        self.seed_dataset()
        _, plain, _ = self.run_cli(["list"])
        _, with_pretty, _ = self.run_cli(["list", "--pretty"])
        self.assertEqual(plain, with_pretty)
        self.assertIsInstance(json.loads(with_pretty), list)

    def test_order_asc_explicit_still_triggers_envelope(self):
        self.seed_dataset()
        code, out, _ = self.run_cli(["list", "--order", "asc"])
        self.assertEqual(code, 0)
        data = json.loads(out)
        self.assertIsInstance(data, dict)
        self.assertEqual(self.ids_of(data["items"]), [1, 2, 3, 4, 5])

    def test_pretty_flag_combined_with_real_flag_still_envelopes(self):
        self.seed_dataset()
        code, out, _ = self.run_cli(["list", "--pretty", "--min-visits", "1"])
        data = json.loads(out)
        self.assertIsInstance(data, dict)
        self.assertEqual(self.ids_of(data["items"]), [1, 2, 4])

    def test_each_new_flag_alone_triggers_envelope(self):
        self.seed_dataset()
        flag_sets = [
            ["--tag", "ref"],
            ["--any-tag"],
            ["--min-visits", "0"],
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
            ["id", "url", "title", "tags", "added_at", "visits"],
        )


# ---------------------------------------------------------------------------
# README
# ---------------------------------------------------------------------------

class ReadmeTests(unittest.TestCase):
    def setUp(self):
        self.db_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "_hidden_readme4.json"
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
        self.assertIn("list --tag ref --tag howto --any-tag", text)
        self.assertIn("list --page 2 --page-size 2", text)

    def test_readme_examples_produce_their_documented_output(self):
        clock = itertools.count(1705320000.0).__next__
        self.run_cli(["add", "https://a.example.com/1", "--title", "Zebra Guide",
                      "--tag", "ref", "--tag", "howto"], clock)
        self.run_cli(["add", "https://b.example.com/2", "--title", "Beta Tools",
                      "--tag", "howto"], clock)
        self.run_cli(["add", "https://c.example.com/3", "--title", "Charlie Notes",
                      "--tag", "ref"], clock)
        self.run_cli(["add", "https://d.example.com/4", "--title", "delta reference",
                      "--tag", "ref", "--tag", "extra"], clock)
        self.run_cli(["add", "https://e.example.com/5", "--title", "apple five"], clock)

        code, out, _ = self.run_cli(["list", "--tag", "ref", "--tag", "howto", "--any-tag"], clock)
        self.assertEqual(code, 0)
        envelope = json.loads(out)
        self.assertEqual([b["id"] for b in envelope["items"]], [1, 2, 3, 4])

        code, out, _ = self.run_cli(["list", "--page", "2", "--page-size", "2"], clock)
        self.assertEqual(code, 0)
        envelope = json.loads(out)
        self.assertEqual([b["id"] for b in envelope["items"]], [3, 4])
        self.assertEqual(envelope["total"], 5)
        self.assertEqual(envelope["pages"], 3)


if __name__ == "__main__":
    unittest.main()
