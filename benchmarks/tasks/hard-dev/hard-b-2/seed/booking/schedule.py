"""Coordinates multiple named meeting rooms."""

from .rooms import Room


class Scheduler:
    def __init__(self):
        self._rooms = {}

    def add_room(self, name):
        if name in self._rooms:
            raise ValueError(f"room {name!r} already exists")
        room = Room(name)
        self._rooms[name] = room
        return room

    def room(self, name):
        if name not in self._rooms:
            raise KeyError(name)
        return self._rooms[name]

    def room_names(self):
        return [room.name for room in self._rooms.values()]

    def import_bookings(self, room_name, entries):
        """Bulk-load (start, end, organizer) tuples into a room.

        `entries` is consumed in chronological order; the caller's own
        list is left exactly as it was passed in.
        """
        room = self.room(room_name)
        entries.sort(key=lambda e: e[0])
        booking_ids = []
        for start, end, organizer in entries:
            booking_ids.append(room.book(start, end, organizer))
        return booking_ids
