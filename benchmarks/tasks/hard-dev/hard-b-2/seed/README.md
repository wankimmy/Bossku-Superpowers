# Meeting Room Booking

Tracks bookings for named meeting rooms over a single day, in minutes
since midnight (0-1440).

Run tests: `python -m unittest discover -s tests`

## Rooms

- `Scheduler.add_room(name)` creates a room and returns it. Room names
  are matched **case-insensitively** and **ignoring leading/trailing
  whitespace** everywhere a room is looked up: `"Board Room"`,
  `"board room"` and `" BOARD ROOM "` all refer to the same room.
  Adding a room whose normalized name already exists raises
  `ValueError`. A room's `.name` attribute keeps whatever casing and
  spacing was used the first time it was added.
- `Scheduler.room(name)` looks up a room (same normalization); raises
  `KeyError` if no such room exists.
- `Scheduler.room_names()` returns the display names of all rooms,
  in the order they were added.

## Bookings

- `Room.book(start, end, organizer)` adds a booking. `start` and `end`
  are minutes since midnight; `0 <= start < end <= 1440` or it raises
  `ValueError`. Returns a `booking_id` (int) used to cancel it later.
- Two bookings **overlap** only if they share an actual minute of time.
  Bookings that merely touch — one ending exactly when another starts —
  do **not** overlap and are both allowed (e.g. a 09:00-10:00 booking
  and a 10:00-11:00 booking in the same room coexist fine).
- Booking a time slot that overlaps an existing booking in that room
  raises `ValueError`; it does not modify any state.
- `Room.is_available(start, end)` returns whether `[start, end)` is
  free of any overlap, using the same touching-is-fine rule above. It
  raises `ValueError` if `start >= end`.
- `Room.cancel(booking_id)` removes a booking; raises `KeyError` if
  that id doesn't exist in the room.
- `Room.booked_minutes()` returns the total minutes currently booked
  in the room.

## Free slots

`Room.free_slots()` returns the list of `(start, end)` gaps in the day
that are not covered by any booking, **in ascending order by start
time**. An empty room returns `[(0, 1440)]`. The list always reflects
the room's *current* bookings — after any `book()` or `cancel()` call,
the very next `free_slots()` call must already reflect that change.

## Bulk import

`Scheduler.import_bookings(room_name, entries)` takes a list of
`(start, end, organizer)` tuples and books them, in order from
earliest start time to latest. **The caller's `entries` list itself is
never modified** — `import_bookings` only reads from it. It returns the
list of newly created booking ids, in the order the bookings were made
(earliest start time first), regardless of the order `entries` was
given in. If any entry in the batch conflicts with an existing booking
(or another entry already imported earlier in the same call), the
`ValueError` from `Room.book()` propagates and any bookings already
made earlier in that same call remain booked (import is not
transactional).

## Utilization

`utilization_percent(room)` (in `booking/reports.py`) returns the
percentage of the day currently booked, `0.0`-`100.0`, rounded to one
decimal place.
