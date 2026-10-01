import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest

from booking.schedule import Scheduler


class BookingTests(unittest.TestCase):
    def test_add_and_book(self):
        sched = Scheduler()
        room = sched.add_room("Falcon")
        booking_id = room.book(60, 120, "amy")
        self.assertEqual(booking_id, 1)

    def test_overlapping_booking_rejected(self):
        sched = Scheduler()
        room = sched.add_room("Falcon")
        room.book(60, 120, "amy")
        with self.assertRaises(ValueError):
            room.book(90, 150, "bob")

    def test_cancel_removes_booking(self):
        sched = Scheduler()
        room = sched.add_room("Falcon")
        booking_id = room.book(60, 120, "amy")
        room.cancel(booking_id)
        self.assertEqual(room.booked_minutes(), 0)

    def test_duplicate_room_name_raises(self):
        sched = Scheduler()
        sched.add_room("Falcon")
        with self.assertRaises(ValueError):
            sched.add_room("Falcon")


if __name__ == "__main__":
    unittest.main()
