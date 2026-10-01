import unittest

from ledger import Ledger


class DepositWithdrawTests(unittest.TestCase):
    def test_deposit_increases_balance(self):
        l = Ledger()
        l.deposit(100)
        l.deposit(50)
        self.assertEqual(l.balance, 150)

    def test_withdraw_decreases_balance(self):
        l = Ledger()
        l.deposit(100)
        l.withdraw(40)
        self.assertEqual(l.balance, 60)

    def test_withdraw_exact_balance_is_allowed(self):
        l = Ledger()
        l.deposit(100)
        l.withdraw(100)
        self.assertEqual(l.balance, 0)

    def test_withdraw_more_than_balance_raises_and_is_unchanged(self):
        l = Ledger()
        l.deposit(50)
        with self.assertRaises(ValueError):
            l.withdraw(51)
        self.assertEqual(l.balance, 50)

    def test_non_positive_amounts_raise(self):
        l = Ledger()
        l.deposit(10)
        for amount in (0, -5):
            with self.subTest(amount=amount):
                with self.assertRaises(ValueError):
                    l.deposit(amount)
                with self.assertRaises(ValueError):
                    l.withdraw(amount)


class HistoryTests(unittest.TestCase):
    def test_history_records_in_order(self):
        l = Ledger()
        l.deposit(100)
        l.withdraw(30)
        self.assertEqual(l.history(), [("deposit", 100), ("withdraw", 30)])

    def test_history_is_a_copy(self):
        l = Ledger()
        l.deposit(100)
        snapshot = l.history()
        snapshot.append(("deposit", 999))
        snapshot.clear()
        self.assertEqual(l.history(), [("deposit", 100)])
        self.assertEqual(l.balance, 100)

    def test_transaction_count(self):
        l = Ledger()
        self.assertEqual(l.transaction_count(), 0)
        l.deposit(10)
        l.withdraw(5)
        self.assertEqual(l.transaction_count(), 2)


class VoidLastTests(unittest.TestCase):
    def test_void_last_deposit_reduces_balance_and_removes_entry(self):
        l = Ledger()
        l.deposit(100)
        l.deposit(20)
        kind, amount = l.void_last()
        self.assertEqual((kind, amount), ("deposit", 20))
        self.assertEqual(l.balance, 100)
        self.assertEqual(l.history(), [("deposit", 100)])

    def test_void_last_withdraw_restores_balance(self):
        l = Ledger()
        l.deposit(100)
        l.withdraw(30)
        l.void_last()
        self.assertEqual(l.balance, 100)
        self.assertEqual(l.history(), [("deposit", 100)])

    def test_void_last_only_undoes_successful_transactions(self):
        l = Ledger()
        l.deposit(100)
        with self.assertRaises(ValueError):
            l.withdraw(1000)
        l.void_last()
        self.assertEqual(l.balance, 0)
        self.assertEqual(l.history(), [])

    def test_void_on_empty_history_raises(self):
        l = Ledger()
        with self.assertRaises(ValueError):
            l.void_last()


class AggregateTests(unittest.TestCase):
    def test_total_deposited_and_withdrawn(self):
        l = Ledger()
        l.deposit(100)
        l.deposit(50)
        l.withdraw(30)
        self.assertEqual(l.total_deposited(), 150)
        self.assertEqual(l.total_withdrawn(), 30)

    def test_totals_exclude_voided_entries(self):
        l = Ledger()
        l.deposit(100)
        l.deposit(50)
        l.void_last()
        self.assertEqual(l.total_deposited(), 100)

    def test_largest_transaction(self):
        l = Ledger()
        l.deposit(10)
        l.deposit(500)
        l.withdraw(20)
        self.assertEqual(l.largest_transaction(), 500)

    def test_largest_transaction_on_empty_ledger_is_none(self):
        l = Ledger()
        self.assertIsNone(l.largest_transaction())


class InterestTests(unittest.TestCase):
    def test_apply_interest_adds_percentage_of_balance(self):
        l = Ledger()
        l.deposit(200)
        interest = l.apply_interest(10)
        self.assertEqual(interest, 20.0)
        self.assertEqual(l.balance, 220.0)

    def test_apply_interest_on_zero_balance_adds_nothing(self):
        l = Ledger()
        interest = l.apply_interest(10)
        self.assertEqual(interest, 0)
        self.assertEqual(l.history(), [])

    def test_negative_rate_raises(self):
        l = Ledger()
        l.deposit(100)
        with self.assertRaises(ValueError):
            l.apply_interest(-1)


class TransferTests(unittest.TestCase):
    def test_transfer_moves_funds_between_ledgers(self):
        src = Ledger()
        dst = Ledger()
        src.deposit(100)
        src.transfer_to(dst, 40)
        self.assertEqual(src.balance, 60)
        self.assertEqual(dst.balance, 40)

    def test_failed_transfer_leaves_destination_unchanged(self):
        src = Ledger()
        dst = Ledger()
        src.deposit(10)
        with self.assertRaises(ValueError):
            src.transfer_to(dst, 1000)
        self.assertEqual(dst.balance, 0)
        self.assertEqual(src.balance, 10)


if __name__ == "__main__":
    unittest.main()
