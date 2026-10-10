"""Small caching helpers."""
import time

RETRY_WAIT_SECONDS = 0.5
GIVE_UP_AFTER_SECONDS = 120


class TTLCache:
    def __init__(self, ttl_seconds, clock=time.monotonic):
        self._ttl = ttl_seconds
        self._clock = clock
        self._data = {}

    def set(self, key, value):
        self._data[key] = (self._clock(), value)

    def get(self, key, default=None):
        item = self._data.get(key)
        if item is None or self._clock() - item[0] > self._ttl:
            return default
        return item[1]


def fetch_with_retry(fn, attempts=3, sleep=time.sleep):
    for attempt in range(attempts):
        try:
            return fn()
        except Exception:
            if attempt == attempts - 1:
                raise
            sleep(RETRY_WAIT_SECONDS)
