"""Shared exception hierarchy for the garage billing package.

Every error raised anywhere in this package must subclass ``GarageError``.
Feature code should never raise a bare ``ValueError``/``KeyError`` directly;
use one of the subclasses below instead, so callers can catch
``GarageError`` once and see every failure mode this package can produce.
"""


class GarageError(Exception):
    """Base class for every error raised by this package."""


class ValidationError(GarageError):
    """An input value was the wrong type, shape, or out of range.

    The message always starts with the literal prefix ``"invalid: "``
    followed by a short, specific description, e.g.
    ``"invalid: account_id must not be empty"``.
    """


class NotFoundError(GarageError):
    """A lookup (ticket, vehicle, account) found nothing.

    The message always starts with the literal prefix ``"not_found: "``.
    """


class StateError(GarageError):
    """An operation was refused because of an object's current state.

    The message always starts with the literal prefix ``"conflict: "``.
    """
