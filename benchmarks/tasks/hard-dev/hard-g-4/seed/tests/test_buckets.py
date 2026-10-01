import os
import sys
import unittest
from dataclasses import FrozenInstanceError
from decimal import Decimal

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import buckets
import errors


class RefillTests(unittest.TestCase):
    """Shows the style this project expects: frozen dataclasses built
    directly, timestamps injected explicitly as Decimal (never read from
    the real clock in a test), and errors checked against the shared
    base class rather than a bare builtin exception."""

    def setUp(self):
        self.bucket = buckets.TokenBucket(
            bucket_id="b1",
            capacity=10,
            refill_rate=Decimal("2"),
            tokens=Decimal("4"),
            last_refill_at=Decimal("1000"),
        )

    def test_refill_adds_elapsed_times_rate(self):
        updated = buckets.refill(self.bucket, Decimal("1001"))
        self.assertEqual(updated.tokens, Decimal("6"))
        self.assertEqual(updated.last_refill_at, Decimal("1001"))

    def test_refill_caps_at_capacity(self):
        updated = buckets.refill(self.bucket, Decimal("1100"))
        self.assertEqual(updated.tokens, Decimal("10"))

    def test_refill_does_not_mutate_original_bucket(self):
        buckets.refill(self.bucket, Decimal("1001"))
        self.assertEqual(self.bucket.tokens, Decimal("4"))

    def test_now_before_last_refill_raises(self):
        with self.assertRaises(errors.RateLimitError):
            buckets.refill(self.bucket, Decimal("999"))

    def test_bucket_is_frozen(self):
        with self.assertRaises(FrozenInstanceError):
            self.bucket.tokens = Decimal("0")


if __name__ == "__main__":
    unittest.main()
