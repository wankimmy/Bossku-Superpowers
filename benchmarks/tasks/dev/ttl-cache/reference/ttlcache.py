import time
from collections import OrderedDict


class TTLCache:
    def __init__(self, maxsize, ttl, clock=time.monotonic):
        if maxsize <= 0 or ttl <= 0:
            raise ValueError("maxsize and ttl must be positive")
        self.maxsize, self.ttl, self._clock = maxsize, ttl, clock
        self._data = OrderedDict()  # key -> (value, expires_at); order = recency of use

    def _alive(self, entry):
        return self._clock() < entry[1]

    def purge(self):
        dead = [k for k, e in self._data.items() if not self._alive(e)]
        for k in dead:
            del self._data[k]
        return len(dead)

    def set(self, key, value):
        self.purge()
        if key in self._data:
            del self._data[key]
        elif len(self._data) >= self.maxsize:
            self._data.popitem(last=False)
        self._data[key] = (value, self._clock() + self.ttl)

    def get(self, key, default=None):
        entry = self._data.get(key)
        if entry is None:
            return default
        if not self._alive(entry):
            del self._data[key]
            return default
        self._data.move_to_end(key)
        return entry[0]

    def __contains__(self, key):
        entry = self._data.get(key)
        return entry is not None and self._alive(entry)

    def __len__(self):
        return sum(1 for e in self._data.values() if self._alive(e))
