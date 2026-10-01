class Full(Exception):
    pass


class Empty(Exception):
    pass


class BoundedQueue:
    """A fixed-capacity FIFO queue shared by multiple threads."""

    def __init__(self, maxsize):
        raise NotImplementedError

    def put(self, item):
        raise NotImplementedError

    def get(self):
        raise NotImplementedError

    def put_nowait(self, item):
        raise NotImplementedError

    def get_nowait(self):
        raise NotImplementedError

    def qsize(self):
        raise NotImplementedError
