import ast
import os
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
MODELS = os.path.join(HERE, "shop", "models")


class ShopHiddenTests(unittest.TestCase):
    def test_invoice(self):
        from shop.models.invoice import Invoice
        inv = Invoice("INV-1", "Aisyah", 5000)
        self.assertEqual((inv.number, inv.customer, inv.total_cents), ("INV-1", "Aisyah", 5000))
        self.assertFalse(inv.is_paid())
        self.assertTrue(Invoice("INV-2", "Wei", 1, True).is_paid())

    def test_currency(self):
        from shop.models.currency import Currency
        self.assertEqual([c.name for c in Currency], ["MYR", "SGD", "USD"])
        self.assertEqual(Currency.SGD.value, "SGD")

    def test_line_item(self):
        from shop.models.currency import Currency
        from shop.models.line_item import LineItem
        item = LineItem("AB-1234", 3, 250)
        self.assertEqual((item.sku, item.qty, item.unit_cents), ("AB-1234", 3, 250))
        self.assertEqual(item.total_cents(), 750)
        self.assertIs(item.currency, Currency.MYR)
        self.assertIs(LineItem("X", 1, 1, Currency.USD).currency, Currency.USD)

    def test_credit_note(self):
        from shop.models.credit_note import CreditNote
        note = CreditNote("CN-1", "INV-1", 300)
        self.assertEqual((note.number, note.invoice_number, note.amount_cents), ("CN-1", "INV-1", 300))

    # ---- rule: one class per file, file name = snake_case of class ----

    def test_expected_files_exist(self):
        for name in ("invoice.py", "currency.py", "line_item.py", "credit_note.py"):
            self.assertTrue(os.path.isfile(os.path.join(MODELS, name)), name)

    def test_no_catch_all_models_module(self):
        self.assertFalse(os.path.exists(os.path.join(HERE, "shop", "models.py")))

    def test_one_class_per_file_named_after_it(self):
        expected = {"invoice.py": "Invoice", "currency.py": "Currency", "line_item.py": "LineItem",
                    "credit_note.py": "CreditNote"}
        for name in sorted(os.listdir(MODELS)):
            if not name.endswith(".py") or name == "__init__.py":
                continue
            with open(os.path.join(MODELS, name), "r", encoding="utf-8") as f:
                classes = [n.name for n in ast.walk(ast.parse(f.read())) if isinstance(n, ast.ClassDef)]
            self.assertEqual(len(classes), 1, name)
            if name in expected:
                self.assertEqual(classes, [expected[name]])


if __name__ == "__main__":
    unittest.main()
