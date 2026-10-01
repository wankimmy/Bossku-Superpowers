import unittest

from booking.rooms import Room
from booking.schedule import Scheduler
from booking.reports import utilization_percent


class BookingHiddenTests(unittest.TestCase):
    def test_book_returns_incrementing_ids(self):
        room = Room("Falcon")
        id1 = room.book(0, 60, "amy")
        id2 = room.book(60, 120, "bob")
        self.assertEqual((id1, id2), (1, 2))

    def test_overlapping_booking_raises_and_leaves_state_unchanged(self):
        room = Room("Falcon")
        room.book(60, 120, "amy")
        with self.assertRaises(ValueError):
            room.book(90, 150, "bob")
        self.assertEqual(room.booked_minutes(), 60)

    def test_book_rejects_start_after_end(self):
        room = Room("Falcon")
        with self.assertRaises(ValueError):
            room.book(100, 50, "amy")

    def test_book_rejects_equal_start_end(self):
        room = Room("Falcon")
        with self.assertRaises(ValueError):
            room.book(50, 50, "amy")

    def test_book_rejects_out_of_day_bounds(self):
        room = Room("Falcon")
        with self.assertRaises(ValueError):
            room.book(-10, 10, "amy")
        with self.assertRaises(ValueError):
            room.book(1400, 1500, "amy")

    def test_touching_bookings_are_both_allowed(self):
        room = Room("Falcon")
        room.book(60, 120, "amy")
        second_id = room.book(120, 180, "bob")
        self.assertIsNotNone(second_id)
        self.assertEqual(room.booked_minutes(), 120)

    def test_touching_bookings_allowed_in_either_order(self):
        room = Room("Falcon")
        room.book(120, 180, "bob")
        first_id = room.book(60, 120, "amy")
        self.assertIsNotNone(first_id)
        self.assertEqual(room.booked_minutes(), 120)

    def test_is_available_true_for_touching_windows(self):
        room = Room("Falcon")
        room.book(60, 120, "amy")
        self.assertTrue(room.is_available(120, 180))
        self.assertTrue(room.is_available(0, 60))

    def test_is_available_false_for_real_overlap(self):
        room = Room("Falcon")
        room.book(60, 120, "amy")
        self.assertFalse(room.is_available(119, 121))
        self.assertFalse(room.is_available(0, 61))

    def test_is_available_rejects_equal_start_end(self):
        room = Room("Falcon")
        with self.assertRaises(ValueError):
            room.is_available(30, 30)

    def test_cancel_unknown_id_raises_keyerror(self):
        room = Room("Falcon")
        with self.assertRaises(KeyError):
            room.cancel(999)

    def test_free_slots_empty_room(self):
        room = Room("Falcon")
        self.assertEqual(room.free_slots(), [(0, 1440)])

    def test_free_slots_ascending_order_with_multiple_gaps(self):
        room = Room("Falcon")
        room.book(100, 200, "amy")
        room.book(400, 500, "bob")
        self.assertEqual(room.free_slots(), [(0, 100), (200, 400), (500, 1440)])

    def test_free_slots_reflects_cancel_immediately(self):
        room = Room("Falcon")
        booking_id = room.book(0, 600, "amy")
        self.assertEqual(room.free_slots(), [(600, 1440)])  # populate the cache
        room.cancel(booking_id)
        self.assertEqual(room.free_slots(), [(0, 1440)])

    def test_free_slots_reflects_new_booking_immediately(self):
        room = Room("Falcon")
        room.book(0, 100, "amy")
        self.assertEqual(room.free_slots(), [(100, 1440)])  # populate the cache
        room.book(200, 300, "bob")
        self.assertEqual(room.free_slots(), [(100, 200), (300, 1440)])

    def test_full_day_booking_leaves_no_free_slots(self):
        room = Room("Falcon")
        room.book(0, 1440, "amy")
        self.assertEqual(room.free_slots(), [])

    def test_room_lookup_is_case_and_whitespace_insensitive(self):
        sched = Scheduler()
        original = sched.add_room("Board Room")
        self.assertIs(sched.room("board room"), original)
        self.assertIs(sched.room(" BOARD ROOM "), original)
        self.assertEqual(sched.room("board room").name, "Board Room")

    def test_duplicate_room_name_case_insensitive_raises(self):
        sched = Scheduler()
        sched.add_room("Board Room")
        with self.assertRaises(ValueError):
            sched.add_room(" board room ")

    def test_room_names_preserve_display_form_and_add_order(self):
        sched = Scheduler()
        sched.add_room("Zeta")
        sched.add_room("Alpha")
        self.assertEqual(sched.room_names(), ["Zeta", "Alpha"])

    def test_import_bookings_does_not_mutate_caller_list(self):
        sched = Scheduler()
        sched.add_room("Falcon")
        entries = [(600, 660, "x"), (0, 60, "y")]
        original = list(entries)
        sched.import_bookings("Falcon", entries)
        self.assertEqual(entries, original)

    def test_import_bookings_books_chronologically_regardless_of_input_order(self):
        sched = Scheduler()
        sched.add_room("Falcon")
        entries = [(600, 660, "b"), (0, 60, "a")]
        ids = sched.import_bookings("Falcon", entries)
        self.assertEqual(len(ids), 2)
        self.assertLess(ids[0], ids[1])
        room = sched.room("Falcon")
        self.assertEqual(room.free_slots(), [(60, 600), (660, 1440)])

    def test_import_bookings_conflict_keeps_earlier_bookings(self):
        sched = Scheduler()
        sched.add_room("Falcon")
        entries = [(0, 60, "a"), (30, 90, "b")]
        with self.assertRaises(ValueError):
            sched.import_bookings("Falcon", entries)
        room = sched.room("Falcon")
        self.assertEqual(room.booked_minutes(), 60)

    def test_utilization_percent_basic(self):
        room = Room("Falcon")
        room.book(0, 360, "amy")
        self.assertEqual(utilization_percent(room), 25.0)


if __name__ == "__main__":
    unittest.main()
