"""Core parking-session fee engine.

This module is already correct and in production use -- do not change its
behavior. It exists here so new features can reuse it instead of
re-deriving a session's fee by hand.
"""
import datetime
from dataclasses import dataclass
from decimal import Decimal
import math

import errors
import money
import validation


@dataclass(frozen=True)
class RateCard:
    """An immutable billing rate card for one garage.

    Fields:
        hourly_rate: ``Decimal`` charged per full or partial hour billed.
        max_fee: ``Decimal`` absolute ceiling on a single session's fee.
        grace_minutes: ``int`` -- a session lasting this many minutes or
            fewer is always free.
        round_increment_minutes: ``int`` -- billed duration is rounded UP
            to the next multiple of this many minutes.
    """

    hourly_rate: Decimal
    max_fee: Decimal
    grace_minutes: int
    round_increment_minutes: int


@dataclass(frozen=True)
class SessionRecord:
    """One vehicle's parking session.

    ``entry_time`` and ``exit_time`` are :class:`datetime.datetime`
    values; this dataclass performs no validation of its own -- that
    happens in :func:`compute_session_fee` and in any feature code that
    accepts a list of these.
    """

    vehicle_id: str
    entry_time: datetime.datetime
    exit_time: datetime.datetime


def compute_session_fee(rate_card, session):
    """Compute the fee for one parking session, as a ``Decimal`` with 2dp.

    Rules, applied in this order:

    1. ``session.exit_time`` must be strictly after ``session.entry_time``
       (``errors.ValidationError`` otherwise).
    2. If the total duration is less than or equal to
       ``rate_card.grace_minutes``, the fee is exactly ``Decimal("0.00")``
       -- no rounding or hourly rate ever applies to a grace-period stay.
    3. Otherwise the duration is rounded UP to the next multiple of
       ``rate_card.round_increment_minutes`` (a duration that is already
       an exact multiple is not rounded further).
    4. The rounded duration is billed at
       ``ceil(rounded_minutes / 60) * rate_card.hourly_rate`` -- i.e. by
       the full or partial hour.
    5. The result is capped at ``rate_card.max_fee`` (never reduced
       below it if it's already under the cap).
    6. The final fee is rounded with :func:`money.round_money` before
       being returned.
    """
    validation.require_type("rate_card", rate_card, RateCard)
    validation.require_type("session", session, SessionRecord)
    validation.require_ordered(
        "entry_time", session.entry_time, "exit_time", session.exit_time
    )

    total_minutes = (session.exit_time - session.entry_time).total_seconds() / 60
    if total_minutes <= rate_card.grace_minutes:
        return Decimal("0.00")

    increment = rate_card.round_increment_minutes
    rounded_minutes = math.ceil(total_minutes / increment) * increment
    hours = math.ceil(rounded_minutes / 60)
    fee = Decimal(hours) * rate_card.hourly_rate
    fee = min(fee, rate_card.max_fee)
    return money.round_money(fee)
