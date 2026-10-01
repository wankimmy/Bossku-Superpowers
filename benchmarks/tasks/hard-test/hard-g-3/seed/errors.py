"""Shared exception hierarchy for the warehouse package.

Every error raised anywhere in this package must subclass ``WarehouseError``.
Feature code should never raise a bare ``ValueError``/``KeyError`` directly.
"""


class WarehouseError(Exception):
    """Base class for every error raised by this package."""


class ValidationError(WarehouseError):
    """An input value was the wrong type, shape, or out of range.

    The message always starts with the literal prefix ``"invalid: "``.
    """


class InsufficientStockError(WarehouseError):
    """An order could not be fully satisfied when partial allocation was disallowed.

    The message always starts with the literal prefix
    ``"insufficient_stock: "``.
    """
