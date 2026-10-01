"""Single-room booking calendar built on top of DateRange."""
from daterange import DateRange


class Booking:
    def __init__(self, guest, check_in, check_out):
        self.guest = guest
        self.range = DateRange(check_in, check_out)

    @property
    def nights(self):
        return self.range.nights

    def overlaps(self, other):
        return self.range.overlaps(other.range)


class Calendar:
    def __init__(self):
        self._bookings = []

    def add_booking(self, booking):
        for existing in self._bookings:
            if booking.overlaps(existing):
                raise ValueError(f"{booking.guest} conflicts with {existing.guest}")
        self._bookings.append(booking)

    def bookings_on(self, day):
        return sorted(b.guest for b in self._bookings if b.range.contains_day(day))

    def total_nights(self, guest):
        return sum(b.nights for b in self._bookings if b.guest == guest)
