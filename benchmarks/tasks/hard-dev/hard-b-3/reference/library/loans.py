"""Checkout, return, and fee tracking tying catalog + members together."""

from decimal import Decimal

from .members import BLOCK_THRESHOLD

STANDARD_LOAN_DAYS = 14
DAILY_FEE_CENTS = 25
FEE_CAP = Decimal("10.00")


class Loan:
    __slots__ = ("loan_id", "isbn", "member_id", "due_day", "returned")

    def __init__(self, loan_id, isbn, member_id, due_day):
        self.loan_id = loan_id
        self.isbn = isbn
        self.member_id = member_id
        self.due_day = due_day
        self.returned = False


def fee_for_billable_days(billable_days):
    """25 cents per billable late day, capped at FEE_CAP."""
    cents = billable_days * DAILY_FEE_CENTS
    fee = Decimal(cents) / Decimal(100)
    return min(fee, FEE_CAP)


class LibrarySystem:
    def __init__(self, catalog, members):
        self.catalog = catalog
        self.members = members
        self._loans = {}
        self._next_loan_id = 1
        self._block_cache = {}

    def _compute_blocked(self, member_id):
        member = self.members.get(member_id)
        return member.balance >= BLOCK_THRESHOLD

    def is_blocked(self, member_id):
        if member_id not in self._block_cache:
            self._block_cache[member_id] = self._compute_blocked(member_id)
        return self._block_cache[member_id]

    def checkout(self, isbn, member_id, today):
        member = self.members.get(member_id)
        if self.is_blocked(member_id):
            raise ValueError("member has unpaid fees")
        self.catalog.checkout_copy(isbn)
        loan_id = self._next_loan_id
        self._next_loan_id += 1
        due_day = today + STANDARD_LOAN_DAYS
        self._loans[loan_id] = Loan(loan_id, isbn, member_id, due_day)
        member.loan_history.append(loan_id)
        return loan_id

    def return_book(self, loan_id, today):
        if loan_id not in self._loans:
            raise KeyError(loan_id)
        loan = self._loans[loan_id]
        if loan.returned:
            raise ValueError("loan already returned")

        self.catalog.return_copy(loan.isbn)
        loan.returned = True

        days_late = today - loan.due_day
        billable_days = max(0, days_late - 1)
        fee = fee_for_billable_days(billable_days)
        if fee > 0:
            member = self.members.get(loan.member_id)
            member.balance += fee
            self._block_cache.pop(loan.member_id, None)

        return fee

    def pay_fee(self, member_id, amount):
        member = self.members.get(member_id)
        if amount <= 0:
            raise ValueError("payment amount must be positive")
        if amount > member.balance:
            raise ValueError("payment exceeds current balance")
        member.balance -= amount
        self._block_cache.pop(member_id, None)
