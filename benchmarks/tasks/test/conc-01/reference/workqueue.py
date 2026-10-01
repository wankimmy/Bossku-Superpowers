import threading


class Full(Exception):
    pass


class Empty(Exception):
    pass


class BoundedQueue:
    def __init__(self, maxsize):
        if not isinstance(maxsize, int) or maxsize <= 0:
            raise ValueError("maxsize must be a positive int")
        self._maxsize = maxsize
        self._items = []
        self._lock = threading.Lock()
        self._not_full = threading.Condition(self._lock)
        self._not_empty = threading.Condition(self._lock)

    def put(self, item):
        with self._not_full:
            while len(self._items) >= self._maxsize:
                self._not_full.wait()
            self._items.append(item)
            self._not_empty.notify()

    def get(self):
        with self._not_empty:
            while not self._items:
                self._not_empty.wait()
            item = self._items.pop(0)
            self._not_full.notify()
            return item

    def put_nowait(self, item):
        with self._lock:
            if len(self._items) >= self._maxsize:
                raise Full()
            self._items.append(item)
            self._not_empty.notify()

    def get_nowait(self):
        with self._lock:
            if not self._items:
                raise Empty()
            item = self._items.pop(0)
            self._not_full.notify()
            return item

    def qsize(self):
        with self._lock:
            return len(self._items)
