"""The ``Expense`` entity.

Fields:

- ``id``: positive ``int``, assigned by the repository and never reused
  (see ``storage.py``).
- ``date``: a string in ``YYYY-MM-DD`` form that is a real calendar date
  (validated with ``datetime.date.fromisoformat``).
- ``category``: non-empty string (leading/trailing whitespace stripped).
  Its original case is kept in storage; matching it is case-insensitive
  (see ``repository.py``).
- ``amount``: a positive number, rounded to the nearest cent with
  ``money.round_money`` at creation time - once rounded here, it is
  never rounded differently anywhere else in this project.
- ``note``: a string, or ``None``. Whitespace-only input is normalized
  to ``None``.

``to_dict()`` always returns a *new* dict, so callers can freely mutate
what they get back without ever corrupting the ``Expense``'s own state.
"""
import datetime

from errors import ValidationError
from money import round_money


class Expense:
    __slots__ = ("id", "date", "category", "amount", "note")

    def __init__(self, id, date, category, amount, note=None):
        try:
            datetime.date.fromisoformat(date)
        except (TypeError, ValueError) as exc:
            raise ValidationError(f"invalid date: {date!r}") from exc

        category = str(category).strip()
        if not category:
            raise ValidationError("category is required")

        try:
            amount = float(amount)
        except (TypeError, ValueError) as exc:
            raise ValidationError(f"invalid amount: {amount!r}") from exc
        if amount <= 0:
            raise ValidationError(f"amount must be positive: {amount!r}")

        note = str(note).strip() if note is not None else None
        note = note or None

        self.id = id
        self.date = date
        self.category = category
        self.amount = round_money(amount)
        self.note = note

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date,
            "category": self.category,
            "amount": self.amount,
            "note": self.note,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            date=data["date"],
            category=data["category"],
            amount=data["amount"],
            note=data.get("note"),
        )
