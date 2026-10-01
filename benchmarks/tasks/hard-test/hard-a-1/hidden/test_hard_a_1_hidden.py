import unittest

from duration import parse_duration, format_duration, DurationError


class ParseBasicTests(unittest.TestCase):
    def test_single_units(self):
        self.assertEqual(parse_duration("59s"), 59)
        self.assertEqual(parse_duration("1m"), 60)
        self.assertEqual(parse_duration("1h"), 3600)
        self.assertEqual(parse_duration("1d"), 86400)

    def test_full_combo_in_order(self):
        self.assertEqual(parse_duration("1d1h1m1s"), 90061)

    def test_skipping_a_middle_unit_is_allowed(self):
        self.assertEqual(parse_duration("1d5m"), 86400 + 300)

    def test_leading_zeros_in_digits_are_allowed(self):
        self.assertEqual(parse_duration("007h"), 7 * 3600)

    def test_negative_duration(self):
        self.assertEqual(parse_duration("-1h30m"), -5400)
        self.assertEqual(parse_duration("-0s"), 0)

    def test_huge_value_does_not_overflow(self):
        self.assertEqual(parse_duration("1000000000d"), 1000000000 * 86400)


class ParseInvalidTests(unittest.TestCase):
    def test_empty_string_raises(self):
        with self.assertRaises(DurationError):
            parse_duration("")

    def test_lone_dash_raises(self):
        with self.assertRaises(DurationError):
            parse_duration("-")

    def test_leading_plus_raises(self):
        with self.assertRaises(DurationError):
            parse_duration("+1h")

    def test_decimal_point_raises(self):
        with self.assertRaises(DurationError):
            parse_duration("1.5h")

    def test_uppercase_unit_raises(self):
        with self.assertRaises(DurationError):
            parse_duration("1H")

    def test_units_out_of_order_raises(self):
        with self.assertRaises(DurationError):
            parse_duration("1m1h")

    def test_duplicate_unit_raises(self):
        with self.assertRaises(DurationError):
            parse_duration("1h1h")

    def test_internal_whitespace_raises(self):
        with self.assertRaises(DurationError):
            parse_duration("1h 30m")

    def test_trailing_garbage_raises(self):
        with self.assertRaises(DurationError):
            parse_duration("1hx")

    def test_missing_digits_before_unit_raises(self):
        with self.assertRaises(DurationError):
            parse_duration("h5m")

    def test_non_ascii_digit_raises(self):
        with self.assertRaises(DurationError):
            parse_duration("١1h")  # Extended Arabic-Indic digit one, then "1h"

    def test_wrong_type_raises_type_error(self):
        with self.assertRaises(TypeError):
            parse_duration(3600)
        with self.assertRaises(TypeError):
            parse_duration(None)


class FormatTests(unittest.TestCase):
    def test_format_omits_zero_units(self):
        self.assertEqual(format_duration(3600), "1h")
        self.assertEqual(format_duration(61), "1m1s")
        self.assertEqual(format_duration(86400), "1d")

    def test_format_zero_is_0s(self):
        self.assertEqual(format_duration(0), "0s")

    def test_format_negative_single_leading_sign(self):
        self.assertEqual(format_duration(-5400), "-1h30m")

    def test_format_rejects_non_int(self):
        with self.assertRaises(TypeError):
            format_duration("3600")
        with self.assertRaises(TypeError):
            format_duration(3600.0)

    def test_format_rejects_bool(self):
        with self.assertRaises(TypeError):
            format_duration(True)


class RoundTripTests(unittest.TestCase):
    def test_round_trip_several_values(self):
        for n in (0, 59, 60, 61, 3600, 3661, 86400, 90061, -61, -5400, 123456789):
            self.assertEqual(parse_duration(format_duration(n)), n)


class ExceptionHierarchyTests(unittest.TestCase):
    def test_duration_error_is_value_error(self):
        self.assertTrue(issubclass(DurationError, ValueError))


if __name__ == "__main__":
    unittest.main()
