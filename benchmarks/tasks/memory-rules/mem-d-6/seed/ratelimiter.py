"""A tiny token-bucket rate limiter (manual refill, no wall clock)."""


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
