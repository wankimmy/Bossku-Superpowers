import os
import sys
import unittest
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from booking import Booking, Calendar


class BookingTests(unittest.TestCase):
    def test_back_to_back_bookings_are_allowed(self):
        cal = Calendar()
        cal.add_booking(Booking("ann", date(2026, 1, 1), date(2026, 1, 5)))
        # bea checks in the same day ann checks out -- should not conflict
        cal.add_booking(Booking("bea", date(2026, 1, 5), date(2026, 1, 8)))
        self.assertEqual(cal.total_nights("ann"), 4)
        self.assertEqual(cal.total_nights("bea"), 3)

    def test_bookings_on_excludes_checkout_day(self):
        cal = Calendar()
        cal.add_booking(Booking("ann", date(2026, 1, 1), date(2026, 1, 5)))
        self.assertEqual(cal.bookings_on(date(2026, 1, 4)), ["ann"])
        self.assertEqual(cal.bookings_on(date(2026, 1, 5)), [])

    def test_real_overlap_is_rejected(self):
        cal = Calendar()
        cal.add_booking(Booking("ann", date(2026, 1, 1), date(2026, 1, 5)))
        with self.assertRaises(ValueError):
            cal.add_booking(Booking("bea", date(2026, 1, 4), date(2026, 1, 6)))


if __name__ == "__main__":
    unittest.main()
