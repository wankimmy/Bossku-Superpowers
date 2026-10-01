"""A small reusable descriptive-statistics helper."""


class Stats:
    def __init__(self, values):
        values = list(values)
        if not values:
            raise ValueError("values must not be empty")
        self._values = values

    @property
    def count(self):
        return len(self._values)

    @property
    def total(self):
        return round(sum(self._values), 2)

    @property
    def average(self):
        return round(sum(self._values) / len(self._values), 2)

    @property
    def minimum(self):
        return round(min(self._values), 2)

    @property
    def maximum(self):
        return round(max(self._values), 2)

    def as_dict(self):
        return {
            "count": self.count,
            "total": self.total,
            "average": self.average,
            "min": self.minimum,
            "max": self.maximum,
        }
