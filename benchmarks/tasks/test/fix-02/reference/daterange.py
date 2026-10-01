"""Half-open date ranges used for bookings."""
from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class DateRange:
    start: date
    end: date

    def __post_init__(self):
        if self.end <= self.start:
            raise ValueError("end must be after start")

    @property
    def nights(self):
        return (self.end - self.start).days

    def contains_day(self, day):
        return self.start <= day < self.end

    def overlaps(self, other):
        return self.start < other.end and other.start < self.end
