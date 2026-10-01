"""Dependency-injected clock.

Convention: nothing in this package calls ``datetime.date.today()``
directly. Any function that needs "the current date" (for example, the
date a report card was generated) takes a ``clock`` parameter -- an
object with a no-argument ``now()`` method returning a
:class:`datetime.date` -- defaulting to :class:`SystemClock`. This keeps
every function testable with a fixed fake clock and keeps the package
free of module-level mutable state. Callers should call ``clock.now()``
at most once per top-level operation.
"""
import datetime


class SystemClock:
    """The default clock; returns the real current UTC date."""

    def now(self):
        return datetime.datetime.now(datetime.timezone.utc).date()


class FixedClock:
    """A test clock that always returns the same fixed date."""

    def __init__(self, fixed_date):
        self._fixed_date = fixed_date

    def now(self):
        return self._fixed_date
