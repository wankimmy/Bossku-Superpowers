import os
import sys
from decimal import Decimal

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest

from library.catalog import Catalog
from library.members import Members
from library.loans import LibrarySystem


def make_system():
    catalog = Catalog()
    catalog.add_title("ISBN1", "Dune", 1)
    members = Members()
    members.add_member("alice", "Alice")
    return LibrarySystem(catalog, members), catalog, members


class LibraryTests(unittest.TestCase):
    def test_checkout_returns_loan_id_and_decrements_copies(self):
        system, catalog, _ = make_system()
        loan_id = system.checkout("ISBN1", "alice", 0)
        self.assertEqual(loan_id, 1)
        self.assertEqual(catalog.available("ISBN1"), 0)

    def test_checkout_no_copies_raises(self):
        system, _, _ = make_system()
        system.checkout("ISBN1", "alice", 0)
        with self.assertRaises(ValueError):
            system.checkout("ISBN1", "alice", 0)

    def test_return_on_time_no_fee(self):
        system, catalog, _ = make_system()
        loan_id = system.checkout("ISBN1", "alice", 0)
        fee = system.return_book(loan_id, 14)
        self.assertEqual(fee, Decimal("0.00"))
        self.assertEqual(catalog.available("ISBN1"), 1)

    def test_unknown_member_raises_keyerror(self):
        system, _, _ = make_system()
        with self.assertRaises(KeyError):
            system.checkout("ISBN1", "nobody", 0)


if __name__ == "__main__":
    unittest.main()
