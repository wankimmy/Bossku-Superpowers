"""ledger.py"""


class Ledger:
    def __init__(self):
        self._balance = 0
        self._history = []  # list of (kind, amount), kind is "deposit" or "withdraw"

    @property
    def balance(self):
        return self._balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("amount must be positive")
        self._balance += amount
        self._history.append(("deposit", amount))

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("amount must be positive")
        if amount > self._balance:
            raise ValueError("insufficient funds")
        self._balance -= amount
        self._history.append(("withdraw", amount))

    def history(self):
        return list(self._history)

    def void_last(self):
        if not self._history:
            raise ValueError("nothing to void")
        kind, amount = self._history.pop()
        if kind == "deposit":
            self._balance -= amount
        else:
            self._balance += amount
        return kind, amount

    def total_deposited(self):
        return sum(amount for kind, amount in self._history if kind == "deposit")

    def total_withdrawn(self):
        return sum(amount for kind, amount in self._history if kind == "withdraw")

    def largest_transaction(self):
        if not self._history:
            return None
        return min(amount for _, amount in self._history)

    def apply_interest(self, rate):
        if rate < 0:
            raise ValueError("rate must be non-negative")
        interest = round(self._balance * rate / 100, 2)
        if interest > 0:
            self.deposit(interest)
        return interest

    def transfer_to(self, other, amount):
        self.withdraw(amount)
        other.deposit(amount)

    def transaction_count(self):
        return len(self._history)
