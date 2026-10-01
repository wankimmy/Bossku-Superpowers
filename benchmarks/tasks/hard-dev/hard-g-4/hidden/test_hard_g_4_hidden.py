import dataclasses
import logging
import unittest
from decimal import Decimal
from unittest import mock

import buckets
import clock
import errors
import limiter


def B(bucket_id="b1", capacity=10, refill_rate="2", tokens="4", last_refill_at="1000"):
    return buckets.TokenBucket(
        bucket_id=bucket_id,
        capacity=capacity,
        refill_rate=Decimal(refill_rate),
        tokens=Decimal(tokens),
        last_refill_at=Decimal(last_refill_at),
    )


class _ListHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.records = []

    def emit(self, record):
        self.records.append(record)


class BucketsExistingBehaviorTests(unittest.TestCase):
    """buckets.py already works; these pin its behavior so it stays untouched."""

    def setUp(self):
        self.bucket = B(capacity=10, refill_rate="2", tokens="4", last_refill_at="1000")

    def test_refill_adds_elapsed_times_rate(self):
        updated = buckets.refill(self.bucket, Decimal("1001"))
        self.assertEqual(updated.tokens, Decimal("6"))
        self.assertEqual(updated.last_refill_at, Decimal("1001"))

    def test_refill_caps_at_capacity(self):
        updated = buckets.refill(self.bucket, Decimal("1100"))
        self.assertEqual(updated.tokens, Decimal("10"))

    def test_refill_result_tokens_is_always_decimal_even_when_capped(self):
        # A naive min(int_capacity, decimal_tokens) returns a plain int
        # when the capacity is the smaller value -- tokens must stay Decimal.
        updated = buckets.refill(self.bucket, Decimal("1100"))
        self.assertIs(type(updated.tokens), Decimal)

    def test_refill_does_not_mutate_original_bucket(self):
        buckets.refill(self.bucket, Decimal("1001"))
        self.assertEqual(self.bucket.tokens, Decimal("4"))
        self.assertEqual(self.bucket.last_refill_at, Decimal("1000"))

    def test_now_before_last_refill_raises(self):
        with self.assertRaises(errors.RateLimitError):
            buckets.refill(self.bucket, Decimal("999"))

    def test_wrong_bucket_type_raises(self):
        with self.assertRaises(errors.RateLimitError):
            buckets.refill("not-a-bucket", Decimal("1001"))

    def test_bucket_is_frozen(self):
        with self.assertRaises(dataclasses.FrozenInstanceError):
            self.bucket.tokens = Decimal("0")


class SequentialBatchTests(unittest.TestCase):
    def setUp(self):
        self.full_bucket = B(capacity=10, tokens="10", last_refill_at="1000")

    def test_allowed_request_deducts_cost(self):
        r = limiter.check_requests(self.full_bucket, [7], clock=clock.FixedClock(Decimal("1000")))
        self.assertEqual(r.decisions[0].allowed, True)
        self.assertEqual(r.decisions[0].tokens_remaining, Decimal("3"))

    def test_denied_request_does_not_affect_running_total(self):
        r = limiter.check_requests(self.full_bucket, [7, 5, 3], clock=clock.FixedClock(Decimal("1000")))
        self.assertEqual(
            [(d.cost, d.allowed, d.tokens_remaining) for d in r.decisions],
            [(7, True, Decimal("3")), (5, False, Decimal("3")), (3, True, Decimal("0"))],
        )

    def test_batch_does_not_stop_on_first_denial(self):
        r = limiter.check_requests(self.full_bucket, [100, 1], clock=clock.FixedClock(Decimal("1000")))
        self.assertEqual(len(r.decisions), 2)
        self.assertFalse(r.decisions[0].allowed)
        self.assertTrue(r.decisions[1].allowed)

    def test_cost_exceeding_capacity_is_always_denied(self):
        r = limiter.check_requests(self.full_bucket, [50], clock=clock.FixedClock(Decimal("1000")))
        self.assertFalse(r.decisions[0].allowed)
        self.assertEqual(r.decisions[0].tokens_remaining, Decimal("10"))

    def test_decisions_are_in_same_order_as_costs(self):
        r = limiter.check_requests(self.full_bucket, [3, 9, 1], clock=clock.FixedClock(Decimal("1000")))
        self.assertEqual([d.cost for d in r.decisions], [3, 9, 1])

    def test_bucket_after_tokens_equals_final_running_total(self):
        r = limiter.check_requests(self.full_bucket, [7, 5, 3], clock=clock.FixedClock(Decimal("1000")))
        self.assertEqual(r.bucket_after.tokens, r.decisions[-1].tokens_remaining)
        self.assertEqual(r.bucket_after.tokens, Decimal("0"))


class RefillIntegrationTests(unittest.TestCase):
    def test_refill_applied_once_before_batch_not_per_request(self):
        low_bucket = B(capacity=10, tokens="0", refill_rate="1", last_refill_at="1000")
        r = limiter.check_requests(low_bucket, [3, 3], clock=clock.FixedClock(Decimal("1005")))
        # Only 5 tokens ever enter the bucket (one refill of 5s * 1/s), so
        # the second identical request must be denied, not separately refilled.
        self.assertEqual(
            [(d.cost, d.allowed, d.tokens_remaining) for d in r.decisions],
            [(3, True, Decimal("2")), (3, False, Decimal("2"))],
        )

    def test_evaluated_at_equals_clock_value(self):
        r = limiter.check_requests(
            B(tokens="10", last_refill_at="1000"), [1], clock=clock.FixedClock(Decimal("1005"))
        )
        self.assertEqual(r.evaluated_at, Decimal("1005"))

    def test_bucket_after_preserves_identity_fields(self):
        bucket = B(bucket_id="xyz", capacity=7, refill_rate="3", tokens="7", last_refill_at="1000")
        r = limiter.check_requests(bucket, [1], clock=clock.FixedClock(Decimal("1000")))
        self.assertEqual(r.bucket_after.bucket_id, "xyz")
        self.assertEqual(r.bucket_after.capacity, 7)
        self.assertEqual(r.bucket_after.refill_rate, Decimal("3"))

    def test_bucket_after_last_refill_at_equals_evaluated_at(self):
        bucket = B(tokens="10", last_refill_at="1000")
        r = limiter.check_requests(bucket, [1], clock=clock.FixedClock(Decimal("1234")))
        self.assertEqual(r.bucket_after.last_refill_at, Decimal("1234"))
        self.assertEqual(r.bucket_after.last_refill_at, r.evaluated_at)

    def test_propagates_refill_validation_error_for_backward_clock(self):
        bucket = B(tokens="10", last_refill_at="1000")
        with self.assertRaises(errors.ValidationError) as ctx:
            limiter.check_requests(bucket, [1], clock=clock.FixedClock(Decimal("999")))
        self.assertEqual(str(ctx.exception), "invalid: now must not be before last_refill_at")


class OutputShapeTests(unittest.TestCase):
    def test_batch_decision_is_frozen(self):
        bucket = B(tokens="10", last_refill_at="1000")
        r = limiter.check_requests(bucket, [1], clock=clock.FixedClock(Decimal("1000")))
        with self.assertRaises(dataclasses.FrozenInstanceError):
            r.evaluated_at = Decimal("0")

    def test_request_decision_is_frozen(self):
        bucket = B(tokens="10", last_refill_at="1000")
        r = limiter.check_requests(bucket, [1], clock=clock.FixedClock(Decimal("1000")))
        with self.assertRaises(dataclasses.FrozenInstanceError):
            r.decisions[0].allowed = False

    def test_decisions_is_a_tuple(self):
        bucket = B(tokens="10", last_refill_at="1000")
        r = limiter.check_requests(bucket, [1], clock=clock.FixedClock(Decimal("1000")))
        self.assertIsInstance(r.decisions, tuple)

    def test_keyword_call_matches_documented_signature(self):
        bucket = B(tokens="10", last_refill_at="1000")
        r = limiter.check_requests(bucket=bucket, costs=[1], clock=clock.FixedClock(Decimal("4242")))
        self.assertEqual(r.evaluated_at, Decimal("4242"))


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.bucket = B(tokens="10", last_refill_at="1000")

    def test_bucket_wrong_type_raises(self):
        with self.assertRaises(errors.ValidationError) as ctx:
            limiter.check_requests("not-a-bucket", [1])
        self.assertEqual(str(ctx.exception), "invalid: bucket must be a TokenBucket")

    def test_costs_wrong_type_raises(self):
        with self.assertRaises(errors.ValidationError) as ctx:
            limiter.check_requests(self.bucket, "not-a-list")
        self.assertEqual(str(ctx.exception), "invalid: costs must be a list or tuple")

    def test_costs_empty_raises(self):
        with self.assertRaises(errors.ValidationError) as ctx:
            limiter.check_requests(self.bucket, [])
        self.assertEqual(str(ctx.exception), "invalid: costs must not be empty")

    def test_cost_zero_raises(self):
        with self.assertRaises(errors.ValidationError) as ctx:
            limiter.check_requests(self.bucket, [1, 0])
        self.assertEqual(str(ctx.exception), "invalid: costs[1] must be a positive int")

    def test_cost_negative_raises(self):
        with self.assertRaises(errors.ValidationError) as ctx:
            limiter.check_requests(self.bucket, [1, -5])
        self.assertEqual(str(ctx.exception), "invalid: costs[1] must be a positive int")

    def test_cost_non_int_types_rejected(self):
        for bad_cost in (True, "5", 3.5):
            with self.subTest(bad_cost=bad_cost):
                with self.assertRaises(errors.ValidationError) as ctx:
                    limiter.check_requests(self.bucket, [1, bad_cost])
                self.assertEqual(str(ctx.exception), "invalid: costs[1] must be a int")

    def test_all_validation_errors_are_ratelimit_errors(self):
        with self.assertRaises(errors.RateLimitError):
            limiter.check_requests(self.bucket, [])


class ClockLoggingReuseMutationTests(unittest.TestCase):
    def setUp(self):
        self.bucket = B(capacity=10, tokens="10", last_refill_at="1000")
        self.logger = logging.getLogger("ratelimit.limiter")

    def test_clock_called_exactly_once(self):
        class CountingClock:
            def __init__(self, value):
                self.calls = 0
                self.value = value

            def now(self):
                self.calls += 1
                return self.value

        cc = CountingClock(Decimal("1000"))
        limiter.check_requests(self.bucket, [1, 1, 1], clock=cc)
        self.assertEqual(cc.calls, 1)

    def test_default_clock_comes_from_clock_module(self):
        with mock.patch("clock.SystemClock") as fake_system:
            fake_system.return_value.now.return_value = Decimal("5000")
            r = limiter.check_requests(self.bucket, [1])
        self.assertEqual(r.evaluated_at, Decimal("5000"))

    def test_success_logs_exactly_one_info_record_with_exact_message(self):
        handler = _ListHandler()
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
        try:
            limiter.check_requests(self.bucket, [7, 5, 3], clock=clock.FixedClock(Decimal("1000")))
        finally:
            self.logger.removeHandler(handler)
        self.assertEqual(len(handler.records), 1)
        self.assertEqual(handler.records[0].levelname, "INFO")
        self.assertEqual(
            handler.records[0].getMessage(), "batch bucket=b1 requests=3 allowed=2 denied=1"
        )

    def test_failure_logs_nothing(self):
        handler = _ListHandler()
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
        try:
            with self.assertRaises(errors.ValidationError):
                limiter.check_requests(self.bucket, [])
        finally:
            self.logger.removeHandler(handler)
        self.assertEqual(len(handler.records), 0)

    def test_reuses_refill_exactly_once(self):
        with mock.patch("buckets.refill", wraps=buckets.refill) as spy:
            limiter.check_requests(self.bucket, [1, 1, 1], clock=clock.FixedClock(Decimal("1000")))
        self.assertEqual(spy.call_count, 1)
        spy.assert_called_once_with(self.bucket, Decimal("1000"))

    def test_does_not_mutate_bucket_or_costs(self):
        costs = [5, 3]
        limiter.check_requests(self.bucket, costs, clock=clock.FixedClock(Decimal("1000")))
        self.assertEqual(self.bucket.tokens, Decimal("10"))
        self.assertEqual(costs, [5, 3])


if __name__ == "__main__":
    unittest.main()
