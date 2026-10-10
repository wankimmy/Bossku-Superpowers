"""Payments."""


class PaymentFailure(Exception):
    pass


class InsufficientFundsFailure(PaymentFailure):
    pass


class FrozenWalletFailure(PaymentFailure):
    pass


class Wallet:
    def __init__(self):
        self.balance_cents = 0
        self._frozen = False

    def freeze(self):
        self._frozen = True

    def _check(self, cents):
        if not isinstance(cents, int) or isinstance(cents, bool) or cents <= 0:
            raise ValueError("amount must be a positive int")
        if self._frozen:
            raise FrozenWalletFailure("wallet is frozen")

    def deposit(self, cents):
        self._check(cents)
        self.balance_cents += cents

    def withdraw(self, cents):
        self._check(cents)
        if cents > self.balance_cents:
            raise InsufficientFundsFailure("not enough funds")
        self.balance_cents -= cents

    def balance(self):
        return self.balance_cents
