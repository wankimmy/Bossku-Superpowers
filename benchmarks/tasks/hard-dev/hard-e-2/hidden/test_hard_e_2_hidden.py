import unittest

from httpheader import split_list, parse_params, parse_quality_list, HeaderParseError

BSLASH = chr(92)
DQUOTE = chr(34)


class SplitListTests(unittest.TestCase):
    def test_basic_split_and_trim(self):
        self.assertEqual(split_list("a, b , c"), ["a", "b", "c"])

    def test_empty_elements_dropped(self):
        self.assertEqual(split_list(",a,,b,"), ["a", "b"])
        self.assertEqual(split_list("  ,  "), [])

    def test_quoted_comma_not_split(self):
        value = 'a, ' + DQUOTE + "b,c" + DQUOTE + ", d"
        self.assertEqual(split_list(value), ["a", DQUOTE + "b,c" + DQUOTE, "d"])

    def test_raw_text_preserved_not_unescaped(self):
        value = DQUOTE + "a" + BSLASH + DQUOTE + "b" + DQUOTE + ",c"
        self.assertEqual(split_list(value), [DQUOTE + "a" + BSLASH + DQUOTE + "b" + DQUOTE, "c"])

    def test_unterminated_quote_raises(self):
        with self.assertRaises(HeaderParseError):
            split_list('a,"unterminated')

    def test_invalid_escape_inside_quote_raises(self):
        with self.assertRaises(HeaderParseError):
            split_list(DQUOTE + "bad" + BSLASH + "x" + DQUOTE)

    def test_empty_string_returns_empty_list(self):
        self.assertEqual(split_list(""), [])

    def test_type_error(self):
        with self.assertRaises(TypeError):
            split_list(123)


class ParseParamsTests(unittest.TestCase):
    def test_simple_no_params(self):
        self.assertEqual(parse_params("text/html"), ("text/html", []))

    def test_params_bare_and_quoted(self):
        value = 'text/html; charset=utf-8; Boundary="abc def"'
        self.assertEqual(
            parse_params(value),
            ("text/html", [("charset", "utf-8"), ("boundary", "abc def")]),
        )

    def test_param_keys_lowercased_values_case_preserved(self):
        main, params = parse_params("x; KEY=Value")
        self.assertEqual(params, [("key", "Value")])

    def test_quoted_value_escapes_resolved(self):
        value = "x; a=" + DQUOTE + "b" + BSLASH + DQUOTE + "c" + DQUOTE
        self.assertEqual(parse_params(value), ("x", [("a", "b" + DQUOTE + "c")]))

    def test_duplicate_keys_preserved_in_order(self):
        self.assertEqual(parse_params("x;a=1;a=2"), ("x", [("a", "1"), ("a", "2")]))

    def test_whitespace_around_delimiters_insignificant(self):
        self.assertEqual(parse_params("  x  ;  a = 1  "), ("x", [("a", "1")]))

    def test_empty_value_raises(self):
        with self.assertRaises(HeaderParseError):
            parse_params("")
        with self.assertRaises(HeaderParseError):
            parse_params("   ")

    def test_dangling_semicolon_raises(self):
        with self.assertRaises(HeaderParseError):
            parse_params("x;")

    def test_empty_parameter_between_semicolons_raises(self):
        with self.assertRaises(HeaderParseError):
            parse_params("x;;a=1")

    def test_empty_main_value_raises(self):
        with self.assertRaises(HeaderParseError):
            parse_params(";a=1")

    def test_bare_value_with_space_raises(self):
        with self.assertRaises(HeaderParseError):
            parse_params("x;a=has space")

    def test_value_with_embedded_equals_must_be_quoted(self):
        with self.assertRaises(HeaderParseError):
            parse_params("x;a=b=c")
        self.assertEqual(
            parse_params("x;a=" + DQUOTE + "b=c" + DQUOTE),
            ("x", [("a", "b=c")]),
        )

    def test_param_without_equals_raises(self):
        with self.assertRaises(HeaderParseError):
            parse_params("x;a")

    def test_trailing_chars_after_quoted_value_raises(self):
        with self.assertRaises(HeaderParseError):
            parse_params("x;a=" + DQUOTE + "b" + DQUOTE + "extra")

    def test_unterminated_quoted_value_raises(self):
        with self.assertRaises(HeaderParseError):
            parse_params("x;a=" + DQUOTE + "b")

    def test_semicolon_inside_quoted_value_does_not_split(self):
        value = "x;a=" + DQUOTE + "b;c" + DQUOTE + ";d=2"
        self.assertEqual(parse_params(value), ("x", [("a", "b;c"), ("d", "2")]))

    def test_type_error(self):
        with self.assertRaises(TypeError):
            parse_params(None)


class ParseQualityListTests(unittest.TestCase):
    def test_basic_sort_descending(self):
        self.assertEqual(
            parse_quality_list("en-US,en;q=0.8,fr;q=0.9,*;q=0.1"),
            [("en-US", 1.0), ("fr", 0.9), ("en", 0.8), ("*", 0.1)],
        )

    def test_default_q_is_one(self):
        self.assertEqual(parse_quality_list("a"), [("a", 1.0)])

    def test_ties_preserve_original_order(self):
        self.assertEqual(
            parse_quality_list("a;q=0.5,b;q=0.5,c;q=0.9"),
            [("c", 0.9), ("a", 0.5), ("b", 0.5)],
        )

    def test_q_one_variants(self):
        self.assertEqual(
            parse_quality_list("a;q=1,b;q=1.0,c;q=1.000"),
            [("a", 1.0), ("b", 1.0), ("c", 1.0)],
        )

    def test_q_zero_variants(self):
        result = parse_quality_list("a;q=0,b;q=0.,c;q=0.000")
        self.assertEqual([q for _item, q in result], [0.0, 0.0, 0.0])

    def test_other_params_ignored_but_still_parsed(self):
        self.assertEqual(
            parse_quality_list("a;foo=bar;q=0.3,b;q=0.7"),
            [("b", 0.7), ("a", 0.3)],
        )

    def test_other_malformed_param_still_raises(self):
        with self.assertRaises(HeaderParseError):
            parse_quality_list("a;foo=has space;q=0.3")

    def test_last_duplicate_q_wins(self):
        self.assertEqual(parse_quality_list("a;q=0.1;q=0.9"), [("a", 0.9)])

    def test_empty_elements_dropped_before_parsing(self):
        self.assertEqual(parse_quality_list(",a;q=0.5,,"), [("a", 0.5)])

    def test_invalid_q_values_raise(self):
        for bad in ["1.5", "1.0001", "-0.5", "01", "abc", "", "+1", "1.1"]:
            with self.assertRaises(HeaderParseError):
                parse_quality_list(f"a;q={bad}")

    def test_type_error(self):
        with self.assertRaises(TypeError):
            parse_quality_list(3.14)


if __name__ == "__main__":
    unittest.main()
