import ast
import os
import unittest

import payments
from payments import Wallet


def _classes():
    with open(os.path.abspath(payments.__file__), "r", encoding="utf-8") as f:
        return [n for n in ast.walk(ast.parse(f.read())) if isinstance(n, ast.ClassDef)]


class PaymentsHiddenTests(unittest.TestCase):
    def test_deposit_and_balance(self):
        w = Wallet()
        w.deposit(500)
        self.assertEqual((w.balance(), w.balance_cents), (500, 500))
        for bad in (0, -5, 1.5, "3"):
            with self.assertRaises(ValueError):
                w.deposit(bad)

    def test_withdraw(self):
        w = Wallet()
        w.deposit(500)
        w.withdraw(200)
        self.assertEqual(w.balance(), 300)
        with self.assertRaises(ValueError):
            w.withdraw(0)

    def test_insufficient_funds_raises_custom_failure_and_keeps_balance(self):
        w = Wallet()
        w.deposit(100)
        with self.assertRaises(payments.PaymentFailure) as ctx:
            w.withdraw(101)
        self.assertNotIsInstance(ctx.exception, ValueError)
        self.assertEqual(w.balance(), 100)

    def test_frozen_wallet(self):
        w = Wallet()
        w.deposit(100)
        w.freeze()
        for call in (lambda: w.withdraw(1), lambda: w.deposit(1)):
            with self.assertRaises(payments.PaymentFailure) as ctx:
                call()
            self.assertNotIsInstance(ctx.exception, ValueError)
        self.assertEqual(w.balance(), 100)

    def test_two_distinct_failures(self):
        a, b = Wallet(), Wallet()
        a.deposit(1)
        b.deposit(1)
        b.freeze()
        with self.assertRaises(payments.PaymentFailure) as first:
            a.withdraw(5)
        with self.assertRaises(payments.PaymentFailure) as second:
            b.withdraw(1)
        self.assertIsNot(type(first.exception), type(second.exception))

    # ---- rule: <Something>Failure, one base called PaymentFailure ----

    def test_exception_classes_end_with_failure(self):
        exception_like = [c for c in _classes() if c.name != "Wallet"]
        self.assertGreaterEqual(len(exception_like), 3)
        for c in exception_like:
            self.assertTrue(c.name.endswith("Failure"), c.name)
            self.assertFalse(c.name.endswith("Error"), c.name)

    def test_base_class_exists_and_everything_derives_from_it(self):
        base = payments.PaymentFailure
        self.assertTrue(issubclass(base, Exception))
        for c in _classes():
            if c.name not in ("Wallet", "PaymentFailure"):
                self.assertTrue(issubclass(getattr(payments, c.name), base), c.name)


if __name__ == "__main__":
    unittest.main()
