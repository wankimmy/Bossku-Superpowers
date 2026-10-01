"""Dependency-injected clock.

Convention: nothing in this package calls ``time.time()`` directly. Any
function that needs "the current time" takes a ``clock`` parameter -- an
object with a no-argument ``now()`` method returning a
:class:`decimal.Decimal` count of seconds (never a ``float``, so refill
math stays exact) -- defaulting to :class:`SystemClock`. This keeps
every function testable with a fixed fake clock and keeps the package
free of module-level mutable state. Callers should call ``clock.now()``
at most once per top-level operation.
"""
import time
from decimal import Decimal


class SystemClock:
    """The default clock; returns the real current time as seconds."""

    def now(self):
        return Decimal(str(time.time()))


class FixedClock:
    """A test clock that always returns the same fixed ``Decimal`` time."""

    def __init__(self, fixed_time):
        self._fixed_time = fixed_time

    def now(self):
        return self._fixed_time
