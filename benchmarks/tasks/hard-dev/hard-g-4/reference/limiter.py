"""Batch request admission, built on top of buckets.refill."""
import logging
from dataclasses import dataclass, replace
from decimal import Decimal

import buckets
import clock as clock_module
import validation

_LOGGER = logging.getLogger("ratelimit.limiter")


@dataclass(frozen=True)
class RequestDecision:
    cost: int
    allowed: bool
    tokens_remaining: Decimal


@dataclass(frozen=True)
class BatchDecision:
    evaluated_at: Decimal
    bucket_after: object
    decisions: tuple


def check_requests(bucket, costs, clock=None):
    validation.require_type("bucket", bucket, buckets.TokenBucket)
    validation.require_nonempty_sequence("costs", costs)
    for index, cost in enumerate(costs):
        validation.require_positive_int(f"costs[{index}]", cost)

    active_clock = clock if clock is not None else clock_module.SystemClock()
    now = active_clock.now()

    refilled = buckets.refill(bucket, now)

    running_tokens = refilled.tokens
    decisions = []
    allowed_count = 0
    denied_count = 0
    for cost in costs:
        cost_decimal = Decimal(cost)
        if running_tokens >= cost_decimal:
            running_tokens -= cost_decimal
            allowed = True
            allowed_count += 1
        else:
            allowed = False
            denied_count += 1
        decisions.append(RequestDecision(cost=cost, allowed=allowed, tokens_remaining=running_tokens))

    bucket_after = replace(refilled, tokens=running_tokens)

    _LOGGER.info(
        f"batch bucket={bucket.bucket_id} requests={len(costs)} "
        f"allowed={allowed_count} denied={denied_count}"
    )

    return BatchDecision(
        evaluated_at=now,
        bucket_after=bucket_after,
        decisions=tuple(decisions),
    )
