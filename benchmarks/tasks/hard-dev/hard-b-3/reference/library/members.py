"""Library members and their fee balance."""

from decimal import Decimal

BLOCK_THRESHOLD = Decimal("5.00")


def _key(member_id):
    return member_id.strip().lower()


class Member:
    def __init__(self, member_id, name, loan_history=None):
        self.member_id = member_id
        self.name = name
        self.balance = Decimal("0.00")
        self.loan_history = [] if loan_history is None else loan_history


class Members:
    def __init__(self):
        self._members = {}

    def add_member(self, member_id, name):
        key = _key(member_id)
        if key in self._members:
            raise ValueError(f"{member_id} is already a member")
        self._members[key] = Member(member_id, name)
        return self._members[key]

    def get(self, member_id):
        return self._members[_key(member_id)]
