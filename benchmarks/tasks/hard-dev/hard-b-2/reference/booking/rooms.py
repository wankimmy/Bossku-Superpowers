"""A single meeting room's bookings for one day (minutes since midnight)."""

DAY_MINUTES = 1440


class Booking:
    __slots__ = ("booking_id", "start", "end", "organizer")

    def __init__(self, booking_id, start, end, organizer):
        self.booking_id = booking_id
        self.start = start
        self.end = end
        self.organizer = organizer


class Room:
    def __init__(self, name):
        self.name = name
        self._bookings = {}
        self._next_id = 1
        self._free_slots_cache = None

    def _overlaps(self, start, end):
        for booking in self._bookings.values():
            if start < booking.end and end > booking.start:
                return True
        return False

    def is_available(self, start, end):
        """True if [start, end) doesn't overlap any existing booking.

        Bookings that merely touch (one ends exactly when the other
        starts) do not count as overlapping.
        """
        if start >= end:
            raise ValueError("start must be before end")
        return not self._overlaps(start, end)

    def book(self, start, end, organizer):
        if not (0 <= start < end <= DAY_MINUTES):
            raise ValueError(
                "booking must fall within a single day (0-1440) with start < end"
            )
        if not self.is_available(start, end):
            raise ValueError("time slot is not available")
        booking_id = self._next_id
        self._next_id += 1
        self._bookings[booking_id] = Booking(booking_id, start, end, organizer)
        self._free_slots_cache = None
        return booking_id

    def cancel(self, booking_id):
        if booking_id not in self._bookings:
            raise KeyError(booking_id)
        del self._bookings[booking_id]
        self._free_slots_cache = None

    def booked_minutes(self):
        return sum(b.end - b.start for b in self._bookings.values())

    def free_slots(self):
        """Return the free (start, end) gaps for the day, ascending by start."""
        if self._free_slots_cache is not None:
            return list(self._free_slots_cache)

        ordered = sorted(self._bookings.values(), key=lambda b: b.start)
        gaps = []
        cursor = 0
        for booking in ordered:
            if booking.start > cursor:
                gaps.append((cursor, booking.start))
            cursor = max(cursor, booking.end)
        if cursor < DAY_MINUTES:
            gaps.append((cursor, DAY_MINUTES))

        self._free_slots_cache = gaps
        return list(gaps)
