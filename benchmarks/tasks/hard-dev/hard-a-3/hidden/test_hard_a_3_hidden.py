import unittest

from pipedelim import parse_records, format_records, PipeFormatError


class ParseRecordsTests(unittest.TestCase):
    def test_empty_text_is_zero_records(self):
        self.assertEqual(parse_records(""), [])

    def test_single_newline_is_one_empty_field_record(self):
        self.assertEqual(parse_records("\n"), [[""]])

    def test_two_newlines_is_two_empty_records(self):
        self.assertEqual(parse_records("\n\n"), [[""], [""]])

    def test_consecutive_pipes_make_empty_fields(self):
        self.assertEqual(parse_records("a||b"), [["a", "", "b"]])

    def test_basic_grid(self):
        self.assertEqual(parse_records("a|b\nc|d"), [["a", "b"], ["c", "d"]])

    def test_optional_trailing_newline_is_not_an_extra_record(self):
        self.assertEqual(parse_records("a|b\nc|d\n"), [["a", "b"], ["c", "d"]])

    def test_escaped_pipe_is_literal_in_field(self):
        self.assertEqual(parse_records("a\\|b|c"), [["a|b", "c"]])

    def test_escaped_backslash_is_literal(self):
        self.assertEqual(parse_records("a\\\\b|c"), [["a\\b", "c"]])

    def test_escaped_n_is_a_literal_newline_character(self):
        self.assertEqual(parse_records("a\\nb|c"), [["a\nb", "c"]])

    def test_invalid_escape_sequence_raises(self):
        with self.assertRaises(PipeFormatError):
            parse_records("a\\xb")

    def test_trailing_lone_backslash_raises(self):
        with self.assertRaises(PipeFormatError):
            parse_records("trailing\\")

    def test_non_str_input_raises_type_error(self):
        with self.assertRaises(TypeError):
            parse_records(123)
        with self.assertRaises(TypeError):
            parse_records(None)

    def test_multi_row_mixed_escapes_hardcoded(self):
        text = "a|b\\|c|d\\\\e\nf\\ng|\nsingle\n"
        self.assertEqual(
            parse_records(text),
            [["a", "b|c", "d\\e"], ["f\ng", ""], ["single"]],
        )


class FormatRecordsTests(unittest.TestCase):
    def test_basic_grid_has_no_trailing_separator_garbage(self):
        self.assertEqual(format_records([["a", "b"], ["c", "d"]]), "a|b\nc|d\n")

    def test_empty_list_formats_to_empty_string(self):
        self.assertEqual(format_records([]), "")

    def test_single_row_single_empty_field_is_distinguishable_from_no_rows(self):
        # A record containing one empty field round-trips to "\n", which is
        # NOT the same output as formatting zero records ("").
        encoded = format_records([[""]])
        self.assertEqual(encoded, "\n")
        self.assertNotEqual(encoded, format_records([]))
        self.assertEqual(parse_records(encoded), [[""]])

    def test_escapes_pipe_backslash_and_newline(self):
        self.assertEqual(format_records([["a|b"]]), "a\\|b\n")
        self.assertEqual(format_records([["a\\b"]]), "a\\\\b\n")
        self.assertEqual(format_records([["a\nb"]]), "a\\nb\n")

    def test_multi_row_mixed_escapes_hardcoded(self):
        records = [["a", "b|c", "d\\e"], ["f\ng", ""], ["single"]]
        self.assertEqual(format_records(records), "a|b\\|c|d\\\\e\nf\\ng|\nsingle\n")

    def test_empty_row_raises(self):
        with self.assertRaises(PipeFormatError):
            format_records([[]])

    def test_records_not_a_list_raises_type_error(self):
        with self.assertRaises(TypeError):
            format_records("not a list of rows")

    def test_row_not_a_list_raises_type_error(self):
        with self.assertRaises(TypeError):
            format_records([123])

    def test_field_not_a_str_raises_type_error(self):
        with self.assertRaises(TypeError):
            format_records([[1, "two"]])


class RoundTripTests(unittest.TestCase):
    def test_round_trip_tricky_fields(self):
        tricky_fields = [
            "plain",
            "",
            "has|pipe",
            "has\\backslash",
            "has\nnewline",
            "has\\|both backslash then pipe",
            "unicode é中\U0001F600",
            "tab\tchar",
        ]
        for value in tricky_fields:
            row = [value, "x"]
            with self.subTest(value=value):
                text = format_records([row])
                self.assertEqual(parse_records(text), [row])

    def test_round_trip_general(self):
        records = [["a", "b|c", "d\\e"], ["f\ng", ""], ["single"]]
        self.assertEqual(parse_records(format_records(records)), records)


class ExceptionHierarchyTests(unittest.TestCase):
    def test_pipe_format_error_is_value_error(self):
        self.assertTrue(issubclass(PipeFormatError, ValueError))


if __name__ == "__main__":
    unittest.main()
