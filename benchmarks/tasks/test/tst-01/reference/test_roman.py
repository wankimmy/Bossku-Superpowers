import unittest

from roman import to_roman, from_roman, is_valid, add


class ToRomanTests(unittest.TestCase):
    def test_basic_values(self):
        cases = {
            1: "I", 2: "II", 3: "III", 4: "IV", 5: "V",
            9: "IX", 10: "X", 40: "XL", 44: "XLIV", 49: "XLIX",
            90: "XC", 99: "XCIX", 100: "C", 400: "CD", 500: "D",
            900: "CM", 1000: "M", 1994: "MCMXCIV", 3999: "MMMCMXCIX",
        }
        for n, roman in cases.items():
            with self.subTest(n=n):
                self.assertEqual(to_roman(n), roman)

    def test_out_of_range_raises(self):
        for bad in (0, -1, 4000, 10000):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    to_roman(bad)

    def test_non_int_raises(self):
        for bad in ("5", 5.0, None, [1]):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    to_roman(bad)


class FromRomanTests(unittest.TestCase):
    def test_round_trip_for_many_values(self):
        for n in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 40, 44, 49, 90, 99,
                  100, 400, 500, 900, 1000, 1994, 3999]:
            with self.subTest(n=n):
                self.assertEqual(from_roman(to_roman(n)), n)

    def test_repeated_letters_parse_correctly(self):
        self.assertEqual(from_roman("II"), 2)
        self.assertEqual(from_roman("III"), 3)
        self.assertEqual(from_roman("XXX"), 30)

    def test_lowercase_is_invalid(self):
        with self.assertRaises(ValueError):
            from_roman("iv")

    def test_invalid_character_not_at_start_is_invalid(self):
        with self.assertRaises(ValueError):
            from_roman("XI9")

    def test_non_canonical_repetition_is_invalid(self):
        for bad in ("IIII", "VV", "XXXX", "LL"):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    from_roman(bad)

    def test_wrong_ordering_is_invalid(self):
        for bad in ("IC", "VX", "IXI"):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    from_roman(bad)

    def test_empty_string_is_invalid(self):
        with self.assertRaises(ValueError):
            from_roman("")

    def test_non_string_is_invalid(self):
        for bad in (None, 123, ["I"]):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    from_roman(bad)


class IsValidTests(unittest.TestCase):
    def test_valid_numerals(self):
        for good in ("I", "IV", "IX", "XL", "MCMXCIV", "MMMCMXCIX"):
            with self.subTest(good=good):
                self.assertTrue(is_valid(good))

    def test_invalid_numerals(self):
        for bad in ("IIII", "iv", "", None, 123, "VX"):
            with self.subTest(bad=bad):
                self.assertFalse(is_valid(bad))


class AddTests(unittest.TestCase):
    def test_simple_sum(self):
        self.assertEqual(add("II", "III"), "V")

    def test_sum_at_upper_edge(self):
        self.assertEqual(add("MMM", "CMXCIX"), "MMMCMXCIX")

    def test_sum_overflow_raises(self):
        with self.assertRaises(ValueError):
            add("MMM", "M")

    def test_invalid_operand_raises(self):
        with self.assertRaises(ValueError):
            add("IIII", "I")


if __name__ == "__main__":
    unittest.main()
