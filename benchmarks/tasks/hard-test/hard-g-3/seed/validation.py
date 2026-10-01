"""Shared input-validation helpers.

Every module in this package validates arguments by calling one of these
helpers rather than writing its own ``isinstance``/range check, so every
:class:`errors.ValidationError` this package raises has the exact same
message shape. New feature code should do the same.
"""
import errors


def require_type(name, value, expected_type):
    """Raise ``ValidationError`` unless ``type(value) is expected_type``.

    Uses an exact type check, not ``isinstance`` -- a ``bool`` is rejected
    where an ``int`` is expected, since ``bool`` is a subclass of ``int``.
    """
    if type(value) is not expected_type:
        raise errors.ValidationError(
            f"invalid: {name} must be a {expected_type.__name__}"
        )
    return value


def require_nonempty_str(name, value):
    """Raise ``ValidationError`` unless ``value`` is a non-blank ``str``."""
    require_type(name, value, str)
    if value.strip() == "":
        raise errors.ValidationError(f"invalid: {name} must not be empty")
    return value


def require_list_or_tuple(name, value):
    """Raise ``ValidationError`` unless ``value`` is a ``list`` or ``tuple``."""
    if not isinstance(value, (list, tuple)):
        raise errors.ValidationError(f"invalid: {name} must be a list or tuple")
    return value


def require_nonempty_sequence(name, value):
    """Raise ``ValidationError`` unless ``value`` is a non-empty ``list``/``tuple``."""
    require_list_or_tuple(name, value)
    if len(value) == 0:
        raise errors.ValidationError(f"invalid: {name} must not be empty")
    return value


def require_positive_int(name, value):
    """Raise ``ValidationError`` unless ``value`` is an ``int`` greater than 0.

    Uses the same exact-type check as :func:`require_type`, so a ``bool``
    is rejected even though ``True`` would otherwise compare as ``1``.
    """
    require_type(name, value, int)
    if value <= 0:
        raise errors.ValidationError(f"invalid: {name} must be a positive int")
    return value
