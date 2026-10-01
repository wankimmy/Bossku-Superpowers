"""Shared exception hierarchy for the gradebook package.

Every error raised anywhere in this package must subclass ``GradebookError``.
Feature code should never raise a bare ``ValueError``/``KeyError`` directly.
"""


class GradebookError(Exception):
    """Base class for every error raised by this package."""


class ValidationError(GradebookError):
    """An input value was the wrong type, shape, or out of range.

    The message always starts with the literal prefix ``"invalid: "``.
    """
