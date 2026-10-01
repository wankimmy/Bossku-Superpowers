"""The expense repository: the only place that reads/writes expenses.json.

``list_expenses()`` currently returns every expense, ordered by ``id``
ascending (which is also entry order, since ids are assigned in
increasing order and never reused - see ``storage.py``). It is
read-only: it never calls ``save``. Every dict ``list_expenses()``/
``get``/``add``/``recategorize`` hand back is a fresh copy (via
``Expense.to_dict()``), so mutating a returned dict can never corrupt
the repository's own state.

``recategorize()`` is idempotent: setting a category to the value it
already has is a no-op - calling it twice in a row with the same
argument leaves the expense exactly as the first call did.
"""
import time

from errors import NotFoundError
from models import Expense
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
            from errors import ValidationError
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

    def list_expenses(self):
        return [self._expenses[i].to_dict() for i in sorted(self._expenses)]
