import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ratelimiter import TokenBucket


class TokenBucketTests(unittest.TestCase):
    def test_allow_consumes_tokens(self):
        bucket = TokenBucket(2)
        self.assertTrue(bucket.allow())
        self.assertTrue(bucket.allow())
        self.assertFalse(bucket.allow())

    def test_refill_caps_at_capacity(self):
        bucket = TokenBucket(2)
        bucket.allow()
        bucket.refill(10)
        self.assertEqual(bucket.tokens, 2)


if __name__ == "__main__":
    unittest.main()
