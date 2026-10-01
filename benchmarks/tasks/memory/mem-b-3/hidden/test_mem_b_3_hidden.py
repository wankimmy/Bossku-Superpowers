import ast
import unittest
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HIDDEN_FILENAME = Path(__file__).name


def _project_py_files():
    files = []
    for path in sorted(ROOT.rglob("*.py")):
        if path.name == HIDDEN_FILENAME:
            continue
        if "tests" in path.relative_to(ROOT).parts[:-1]:
            continue
        files.append(path)
    return files


class DecimalRuleTests(unittest.TestCase):
    """The project rule: money is always Decimal, never float or int."""

    def test_no_float_literals_anywhere(self):
        for path in _project_py_files():
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Constant) and isinstance(node.value, float):
                    self.fail(f"{path.name} contains a float literal: {node.value!r}")

    def test_no_float_calls_anywhere(self):
        for path in _project_py_files():
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if (
                    isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Name)
                    and node.func.id == "float"
                ):
                    self.fail(f"{path.name} calls float(...)")

    def test_decimal_module_is_used(self):
        source = (ROOT / "invoice.py").read_text(encoding="utf-8")
        tree = ast.parse(source)
        imported_decimal = any(
            isinstance(node, ast.ImportFrom) and node.module == "decimal"
            for node in ast.walk(tree)
        )
        self.assertTrue(imported_decimal, "invoice.py should import from decimal")

    def test_total_returns_decimal_not_float_or_int(self):
        from invoice import Invoice

        inv = Invoice()
        inv.add_line_item("widget", Decimal("1.50"), 2)
        total = inv.total()
        self.assertIsInstance(total, Decimal)
        self.assertNotIsInstance(total, float)

    def test_split_evenly_returns_only_decimals(self):
        # session-2 trap: a forgetful split tends to use float division
        # or integer cents instead of Decimal.
        from invoice import Invoice, split_evenly

        inv = Invoice()
        inv.add_line_item("rent", Decimal("10.00"), 1)
        shares = split_evenly(inv, 3)
        for share in shares:
            self.assertIsInstance(share, Decimal)
            self.assertNotIsInstance(share, float)

    def test_round_cents_half_even_tie_down(self):
        from invoice import round_cents

        # 2.005 is exactly between 2.00 and 2.01; HALF_EVEN picks 2.00
        # (even digit), HALF_UP would pick 2.01.
        self.assertEqual(round_cents(Decimal("2.005")), Decimal("2.00"))

    def test_round_cents_half_even_tie_up(self):
        from invoice import round_cents

        # 2.025 is exactly between 2.02 and 2.03; HALF_EVEN picks 2.02
        # (even digit), HALF_UP would pick 2.03.
        self.assertEqual(round_cents(Decimal("2.025")), Decimal("2.02"))


class InvoiceFunctionalityTests(unittest.TestCase):
    def test_total_sums_line_items(self):
        from invoice import Invoice

        inv = Invoice()
        inv.add_line_item("widget", Decimal("1.50"), 2)
        inv.add_line_item("gadget", Decimal("4.00"), 1)
        self.assertEqual(inv.total(), Decimal("7.00"))

    def test_total_with_no_items_is_zero(self):
        from invoice import Invoice

        self.assertEqual(Invoice().total(), Decimal("0"))

    def test_round_cents_simple_rounding(self):
        from invoice import round_cents

        self.assertEqual(round_cents(Decimal("1.004")), Decimal("1.00"))
        self.assertEqual(round_cents(Decimal("1.006")), Decimal("1.01"))

    def test_split_evenly_exact_division(self):
        from invoice import Invoice, split_evenly

        inv = Invoice()
        inv.add_line_item("stuff", Decimal("9.00"), 1)
        self.assertEqual(split_evenly(inv, 3), [Decimal("3.00")] * 3)

    def test_split_evenly_distributes_remainder_to_first_people(self):
        from invoice import Invoice, split_evenly

        inv = Invoice()
        inv.add_line_item("rent", Decimal("10.00"), 1)
        self.assertEqual(
            split_evenly(inv, 3), [Decimal("3.34"), Decimal("3.33"), Decimal("3.33")]
        )

    def test_split_evenly_sums_exactly_to_total_general_case(self):
        from invoice import Invoice, round_cents, split_evenly

        inv = Invoice()
        inv.add_line_item("odd", Decimal("100.01"), 1)
        shares = split_evenly(inv, 7)
        self.assertEqual(len(shares), 7)
        self.assertEqual(sum(shares), round_cents(inv.total()))

    def test_split_evenly_returns_n_shares(self):
        from invoice import Invoice, split_evenly

        inv = Invoice()
        inv.add_line_item("thing", Decimal("5.00"), 1)
        self.assertEqual(len(split_evenly(inv, 4)), 4)

    def test_split_evenly_rejects_non_positive_n(self):
        from invoice import Invoice, split_evenly

        inv = Invoice()
        inv.add_line_item("thing", Decimal("5.00"), 1)
        with self.assertRaises(Exception):
            split_evenly(inv, 0)


if __name__ == "__main__":
    unittest.main()
