"""Exception hierarchy and this project's error-message convention.

Every error raised anywhere in this project is an instance of
``LedgerError``. Its string form is always ``"<category>: <detail>"``,
where ``category`` is a class attribute fixed per exception type. The
CLI (``cli.py``) relies on exactly this: it prints ``f"error: {exc}"``
to stderr and exits with ``constants.EXIT_CODES[type(exc).category]``.

Any new error raised from CLI-facing code - including validation of new
command-line flags - must reuse one of the exception types below rather
than raising a bare ``ValueError``/``KeyError``/etc., or that convention
(and the exit-code table in the README) silently stops holding.
"""


class LedgerError(Exception):
    category = "error"

    def __init__(self, detail):
        self.detail = detail
        super().__init__(f"{self.category}: {detail}")


class ValidationError(LedgerError):
    """Bad input: a missing/invalid field, filter value, sort key, or
    page."""

    category = "validation"


class NotFoundError(LedgerError):
    """No expense exists with the given id."""

    category = "not_found"


class StorageError(LedgerError):
    """The on-disk expense file could not be read or written."""

    category = "storage"
