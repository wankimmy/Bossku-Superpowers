import unittest
from datetime import date

from daterange import DateRange
from booking import Booking, Calendar


class DateRangeHiddenTests(unittest.TestCase):
    def test_nights_basic(self):
        r = DateRange(date(2026, 1, 1), date(2026, 1, 4))
        self.assertEqual(r.nights, 3)

    def test_invalid_range_equal_raises(self):
        with self.assertRaises(ValueError):
            DateRange(date(2026, 1, 1), date(2026, 1, 1))

    def test_invalid_range_backwards_raises(self):
        with self.assertRaises(ValueError):
            DateRange(date(2026, 1, 5), date(2026, 1, 1))

    def test_contains_day_before_start(self):
        r = DateRange(date(2026, 1, 1), date(2026, 1, 4))
        self.assertFalse(r.contains_day(date(2025, 12, 31)))

    def test_contains_day_on_start(self):
        r = DateRange(date(2026, 1, 1), date(2026, 1, 4))
        self.assertTrue(r.contains_day(date(2026, 1, 1)))

    def test_contains_day_last_night(self):
        r = DateRange(date(2026, 1, 1), date(2026, 1, 4))
        self.assertTrue(r.contains_day(date(2026, 1, 3)))

    def test_contains_day_excludes_end(self):
        r = DateRange(date(2026, 1, 1), date(2026, 1, 4))
        self.assertFalse(r.contains_day(date(2026, 1, 4)))

    def test_contains_day_after_end(self):
        r = DateRange(date(2026, 1, 1), date(2026, 1, 4))
        self.assertFalse(r.contains_day(date(2026, 1, 5)))

    def test_overlaps_identical_ranges(self):
        a = DateRange(date(2026, 1, 1), date(2026, 1, 4))
        b = DateRange(date(2026, 1, 1), date(2026, 1, 4))
        self.assertTrue(a.overlaps(b))

    def test_overlaps_partial(self):
        a = DateRange(date(2026, 1, 1), date(2026, 1, 4))
        b = DateRange(date(2026, 1, 3), date(2026, 1, 6))
        self.assertTrue(a.overlaps(b))
        self.assertTrue(b.overlaps(a))

    def test_overlaps_adjacent_is_false_both_directions(self):
        a = DateRange(date(2026, 1, 1), date(2026, 1, 4))
        b = DateRange(date(2026, 1, 4), date(2026, 1, 8))
        self.assertFalse(a.overlaps(b))
        self.assertFalse(b.overlaps(a))

    def test_overlaps_disjoint_with_gap_is_false(self):
        a = DateRange(date(2026, 1, 1), date(2026, 1, 4))
        b = DateRange(date(2026, 1, 10), date(2026, 1, 12))
        self.assertFalse(a.overlaps(b))


class BookingCalendarHiddenTests(unittest.TestCase):
    def test_booking_nights_delegates(self):
        b = Booking("ann", date(2026, 1, 1), date(2026, 1, 6))
        self.assertEqual(b.nights, 5)

    def test_add_booking_rejects_real_overlap(self):
        cal = Calendar()
        cal.add_booking(Booking("ann", date(2026, 1, 1), date(2026, 1, 5)))
        with self.assertRaises(ValueError):
            cal.add_booking(Booking("bea", date(2026, 1, 4), date(2026, 1, 6)))

    def test_add_booking_allows_back_to_back(self):
        cal = Calendar()
        cal.add_booking(Booking("ann", date(2026, 1, 1), date(2026, 1, 5)))
        cal.add_booking(Booking("bea", date(2026, 1, 5), date(2026, 1, 8)))
        self.assertEqual(cal.bookings_on(date(2026, 1, 5)), ["bea"])

    def test_bookings_on_boundary_correct_through_calendar(self):
        cal = Calendar()
        cal.add_booking(Booking("zed", date(2026, 1, 1), date(2026, 1, 10)))
        self.assertEqual(cal.bookings_on(date(2026, 1, 1)), ["zed"])
        self.assertEqual(cal.bookings_on(date(2026, 1, 9)), ["zed"])
        self.assertEqual(cal.bookings_on(date(2026, 1, 10)), [])
        self.assertEqual(cal.bookings_on(date(2025, 12, 31)), [])

    def test_bookings_on_returns_sorted_list_type(self):
        cal = Calendar()
        cal.add_booking(Booking("ann", date(2026, 2, 1), date(2026, 2, 5)))
        result = cal.bookings_on(date(2026, 2, 2))
        self.assertEqual(result, sorted(result))
        self.assertEqual(result, ["ann"])

    def test_total_nights_sums_multiple_bookings(self):
        cal = Calendar()
        cal.add_booking(Booking("ann", date(2026, 1, 1), date(2026, 1, 4)))
        cal.add_booking(Booking("ann", date(2026, 2, 1), date(2026, 2, 3)))
        cal.add_booking(Booking("bea", date(2026, 1, 5), date(2026, 1, 6)))
        self.assertEqual(cal.total_nights("ann"), 5)

    def test_total_nights_zero_for_unknown_guest(self):
        cal = Calendar()
        cal.add_booking(Booking("ann", date(2026, 1, 1), date(2026, 1, 4)))
        self.assertEqual(cal.total_nights("nobody"), 0)


if __name__ == "__main__":
    unittest.main()
