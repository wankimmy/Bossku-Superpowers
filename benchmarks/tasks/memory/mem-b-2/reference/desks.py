"""Desk booking for the coworking space."""

from errors import ConflictError, NotFoundError


class DeskBooking:
    def __init__(self):
        self._bookings = {}  # (desk_id, day) -> user

    def book(self, desk_id, user, day):
        key = (desk_id, day)
        if key in self._bookings:
            raise ConflictError(f"desk {desk_id} is already booked on {day}")
        self._bookings[key] = user

    def cancel(self, desk_id, user, day):
        key = (desk_id, day)
        if self._bookings.get(key) != user:
            raise NotFoundError(
                f"no booking for desk {desk_id} on {day} held by {user}"
            )
        del self._bookings[key]

    def list_bookings_for_user(self, user):
        return sorted(
            (desk_id, day)
            for (desk_id, day), owner in self._bookings.items()
            if owner == user
        )

    def move_booking(self, desk_id, user, old_day, new_day):
        old_key = (desk_id, old_day)
        if self._bookings.get(old_key) != user:
            raise NotFoundError(
                f"no booking for desk {desk_id} on {old_day} held by {user}"
            )
        new_key = (desk_id, new_day)
        if new_key in self._bookings:
            raise ConflictError(f"desk {desk_id} is already booked on {new_day}")
        del self._bookings[old_key]
        self._bookings[new_key] = user
