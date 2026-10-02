"""A tiny token-bucket rate limiter (manual refill, no wall clock)."""

from errors import InvalidCapacityError, KeyAlreadyUsedError


class TokenBucket:
    def __init__(self, capacity):
        self.capacity = capacity
        self.tokens = capacity

    def allow(self, cost=1):
        """Consume `cost` tokens if available; return True/False."""
        if self.tokens >= cost:
            self.tokens -= cost
            return True
        return False

    def refill(self, amount):
        """Add tokens back, capped at capacity."""
        self.tokens = min(self.capacity, self.tokens + amount)


def peek(bucket):
    """Return the bucket's current token count without consuming any."""
    return bucket.tokens


def reset(bucket):
    """Refill a bucket all the way back to its capacity immediately."""
    bucket.tokens = bucket.capacity


class KeyedRateLimiter:
    def __init__(self, capacity):
        self.capacity = capacity
        self._buckets = {}
        self._overrides = {}

    def _bucket_for(self, key):
        if key not in self._buckets:
            cap = self._overrides.get(key, self.capacity)
            self._buckets[key] = TokenBucket(cap)
        return self._buckets[key]

    def allow(self, key, cost=1):
        return self._bucket_for(key).allow(cost)

    def set_capacity(self, key, capacity):
        if key in self._buckets:
            raise KeyAlreadyUsedError(f"key {key!r} already has a bucket")
        if not isinstance(capacity, (int, float)) or isinstance(capacity, bool) or capacity <= 0:
            raise InvalidCapacityError(f"capacity must be a positive number, got {capacity!r}")
        self._overrides[key] = capacity
