"""Library members and their fee balance."""

from decimal import Decimal

BLOCK_THRESHOLD = Decimal("5.00")


class Member:
    def __init__(self, member_id, name, loan_history=[]):
        self.member_id = member_id
        self.name = name
        self.balance = Decimal("0.00")
        self.loan_history = loan_history


class Members:
    def __init__(self):
        self._members = {}

    def add_member(self, member_id, name):
        if member_id in self._members:
            raise ValueError(f"{member_id} is already a member")
        self._members[member_id] = Member(member_id, name)
        return self._members[member_id]

    def get(self, member_id):
        return self._members[member_id]
