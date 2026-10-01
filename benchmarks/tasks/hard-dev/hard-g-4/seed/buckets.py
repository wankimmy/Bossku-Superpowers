"""Token-bucket primitives.

This module is already correct and in production use -- do not change its
behavior. It exists here so new features can reuse it instead of
re-deriving a bucket's refill amount by hand.
"""
from dataclasses import dataclass, replace
from decimal import Decimal

import errors
import validation


@dataclass(frozen=True)
class TokenBucket:
    """An immutable snapshot of one rate-limit bucket.

    Fields:
        bucket_id: ``str`` unique identifier for this bucket.
        capacity: ``int`` maximum number of tokens the bucket can hold.
        refill_rate: ``Decimal`` tokens added per second of elapsed time.
        tokens: ``Decimal`` tokens currently available (``0`` to ``capacity``).
        last_refill_at: ``Decimal`` seconds-since-epoch timestamp of the
            last time this bucket's ``tokens``/``last_refill_at`` were
            computed.
    """

    bucket_id: str
    capacity: int
    refill_rate: Decimal
    tokens: Decimal
    last_refill_at: Decimal


def refill(bucket, now):
    """Return a *new* ``TokenBucket`` with tokens topped up to ``now``.

    ``now`` must not be before ``bucket.last_refill_at``
    (``errors.ValidationError`` otherwise -- this package's clocks only
    ever move forward). The elapsed time (``now - last_refill_at``) is
    multiplied by ``refill_rate`` and added to ``tokens``, capped at
    ``capacity``; ``last_refill_at`` becomes ``now``. ``bucket`` itself is
    never mutated -- callers must use the returned bucket going forward.
    """
    validation.require_type("bucket", bucket, TokenBucket)
    validation.require_type("now", now, Decimal)
    if now < bucket.last_refill_at:
        raise errors.ValidationError("invalid: now must not be before last_refill_at")

    elapsed = now - bucket.last_refill_at
    new_tokens = min(Decimal(bucket.capacity), bucket.tokens + elapsed * bucket.refill_rate)
    return replace(bucket, tokens=new_tokens, last_refill_at=now)
