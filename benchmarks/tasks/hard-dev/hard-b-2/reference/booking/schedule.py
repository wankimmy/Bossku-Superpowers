"""Coordinates multiple named meeting rooms."""

from .rooms import Room


def _key(name):
    return name.strip().lower()


class Scheduler:
    def __init__(self):
        self._rooms = {}

    def add_room(self, name):
        key = _key(name)
        if key in self._rooms:
            raise ValueError(f"room {name!r} already exists")
        room = Room(name)
        self._rooms[key] = room
        return room

    def room(self, name):
        key = _key(name)
        if key not in self._rooms:
            raise KeyError(name)
        return self._rooms[key]

    def room_names(self):
        return [room.name for room in self._rooms.values()]

    def import_bookings(self, room_name, entries):
        """Bulk-load (start, end, organizer) tuples into a room.

        `entries` is consumed in chronological order; the caller's own
        list is left exactly as it was passed in.
        """
        room = self.room(room_name)
        booking_ids = []
        for start, end, organizer in sorted(entries, key=lambda e: e[0]):
            booking_ids.append(room.book(start, end, organizer))
        return booking_ids
