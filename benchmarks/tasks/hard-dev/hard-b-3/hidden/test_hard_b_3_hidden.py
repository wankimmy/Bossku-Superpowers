import unittest
from decimal import Decimal

from library.catalog import Catalog
from library.members import Members, Member
from library.loans import LibrarySystem, fee_for_billable_days


def make_system(copies=5):
    catalog = Catalog()
    catalog.add_title("ISBN1", "Dune", copies)
    members = Members()
    members.add_member("alice", "Alice")
    return LibrarySystem(catalog, members), catalog, members


class LibraryHiddenTests(unittest.TestCase):
    # ---- checkout basics ----

    def test_checkout_assigns_incrementing_ids(self):
        system, _, _ = make_system()
        id1 = system.checkout("ISBN1", "alice", 0)
        id2 = system.checkout("ISBN1", "alice", 0)
        self.assertEqual((id1, id2), (1, 2))

    def test_checkout_unknown_isbn_raises_keyerror(self):
        system, _, _ = make_system()
        with self.assertRaises(KeyError):
            system.checkout("NOPE", "alice", 0)

    def test_checkout_unknown_member_raises_keyerror(self):
        system, _, _ = make_system()
        with self.assertRaises(KeyError):
            system.checkout("ISBN1", "nobody", 0)

    def test_checkout_no_copies_raises_valueerror(self):
        system, _, _ = make_system(copies=1)
        system.checkout("ISBN1", "alice", 0)
        with self.assertRaises(ValueError):
            system.checkout("ISBN1", "alice", 0)

    def test_checkout_due_day_is_today_plus_14(self):
        system, _, _ = make_system()
        loan_id = system.checkout("ISBN1", "alice", 100)
        # Returning exactly on the due day (114) must owe nothing.
        fee = system.return_book(loan_id, 114)
        self.assertEqual(fee, Decimal("0.00"))

    # ---- member id normalization (defect) ----

    def test_member_id_lookup_case_and_whitespace_insensitive(self):
        _, _, members = make_system()
        self.assertIs(members.get("ALICE"), members.get(" alice "))

    def test_duplicate_member_case_insensitive_raises(self):
        _, _, members = make_system()
        with self.assertRaises(ValueError):
            members.add_member(" Alice ", "Alice Again")

    # ---- mutable default (defect) ----

    def test_new_member_has_own_empty_loan_history(self):
        members = Members()
        alice = members.add_member("alice", "Alice")
        alice.loan_history.append(999)
        bob = members.add_member("bob", "Bob")
        self.assertEqual(bob.loan_history, [])

    def test_loan_history_records_checkout_order(self):
        system, catalog, members = make_system()
        catalog.add_title("ISBN2", "Dune 2", 5)
        id1 = system.checkout("ISBN1", "alice", 0)
        id2 = system.checkout("ISBN2", "alice", 0)
        self.assertEqual(members.get("alice").loan_history, [id1, id2])

    # ---- returning ----

    def test_return_unknown_loan_raises_keyerror(self):
        system, _, _ = make_system()
        with self.assertRaises(KeyError):
            system.return_book(999, 0)

    def test_return_already_returned_raises_valueerror(self):
        system, _, _ = make_system()
        loan_id = system.checkout("ISBN1", "alice", 0)
        system.return_book(loan_id, 14)
        with self.assertRaises(ValueError):
            system.return_book(loan_id, 15)

    def test_return_increments_available_copies(self):
        system, catalog, _ = make_system(copies=1)
        loan_id = system.checkout("ISBN1", "alice", 0)
        self.assertEqual(catalog.available("ISBN1"), 0)
        system.return_book(loan_id, 14)
        self.assertEqual(catalog.available("ISBN1"), 1)

    # ---- grace period (defect) ----

    def test_return_on_due_day_no_fee(self):
        system, _, _ = make_system()
        loan_id = system.checkout("ISBN1", "alice", 0)
        self.assertEqual(system.return_book(loan_id, 14), Decimal("0.00"))

    def test_return_one_day_late_is_still_grace_no_fee(self):
        system, _, _ = make_system()
        loan_id = system.checkout("ISBN1", "alice", 0)
        self.assertEqual(system.return_book(loan_id, 15), Decimal("0.00"))

    def test_return_two_days_late_charges_exactly_one_billable_day(self):
        system, _, _ = make_system()
        loan_id = system.checkout("ISBN1", "alice", 0)
        self.assertEqual(system.return_book(loan_id, 16), Decimal("0.25"))

    def test_return_far_late_fee_is_capped(self):
        system, _, _ = make_system()
        loan_id = system.checkout("ISBN1", "alice", 0)
        self.assertEqual(system.return_book(loan_id, 114), Decimal("10.00"))

    def test_return_fee_at_exact_five_dollar_boundary(self):
        system, _, _ = make_system()
        loan_id = system.checkout("ISBN1", "alice", 0)
        self.assertEqual(system.return_book(loan_id, 35), Decimal("5.00"))

    # ---- fee schedule as a pure function (defect: cents truncation) ----

    def test_fee_schedule_small_values(self):
        self.assertEqual(fee_for_billable_days(0), Decimal("0.00"))
        self.assertEqual(fee_for_billable_days(1), Decimal("0.25"))
        self.assertEqual(fee_for_billable_days(2), Decimal("0.50"))
        self.assertEqual(fee_for_billable_days(3), Decimal("0.75"))
        self.assertEqual(fee_for_billable_days(5), Decimal("1.25"))
        self.assertEqual(fee_for_billable_days(7), Decimal("1.75"))

    def test_fee_schedule_cap_boundary(self):
        self.assertEqual(fee_for_billable_days(39), Decimal("9.75"))
        self.assertEqual(fee_for_billable_days(40), Decimal("10.00"))
        self.assertEqual(fee_for_billable_days(41), Decimal("10.00"))

    # ---- blocking & payments ----

    def test_blocked_member_cannot_checkout(self):
        system, _, _ = make_system()
        loan_id = system.checkout("ISBN1", "alice", 0)
        system.return_book(loan_id, 114)  # balance now 10.00
        with self.assertRaises(ValueError):
            system.checkout("ISBN1", "alice", 120)

    def test_is_blocked_reflects_new_charge_immediately(self):
        system, _, _ = make_system()
        loan_id = system.checkout("ISBN1", "alice", 0)
        self.assertFalse(system.is_blocked("alice"))  # populate cache as False
        system.return_book(loan_id, 114)  # crosses the $5 threshold
        self.assertTrue(system.is_blocked("alice"))

    def test_pay_fee_unblocks_immediately(self):
        system, _, _ = make_system()
        loan_id = system.checkout("ISBN1", "alice", 0)
        system.return_book(loan_id, 114)  # balance now 10.00, blocked
        self.assertTrue(system.is_blocked("alice"))
        system.pay_fee("alice", Decimal("6.00"))  # balance now 4.00
        self.assertFalse(system.is_blocked("alice"))
        new_loan_id = system.checkout("ISBN1", "alice", 120)
        self.assertIsNotNone(new_loan_id)

    def test_pay_fee_rejects_nonpositive_amount(self):
        system, _, members = make_system()
        members.get("alice").balance = Decimal("3.00")
        with self.assertRaises(ValueError):
            system.pay_fee("alice", Decimal("0"))
        with self.assertRaises(ValueError):
            system.pay_fee("alice", Decimal("-1.00"))

    def test_pay_fee_rejects_overpayment(self):
        system, _, members = make_system()
        members.get("alice").balance = Decimal("3.00")
        with self.assertRaises(ValueError):
            system.pay_fee("alice", Decimal("3.01"))


if __name__ == "__main__":
    unittest.main()
