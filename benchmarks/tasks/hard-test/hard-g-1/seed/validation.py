"""Shared input-validation helpers.

Every module in this package validates its arguments by calling one of
these helpers rather than writing its own ``isinstance``/range check, so
that every :class:`errors.ValidationError` this package raises has the
exact same message shape. New feature code should do the same -- these
helpers are not decorative, they exist so validation is consistent and so
tests can rely on (and patch) them.
"""
import decimal

import errors


def require_type(name, value, expected_type):
    """Raise ``ValidationError`` unless ``type(value) is expected_type``.

    This uses an exact type check, not ``isinstance`` -- so passing a
    ``bool`` where an ``int`` is expected is rejected, since ``bool`` is
    (confusingly) a subclass of ``int`` in Python.
    """
    if type(value) is not expected_type:
        raise errors.ValidationError(
            f"invalid: {name} must be a {expected_type.__name__}"
        )
    return value


def require_nonempty_str(name, value):
    """Raise ``ValidationError`` unless ``value`` is a non-blank ``str``.

    A string containing only whitespace counts as empty.
    """
    require_type(name, value, str)
    if value.strip() == "":
        raise errors.ValidationError(f"invalid: {name} must not be empty")
    return value


def require_list_or_tuple(name, value):
    """Raise ``ValidationError`` unless ``value`` is a ``list`` or ``tuple``."""
    if not isinstance(value, (list, tuple)):
        raise errors.ValidationError(f"invalid: {name} must be a list or tuple")
    return value


def require_ordered(name_a, value_a, name_b, value_b):
    """Raise ``ValidationError`` unless ``value_a`` is strictly before ``value_b``."""
    if not value_a < value_b:
        raise errors.ValidationError(f"invalid: {name_a} must be before {name_b}")


def require_non_negative_decimal(name, value):
    """Coerce ``value`` (``str``, ``int``, or ``Decimal``) to a ``Decimal`` and require >= 0.

    Raises ``ValidationError`` if ``value`` is a ``bool``, is not one of
    the accepted source types, does not parse to a finite decimal number,
    or parses but is negative.
    """
    if isinstance(value, bool) or not isinstance(value, (str, int, decimal.Decimal)):
        raise errors.ValidationError(f"invalid: {name} must be a number")
    try:
        parsed = decimal.Decimal(value)
    except (decimal.InvalidOperation, ValueError, TypeError):
        raise errors.ValidationError(f"invalid: {name} must be a number")
    if not parsed.is_finite():
        raise errors.ValidationError(f"invalid: {name} must be a finite number")
    if parsed < 0:
        raise errors.ValidationError(f"invalid: {name} must not be negative")
    return parsed
