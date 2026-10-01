"""Retry policy with exponential backoff, a delay cap, and an injectable clock."""
import time


class RetryPolicy:
    def __init__(self, max_attempts, base_delay, max_delay=None, multiplier=2.0,
                 retry_on=(Exception,), clock=time.monotonic, sleep=time.sleep):
        if not isinstance(max_attempts, int) or isinstance(max_attempts, bool) or max_attempts < 1:
            raise ValueError("max_attempts must be an int >= 1")
        if base_delay < 0:
            raise ValueError("base_delay must be >= 0")
        if multiplier < 1:
            raise ValueError("multiplier must be >= 1")
        if max_delay is not None and max_delay < base_delay:
            raise ValueError("max_delay must be >= base_delay")

        self.max_attempts = max_attempts
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.multiplier = multiplier
        self.retry_on = retry_on
        self.clock = clock
        self.sleep = sleep

        self.attempts_used = 0
        self.elapsed = 0.0

    def delay_for(self, attempt):
        delay = self.base_delay * (self.multiplier ** (attempt - 1))
        if self.max_delay is not None and delay > self.max_delay:
            delay = self.max_delay
        return delay

    def call(self, fn, *args, **kwargs):
        start = self.clock()
        attempt = 0
        try:
            while True:
                attempt += 1
                self.attempts_used = attempt
                try:
                    return fn(*args, **kwargs)
                except self.retry_on:
                    if attempt >= self.max_attempts:
                        raise
                    self.sleep(self.delay_for(attempt))
        finally:
            self.elapsed = self.clock() - start
