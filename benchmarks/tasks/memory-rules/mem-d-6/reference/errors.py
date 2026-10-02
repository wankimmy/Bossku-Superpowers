"""Dedicated exception hierarchy for the rate limiter package."""


class RateLimiterError(Exception):
    """Root of every exception this package raises on purpose."""


class KeyAlreadyUsedError(RateLimiterError):
    """Raised when set_capacity is called for a key that already has a bucket."""


class InvalidCapacityError(RateLimiterError):
    """Raised when a capacity isn't a positive number."""
