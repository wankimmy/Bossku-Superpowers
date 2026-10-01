import io
import itertools
import json
import os
import unittest

from cli import main
from repository import ContactRepository

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
        """5 contacts:

        id1 Ada Lovelace    ada@acme.io      Acme    [vip]
        id2 Bob Zephyr      bob@example.com  acme    [eng]
        id3 Carol Analyst   (none)           Zenith  [vip, eng]
        id4 Dana Admin      (none)           (none)  []
        id5 Eve Young       eve@zenith.io    Zenith  [vip]
        """
        self.run_cli(["add", "Ada Lovelace", "--email", "ada@acme.io",
                      "--company", "Acme", "--tag", "vip"])
        self.run_cli(["add", "Bob Zephyr", "--email", "bob@example.com",
                      "--company", "acme", "--tag", "eng"])
        self.run_cli(["add", "Carol Analyst", "--company", "Zenith",
                      "--tag", "vip", "--tag", "eng"])
        self.run_cli(["add", "Dana Admin"])
        self.run_cli(["add", "Eve Young", "--email", "eve@zenith.io",
                      "--company", "Zenith", "--tag", "vip"])

    def ids_of(self, items):
        return [item["id"] for item in items]


# ---------------------------------------------------------------------------
# Preserving existing repository behavior while repository.py is extended
# ---------------------------------------------------------------------------

class ExistingBehaviorTests(CliTestBase):
    def test_id_never_reused_after_deleting_highest(self):
        repo = ContactRepository(self.db_path, clock=self.clock)
        repo.add("A")
        second = repo.add("B")
        repo.delete(second["id"])
        third = repo.add("C")
        self.assertEqual(third["id"], 3)

    def test_returned_contact_is_independent_copy(self):
        repo = ContactRepository(self.db_path, clock=self.clock)
        created = repo.add("Someone", tags=["x"])
        created["tags"].append("hack")
        created["full_name"] = "corrupted"
        fetched = repo.get(created["id"])
        self.assertEqual(fetched["tags"], ["x"])
        self.assertEqual(fetched["full_name"], "Someone")

    def test_tag_is_still_idempotent_and_rejects_empty(self):
        repo = ContactRepository(self.db_path, clock=self.clock)
        created = repo.add("Someone")
        repo.tag(created["id"], "vip")
        repo.tag(created["id"], "vip")
        self.assertEqual(repo.get(created["id"])["tags"], ["vip"])
        with self.assertRaises(Exception):
            repo.tag(created["id"], "")

    def test_count_unaffected_by_list_filters(self):
        self.seed_dataset()
        self.run_cli(["list", "--company", "Zenith"])
        code, out, _ = self.run_cli(["count"])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out), {"count": 5})

    def test_list_and_show_do_not_modify_file(self):
        self.seed_dataset()
        with open(self.db_path, "rb") as f:
            before = f.read()
        self.run_cli(["list", "--company", "Zenith", "--sort-by", "name", "--page", "1", "--page-size", "1"])
        self.run_cli(["show", "1"])
        self.run_cli(["count"])
        with open(self.db_path, "rb") as f:
            after = f.read()
        self.assertEqual(before, after)

    def test_add_invalid_phone_is_validation_error(self):
        code, out, err = self.run_cli(["add", "X", "--phone", "call-me-maybe"])
        self.assertEqual(code, 2)
        self.assertEqual(out, "")
        self.assertIn("error: validation:", err)

    def test_show_missing_is_not_found(self):
        code, out, err = self.run_cli(["show", "999"])
        self.assertEqual(code, 3)
        self.assertEqual(out, "")
        self.assertIn("error: not_found:", err)

    def test_list_unknown_format_is_validation_error(self):
        self.seed_dataset()
        code, out, err = self.run_cli(["list", "--format", "xml"])
        self.assertEqual(code, 2)
        self.assertEqual(out, "")
        self.assertIn("error: validation:", err)


# ---------------------------------------------------------------------------
# Search and filters
# ---------------------------------------------------------------------------

class SearchFilterTests(CliTestBase):
    def test_q_searches_name_email_and_company_case_insensitively(self):
        self.seed_dataset()
        _, out, _ = self.run_cli(["list", "--q", "acme"])
        self.assertEqual(self.ids_of(json.loads(out)["items"]), [1, 2])

    def test_q_does_not_search_phone(self):
        self.seed_dataset()
        self.run_cli(["add", "Phoned Person", "--phone", "5551234"])
        _, out, _ = self.run_cli(["list", "--q", "5551234"])
        self.assertEqual(json.loads(out)["items"], [])

    def test_q_combines_with_tag_using_and(self):
        self.seed_dataset()
        _, out, _ = self.run_cli(["list", "--q", "acme", "--tag", "vip"])
        self.assertEqual(self.ids_of(json.loads(out)["items"]), [1])

    def test_tag_filter_multiple_is_and_not_or(self):
        self.seed_dataset()
        _, out, _ = self.run_cli(["list", "--tag", "vip", "--tag", "eng"])
        self.assertEqual(self.ids_of(json.loads(out)["items"]), [3])

    def test_company_filter_is_case_insensitive_exact(self):
        self.seed_dataset()
        _, out, _ = self.run_cli(["list", "--company", "ACME"])
        self.assertEqual(self.ids_of(json.loads(out)["items"]), [1, 2])

    def test_company_empty_string_means_no_company(self):
        self.seed_dataset()
        _, out, _ = self.run_cli(["list", "--company", ""])
        self.assertEqual(self.ids_of(json.loads(out)["items"]), [4])

    def test_company_omitted_applies_no_filter(self):
        self.seed_dataset()
        _, out, _ = self.run_cli(["list", "--sort-by", "id"])
        self.assertEqual(len(json.loads(out)["items"]), 5)

    def test_empty_tag_value_is_validation_error(self):
        self.seed_dataset()
        code, out, err = self.run_cli(["list", "--tag", ""])
        self.assertEqual(code, 2)
        self.assertIn("error: validation:", err)


# ---------------------------------------------------------------------------
# Sorting
# ---------------------------------------------------------------------------

class SortTests(CliTestBase):
    def test_sort_by_name_uses_last_word_not_full_string(self):
        self.seed_dataset()
        _, out, _ = self.run_cli(["list", "--sort-by", "name"])
        # admin(4) < analyst(3) < lovelace(1) < young(5) < zephyr(2)
        self.assertEqual(self.ids_of(json.loads(out)["items"]), [4, 3, 1, 5, 2])

    def test_sort_by_company_no_company_sorts_first(self):
        self.seed_dataset()
        _, out, _ = self.run_cli(["list", "--sort-by", "company"])
        self.assertEqual(self.ids_of(json.loads(out)["items"]), [4, 1, 2, 3, 5])

    def test_sort_by_company_descending_keeps_tie_break_ascending(self):
        self.seed_dataset()
        _, out, _ = self.run_cli(["list", "--sort-by", "company", "--order", "desc"])
        # zenith group {3,5} then acme group {1,2} then "" {4}, each tie
        # group internally id-ascending despite the overall reversal.
        self.assertEqual(self.ids_of(json.loads(out)["items"]), [3, 5, 1, 2, 4])

    def test_sort_by_created_at_descending(self):
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
    def test_pagination_basic_slicing_and_totals(self):
        self.seed_dataset()
        _, out1, _ = self.run_cli(["list", "--page", "1", "--page-size", "3"])
        _, out2, _ = self.run_cli(["list", "--page", "2", "--page-size", "3"])
        e1, e2 = json.loads(out1), json.loads(out2)
        self.assertEqual(self.ids_of(e1["items"]), [1, 2, 3])
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

    def test_default_page_size_is_25(self):
        self.seed_dataset()
        _, out, _ = self.run_cli(["list", "--sort-by", "id"])
        envelope = json.loads(out)
        self.assertEqual(envelope["page_size"], 25)
        self.assertEqual(envelope["pages"], 1)

    def test_page_size_over_50_is_validation_error(self):
        self.seed_dataset()
        code, out, err = self.run_cli(["list", "--page-size", "51"])
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
        # Filtering to company=Zenith (ids 3, 5) then sorting by name
        # ("analyst" < "young") then taking page 1 of size 1 must return
        # id 3 - not an empty page from slicing the raw id-ordered list
        # [1, 2] first and filtering/sorting afterwards.
        code, out, _ = self.run_cli([
            "list", "--company", "Zenith", "--sort-by", "name",
            "--page", "1", "--page-size", "1",
        ])
        envelope = json.loads(out)
        self.assertEqual(self.ids_of(envelope["items"]), [3])
        self.assertEqual(envelope["total"], 2)
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

    def test_list_format_json_flag_alone_still_legacy_array(self):
        self.seed_dataset()
        _, plain, _ = self.run_cli(["list"])
        _, with_format, _ = self.run_cli(["list", "--format", "json"])
        self.assertEqual(plain, with_format)
        self.assertIsInstance(json.loads(with_format), list)

    def test_order_asc_explicit_still_triggers_envelope(self):
        self.seed_dataset()
        code, out, _ = self.run_cli(["list", "--order", "asc"])
        self.assertEqual(code, 0)
        data = json.loads(out)
        self.assertIsInstance(data, dict)
        self.assertEqual(self.ids_of(data["items"]), [1, 2, 3, 4, 5])

    def test_format_flag_combined_with_real_flag_still_envelopes(self):
        self.seed_dataset()
        code, out, _ = self.run_cli(["list", "--format", "json", "--company", "Zenith"])
        data = json.loads(out)
        self.assertIsInstance(data, dict)
        self.assertEqual(self.ids_of(data["items"]), [3, 5])

    def test_each_new_flag_alone_triggers_envelope(self):
        self.seed_dataset()
        flag_sets = [
            ["--q", "a"],
            ["--tag", "vip"],
            ["--company", "Zenith"],
            ["--sort-by", "name"],
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
            ["id", "full_name", "email", "phone", "company", "tags", "created_at"],
        )


# ---------------------------------------------------------------------------
# README
# ---------------------------------------------------------------------------

class ReadmeTests(unittest.TestCase):
    def setUp(self):
        self.db_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "_hidden_readme2.json"
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
        self.assertIn("list --company Acme --sort-by name", text)
        self.assertIn("list --page 2 --page-size 2", text)

    def test_readme_examples_produce_their_documented_output(self):
        clock = itertools.count(1705320000.0).__next__
        self.run_cli(["add", "Ada Lovelace", "--email", "ada@acme.io",
                      "--company", "Acme", "--tag", "vip"], clock)
        self.run_cli(["add", "Bob Zephyr", "--email", "bob@example.com",
                      "--company", "acme", "--tag", "eng"], clock)
        self.run_cli(["add", "Carol Analyst", "--company", "Zenith",
                      "--tag", "vip", "--tag", "eng"], clock)
        self.run_cli(["add", "Dana Admin"], clock)

        code, out, _ = self.run_cli(["list", "--company", "Acme", "--sort-by", "name"], clock)
        self.assertEqual(code, 0)
        envelope = json.loads(out)
        self.assertEqual([c["id"] for c in envelope["items"]], [1, 2])
        self.assertEqual(envelope["total"], 2)

        code, out, _ = self.run_cli(["list", "--page", "2", "--page-size", "2"], clock)
        self.assertEqual(code, 0)
        envelope = json.loads(out)
        self.assertEqual([c["id"] for c in envelope["items"]], [3, 4])
        self.assertEqual(envelope["total"], 4)
        self.assertEqual(envelope["pages"], 2)


if __name__ == "__main__":
    unittest.main()
