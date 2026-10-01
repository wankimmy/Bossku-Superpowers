"""The expense repository: the only place that reads/writes expenses.json.

``list_expenses()`` filters, sorts, and (optionally) paginates, always
in that order: filters are applied first, the *filtered* result is
sorted, and pagination slices the sorted result last. ``total``,
``pages``, and ``total_amount`` in its return value always describe the
filtered set as a whole - every page of the same filter reports the
same ``total``/``pages``/``total_amount`` - never just the items on the
current page. ``total_amount`` is the sum of the filtered (not just the
current page's) amounts, rounded with ``money.round_money`` - the same
function used when each expense's own amount was rounded at creation,
so a total is never computed with a different rounding rule than the
figures it's adding up.

Passing ``page=None`` means "no pagination": every matching expense
comes back as a single page (``page=1``, ``page_size=total``,
``pages=1``, or ``pages=0`` when nothing matches).

``category`` matches case-insensitively. ``date_from``/``date_to``
bound an expense's ``date``: ``date_from`` is inclusive, ``date_to`` is
*exclusive* - an expense dated exactly ``date_to`` is not included.
(`date_from == date_to` therefore matches nothing, which is not an
error.) Comparing ISO ``YYYY-MM-DD`` strings this way works because
that format sorts lexicographically in calendar order.

Sorting: the default sort key is ``id`` ascending, which is also entry
order (ids are never reused - see ``storage.py``). For any other sort
key, ties are always broken by ``id`` ascending, in *both* ``asc`` and
``desc`` order - ``order`` only flips the primary key, never the
tie-break. ``category`` sorts case-insensitively.

This method is read-only: it never calls ``save``. Every dict it,
``get``, ``add``, or ``recategorize`` hand back is a fresh copy, so
mutating a returned dict can never corrupt the repository's own state.
"""
import math

from errors import NotFoundError, ValidationError
from models import Expense
from money import round_money
from storage import load, save


class ExpenseRepository:
    def __init__(self, path):
        self.path = path
        data = load(path)
        self._next_id = data["next_id"]
        self._expenses = {}
        for raw in data["expenses"]:
            expense = Expense.from_dict(raw)
            self._expenses[expense.id] = expense

    def _save(self):
        ordered = [self._expenses[i].to_dict() for i in sorted(self._expenses)]
        save(self.path, self._next_id, ordered)

    def add(self, date, category, amount, note=None):
        expense = Expense(id=self._next_id, date=date, category=category,
                           amount=amount, note=note)
        self._expenses[expense.id] = expense
        self._next_id += 1
        self._save()
        return expense.to_dict()

    def get(self, expense_id):
        expense = self._expenses.get(expense_id)
        if expense is None:
            raise NotFoundError(f"no expense with id {expense_id}")
        return expense.to_dict()

    def recategorize(self, expense_id, new_category):
        expense = self._expenses.get(expense_id)
        if expense is None:
            raise NotFoundError(f"no expense with id {expense_id}")
        new_category = str(new_category).strip()
        if not new_category:
            raise ValidationError("category is required")
        if expense.category != new_category:
            expense.category = new_category
            self._save()
        return expense.to_dict()

    def delete(self, expense_id):
        if expense_id not in self._expenses:
            raise NotFoundError(f"no expense with id {expense_id}")
        del self._expenses[expense_id]
        self._save()

    def count(self):
        return {"count": len(self._expenses)}

    def list_expenses(self, category=None, date_from=None, date_to=None,
                       sort_by="id", order="asc", page=None, page_size=None):
        items = [self._expenses[i] for i in sorted(self._expenses)]

        if category is not None:
            target = category.lower()
            items = [e for e in items if e.category.lower() == target]
        if date_from is not None:
            items = [e for e in items if e.date >= date_from]
        if date_to is not None:
            items = [e for e in items if e.date < date_to]

        # ``items`` is already id-ascending from the initial ``sorted()``
        # above; a single stable sort (with ``reverse`` only flipping the
        # primary key) is what keeps ties in id order in both directions.
        items.sort(key=_sort_key(sort_by), reverse=(order == "desc"))

        dicts = [e.to_dict() for e in items]
        total = len(dicts)
        total_amount = round_money(sum(e.amount for e in items))

        if page is None:
            return {
                "items": dicts,
                "total": total,
                "page": 1,
                "page_size": total,
                "pages": 1 if total else 0,
                "total_amount": total_amount,
            }

        pages = math.ceil(total / page_size) if total else 0
        start = (page - 1) * page_size
        page_items = dicts[start:start + page_size]
        return {
            "items": page_items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "pages": pages,
            "total_amount": total_amount,
        }


def _sort_key(sort_by):
    if sort_by == "category":
        return lambda e: e.category.lower()
    return lambda e: getattr(e, sort_by)
