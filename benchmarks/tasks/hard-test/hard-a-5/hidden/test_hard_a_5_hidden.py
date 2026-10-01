import unittest

from querystring import encode_query, decode_query, QueryStringError


class EncodeQueryTests(unittest.TestCase):
    def test_basic_pairs(self):
        self.assertEqual(encode_query([("a", "1"), ("b", "2")]), "a=1&b=2")

    def test_space_encodes_to_percent_20_not_plus(self):
        self.assertEqual(encode_query([("q", "a b")]), "q=a%20b")

    def test_hex_digits_are_uppercase(self):
        self.assertEqual(encode_query([("k", ":")]), "k=%3A")

    def test_reserved_characters_are_encoded(self):
        self.assertEqual(encode_query([("a=b", "c&d")]), "a%3Db=c%26d")

    def test_empty_params_is_empty_string(self):
        self.assertEqual(encode_query([]), "")

    def test_empty_key_or_value(self):
        self.assertEqual(encode_query([("", "value")]), "=value")

    def test_unicode_is_utf8_percent_encoded(self):
        self.assertEqual(encode_query([("city", "café")]), "city=caf%C3%A9")
        self.assertEqual(encode_query([("e", "\U0001F600")]), "e=%F0%9F%98%80")

    def test_params_not_list_raises_type_error(self):
        with self.assertRaises(TypeError):
            encode_query("not a list")

    def test_non_str_key_or_value_raises_type_error(self):
        with self.assertRaises(TypeError):
            encode_query([("a", 1)])
        with self.assertRaises(TypeError):
            encode_query([(1, "a")])

    def test_entry_not_a_pair_raises_type_error(self):
        with self.assertRaises(TypeError):
            encode_query([("a", "b", "c")])


class DecodeQueryTests(unittest.TestCase):
    def test_basic_pairs(self):
        self.assertEqual(decode_query("a=1&b=2"), [("a", "1"), ("b", "2")])

    def test_flag_without_equals_has_empty_value(self):
        self.assertEqual(decode_query("debug"), [("debug", "")])

    def test_empty_segment_between_ampersands(self):
        self.assertEqual(decode_query("a=1&&b=2"), [("a", "1"), ("", ""), ("b", "2")])

    def test_only_first_equals_splits_key_from_value(self):
        self.assertEqual(decode_query("k=a=b"), [("k", "a=b")])

    def test_plus_is_literal_not_space(self):
        self.assertEqual(decode_query("q=a+b"), [("q", "a+b")])

    def test_percent_20_decodes_to_space(self):
        self.assertEqual(decode_query("q=a%20b"), [("q", "a b")])

    def test_duplicate_keys_preserve_order_as_list(self):
        self.assertEqual(decode_query("a=1&b=2&a=3"), [("a", "1"), ("b", "2"), ("a", "3")])

    def test_empty_string_is_zero_pairs(self):
        self.assertEqual(decode_query(""), [])

    def test_percent_hex_is_case_insensitive_on_input(self):
        self.assertEqual(decode_query("k=%2d"), [("k", "-")])
        self.assertEqual(decode_query("k=%2D"), [("k", "-")])

    def test_multibyte_utf8_percent_sequence_reassembles_correctly(self):
        # A naive decoder that maps each %XX independently to chr(int(XX,16))
        # instead of collecting raw bytes and UTF-8-decoding them together
        # will mangle this.
        self.assertEqual(decode_query("city=caf%C3%A9"), [("city", "café")])
        self.assertEqual(decode_query("e=%F0%9F%98%80"), [("e", "\U0001F600")])

    def test_text_not_str_raises_type_error(self):
        with self.assertRaises(TypeError):
            decode_query(123)

    def test_malformed_percent_escape_raises(self):
        with self.assertRaises(QueryStringError):
            decode_query("k=%2")  # incomplete, end of string
        with self.assertRaises(QueryStringError):
            decode_query("k=%")  # bare percent, nothing follows
        with self.assertRaises(QueryStringError):
            decode_query("k=%2g")  # 'g' is not a hex digit

    def test_invalid_utf8_byte_sequence_raises(self):
        with self.assertRaises(QueryStringError):
            decode_query("k=%80")  # a lone UTF-8 continuation byte


class RoundTripTests(unittest.TestCase):
    def test_round_trip_tricky_values(self):
        pairs = [
            ("a", "b"),
            ("space key", "space value"),
            ("eq=sign", "amp&ersand"),
            ("percent", "100%"),
            ("unicode", "café 中 \U0001F600"),
            ("", ""),
            ("dup", "x"),
            ("dup", "y"),
        ]
        self.assertEqual(decode_query(encode_query(pairs)), pairs)


class ExceptionHierarchyTests(unittest.TestCase):
    def test_query_string_error_is_value_error(self):
        self.assertTrue(issubclass(QueryStringError, ValueError))


if __name__ == "__main__":
    unittest.main()
