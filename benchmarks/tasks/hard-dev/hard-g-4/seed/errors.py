"""Shared exception hierarchy for the ratelimit package.

Every error raised anywhere in this package must subclass ``RateLimitError``.
Feature code should never raise a bare ``ValueError``/``KeyError`` directly.

Note what is deliberately *not* here: there is no "quota exceeded"
exception. Running out of tokens is an ordinary, expected outcome of a
rate limiter, not an error condition -- see `limiter.py`'s behaviour
notes in the README.
"""


class RateLimitError(Exception):
    """Base class for every error raised by this package."""


class ValidationError(RateLimitError):
    """An input value was the wrong type, shape, or out of range.

    The message always starts with the literal prefix ``"invalid: "``.
    """
