"""Project-wide error hierarchy.

Every failure this codebase raises on purpose must be an AppError
subclass, never a bare ValueError/KeyError/etc. The API wrapper only
catches AppError and turns it into a clean response; anything else
leaks a raw traceback to the caller.
"""


class AppError(Exception):
    """Base class for every error this project raises on purpose."""


class NotFoundError(AppError):
    """Raised when a booking that should exist cannot be found."""


class ConflictError(AppError):
    """Raised when an action would collide with an existing booking."""
