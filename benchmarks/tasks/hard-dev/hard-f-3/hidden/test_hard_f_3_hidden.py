import io
import json
import os
import unittest

from cli import main
from repository import ExpenseRepository

README_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md")


class CliTestBase(unittest.TestCase):
    def setUp(self):
        self.db_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), f"_hidden_{self.id().split('.')[-1]}.json"
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

    def seed_dataset(self):
        """5 expenses:

        id1 2024-01-05  Food    12.00
        id2 2024-01-10  Travel  19.125 -> stored 19.13 (round-half-up)
        id3 2024-01-15  Food    8.50
        id4 2024-02-01  Food    1.005  -> stored 1.01 (round-half-up)
        id5 2024-01-20  Travel  20.00
        """
        self.run_cli(["add", "2024-01-05", "Food", "12.00"])
        self.run_cli(["add", "2024-01-10", "Travel", "19.125"])
        self.run_cli(["add", "2024-01-15", "Food", "8.50"])
        self.run_cli(["add", "2024-02-01", "Food", "1.005"])
        self.run_cli(["add", "2024-01-20", "Travel", "20.00"])

    def ids_of(self, items):
        return [item["id"] for item in items]


# ---------------------------------------------------------------------------
# Rounding convention (money.round_money, not plain round())
# ---------------------------------------------------------------------------

class RoundingTests(CliTestBase):
    def test_amount_is_rounded_half_up_at_creation(self):
        code, out, _ = self.run_cli(["add", "2024-01-01", "Misc", "2.125"])
        self.assertEqual(code, 0)
        # Half-up: 2.13. Python's builtin round(2.125, 2) gives 2.12
        # (round-half-to-even), which would be the wrong, careless answer.
        self.assertEqual(json.loads(out)["amount"], 2.13)

    def test_small_amount_rounds_half_up_not_down(self):
        code, out, _ = self.run_cli(["add", "2024-01-01", "Misc", "1.005"])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out)["amount"], 1.01)

    def test_total_amount_uses_the_same_rounding_as_creation(self):
        self.seed_dataset()
        _, out, _ = self.run_cli(["list", "--category", "Food"])
        envelope = json.loads(out)
        # 12.00 + 8.50 + 1.01 (already rounded at creation) = 21.51
        self.assertEqual(envelope["total_amount"], 21.51)

    def test_total_amount_consistent_across_pages_of_same_filter(self):
        self.seed_dataset()
        _, out1, _ = self.run_cli(["list", "--category", "Food", "--page", "1", "--page-size", "2"])
        _, out2, _ = self.run_cli(["list", "--category", "Food", "--page", "2", "--page-size", "2"])
        e1, e2 = json.loads(out1), json.loads(out2)
        self.assertEqual(e1["total_amount"], 21.51)
        self.assertEqual(e2["total_amount"], 21.51)
        self.assertEqual(e1["total"], 3)
        self.assertEqual(e2["total"], 3)


# ---------------------------------------------------------------------------
# Preserving existing repository behavior while repository.py is extended
# ---------------------------------------------------------------------------

class ExistingBehaviorTests(CliTestBase):
    def test_id_never_reused_after_deleting_highest(self):
        repo = ExpenseRepository(self.db_path)
        repo.add("2024-01-01", "Food", "1")
        second = repo.add("2024-01-02", "Food", "2")
        repo.delete(second["id"])
        third = repo.add("2024-01-03", "Food", "3")
        self.assertEqual(third["id"], 3)

    def test_returned_expense_is_independent_copy(self):
        repo = ExpenseRepository(self.db_path)
        created = repo.add("2024-01-01", "Food", "5", note="original")
        created["note"] = "corrupted"
        fetched = repo.get(created["id"])
        self.assertEqual(fetched["note"], "original")

    def test_recategorize_still_idempotent(self):
        repo = ExpenseRepository(self.db_path)
        created = repo.add("2024-01-01", "Food", "5")
        repo.recategorize(created["id"], "Dining")
        repo.recategorize(created["id"], "Dining")
        self.assertEqual(repo.get(created["id"])["category"], "Dining")

    def test_count_unaffected_by_list_filters(self):
        self.seed_dataset()
        self.run_cli(["list", "--category", "Food"])
        code, out, _ = self.run_cli(["count"])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out), {"count": 5})

    def test_list_and_show_do_not_modify_file(self):
        self.seed_dataset()
        with open(self.db_path, "rb") as f:
            before = f.read()
        self.run_cli(["list", "--category", "Food", "--sort-by", "amount", "--page", "1", "--page-size", "2"])
        self.run_cli(["show", "1"])
        self.run_cli(["count"])
        with open(self.db_path, "rb") as f:
            after = f.read()
        self.assertEqual(before, after)

    def test_list_unknown_currency_is_validation_error(self):
        self.seed_dataset()
        code, out, err = self.run_cli(["list", "--currency", "EUR"])
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
    def test_category_filter_case_insensitive(self):
        self.seed_dataset()
        _, out, _ = self.run_cli(["list", "--category", "food"])
        self.assertEqual(self.ids_of(json.loads(out)["items"]), [1, 3, 4])

    def test_empty_category_filter_is_validation_error(self):
        self.seed_dataset()
        code, out, err = self.run_cli(["list", "--category", ""])
        self.assertEqual(code, 2)
        self.assertIn("error: validation:", err)

    def test_date_range_from_inclusive_to_exclusive(self):
        self.seed_dataset()
        _, out, _ = self.run_cli(["list", "--from", "2024-01-10", "--to", "2024-01-20"])
        # id2 (01-10) included; id5 (01-20) excluded because --to is
        # exclusive.
        self.assertEqual(self.ids_of(json.loads(out)["items"]), [2, 3])

    def test_date_range_equal_bounds_matches_nothing(self):
        self.seed_dataset()
        code, out, _ = self.run_cli(["list", "--from", "2024-01-10", "--to", "2024-01-10"])
        self.assertEqual(code, 0)
        envelope = json.loads(out)
        self.assertEqual(envelope["items"], [])
        self.assertEqual(envelope["total_amount"], 0)

    def test_invalid_from_date_is_validation_error(self):
        self.seed_dataset()
        code, out, err = self.run_cli(["list", "--from", "not-a-date"])
        self.assertEqual(code, 2)
        self.assertEqual(out, "")
        self.assertIn("error: validation:", err)

    def test_invalid_to_date_is_validation_error(self):
        self.seed_dataset()
        code, out, err = self.run_cli(["list", "--to", "2024-99-99"])
        self.assertEqual(code, 2)
        self.assertIn("error: validation:", err)


# ---------------------------------------------------------------------------
# Sorting
# ---------------------------------------------------------------------------

class SortTests(CliTestBase):
    def test_sort_by_amount_ascending(self):
        self.seed_dataset()
        _, out, _ = self.run_cli(["list", "--sort-by", "amount"])
        # 1.01(4) < 8.50(3) < 12.00(1) < 19.13(2) < 20.00(5)
        self.assertEqual(self.ids_of(json.loads(out)["items"]), [4, 3, 1, 2, 5])

    def test_sort_by_category_case_insensitive_tie_break_ascending(self):
        self.seed_dataset()
        _, out, _ = self.run_cli(["list", "--sort-by", "category"])
        self.assertEqual(self.ids_of(json.loads(out)["items"]), [1, 3, 4, 2, 5])

    def test_sort_by_category_descending_keeps_tie_break_ascending(self):
        self.seed_dataset()
        _, out, _ = self.run_cli(["list", "--sort-by", "category", "--order", "desc"])
        self.assertEqual(self.ids_of(json.loads(out)["items"]), [2, 5, 1, 3, 4])

    def test_sort_by_date(self):
        self.seed_dataset()
        _, out, _ = self.run_cli(["list", "--sort-by", "date", "--order", "desc"])
        self.assertEqual(self.ids_of(json.loads(out)["items"]), [4, 5, 3, 2, 1])

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

    def test_pagination_out_of_range_page_returns_empty_not_error(self):
        self.seed_dataset()
        code, out, _ = self.run_cli(["list", "--page", "9", "--page-size", "3"])
        self.assertEqual(code, 0)
        envelope = json.loads(out)
        self.assertEqual(envelope["items"], [])
        self.assertEqual(envelope["total"], 5)

    def test_default_page_size_is_10(self):
        self.seed_dataset()
        _, out, _ = self.run_cli(["list", "--sort-by", "id"])
        envelope = json.loads(out)
        self.assertEqual(envelope["page_size"], 10)
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
        # Filtering to the 3 Food expenses, sorting by amount, then
        # taking page 2 of size 1 must return the 2nd-cheapest Food
        # expense (id 3) - not whatever happens to be at raw index 1
        # of the unfiltered id-ordered list (id 2, which is Travel and
        # would wrongly survive a paginate-before-filter bug as an
        # empty page once filtered).
        code, out, _ = self.run_cli([
            "list", "--category", "Food", "--sort-by", "amount",
            "--page", "2", "--page-size", "1",
        ])
        envelope = json.loads(out)
        self.assertEqual(self.ids_of(envelope["items"]), [3])
        self.assertEqual(envelope["total"], 3)
        self.assertEqual(envelope["total_amount"], 21.51)


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

    def test_list_currency_flag_alone_still_legacy_array(self):
        self.seed_dataset()
        _, plain, _ = self.run_cli(["list"])
        _, with_currency, _ = self.run_cli(["list", "--currency", "USD"])
        self.assertEqual(plain, with_currency)
        self.assertIsInstance(json.loads(with_currency), list)

    def test_order_asc_explicit_still_triggers_envelope(self):
        self.seed_dataset()
        code, out, _ = self.run_cli(["list", "--order", "asc"])
        self.assertEqual(code, 0)
        data = json.loads(out)
        self.assertIsInstance(data, dict)
        self.assertEqual(self.ids_of(data["items"]), [1, 2, 3, 4, 5])

    def test_currency_flag_combined_with_real_flag_still_envelopes(self):
        self.seed_dataset()
        code, out, _ = self.run_cli(["list", "--currency", "USD", "--category", "Food"])
        data = json.loads(out)
        self.assertIsInstance(data, dict)
        self.assertEqual(self.ids_of(data["items"]), [1, 3, 4])

    def test_each_new_flag_alone_triggers_envelope(self):
        self.seed_dataset()
        flag_sets = [
            ["--category", "Food"],
            ["--from", "2024-01-01"],
            ["--to", "2024-12-31"],
            ["--sort-by", "amount"],
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
                    set(data.keys()),
                    {"items", "total", "page", "page_size", "pages", "total_amount"},
                )

    def test_envelope_key_order_and_item_key_order(self):
        self.seed_dataset()
        _, out, _ = self.run_cli(["list", "--page", "1", "--page-size", "2"])
        envelope = json.loads(out)
        self.assertEqual(
            list(envelope.keys()),
            ["items", "total", "page", "page_size", "pages", "total_amount"],
        )
        self.assertEqual(
            list(envelope["items"][0].keys()),
            ["id", "date", "category", "amount", "note"],
        )


# ---------------------------------------------------------------------------
# README
# ---------------------------------------------------------------------------

class ReadmeTests(unittest.TestCase):
    def setUp(self):
        self.db_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "_hidden_readme3.json"
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

    def test_readme_documents_the_example_commands(self):
        with open(README_PATH, "r", encoding="utf-8") as f:
            text = f.read()
        self.assertIn("list --category Food", text)
        self.assertIn("list --from 2024-01-10 --to 2024-01-20", text)

    def test_readme_examples_produce_their_documented_output(self):
        self.run_cli(["add", "2024-01-05", "Food", "12.00"])
        self.run_cli(["add", "2024-01-10", "Travel", "19.125"])
        self.run_cli(["add", "2024-01-15", "Food", "8.50"])
        self.run_cli(["add", "2024-02-01", "Food", "1.005"])
        self.run_cli(["add", "2024-01-20", "Travel", "20.00"])

        code, out, _ = self.run_cli(["list", "--category", "Food"])
        self.assertEqual(code, 0)
        envelope = json.loads(out)
        self.assertEqual([e["id"] for e in envelope["items"]], [1, 3, 4])
        self.assertEqual(envelope["total_amount"], 21.51)

        code, out, _ = self.run_cli(["list", "--from", "2024-01-10", "--to", "2024-01-20"])
        self.assertEqual(code, 0)
        envelope = json.loads(out)
        self.assertEqual([e["id"] for e in envelope["items"]], [2, 3])
        self.assertEqual(envelope["total_amount"], 27.63)


if __name__ == "__main__":
    unittest.main()
