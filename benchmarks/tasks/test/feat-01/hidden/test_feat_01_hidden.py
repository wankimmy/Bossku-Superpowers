import unittest

from tinyconfig import parse, ConfigError


class TinyConfigTests(unittest.TestCase):
    def test_plain_int_and_float(self):
        self.assertEqual(parse("count = 5\nratio = 2.5"), {"count": 5, "ratio": 2.5})

    def test_negative_numbers(self):
        self.assertEqual(parse("a = -5\nb = -2.5"), {"a": -5, "b": -2.5})

    def test_booleans_any_case(self):
        result = parse("x = true\ny = FALSE\nz = True")
        self.assertEqual(result, {"x": True, "y": False, "z": True})

    def test_blank_lines_and_comments_ignored(self):
        text = "\n# a comment\nkeep = 1\n   # indented comment\n\n"
        self.assertEqual(parse(text), {"keep": 1})

    def test_whitespace_around_key_and_value_stripped(self):
        self.assertEqual(parse("   name   =   42   "), {"name": 42})

    def test_duration_units(self):
        result = parse("a = 250ms\nb = 2s\nc = 1.5m\nd = 2h\ne = 1d")
        self.assertEqual(result["a"], 0.25)
        self.assertEqual(result["b"], 2.0)
        self.assertEqual(result["c"], 90.0)
        self.assertEqual(result["d"], 7200.0)
        self.assertEqual(result["e"], 86400.0)
        for key in result:
            self.assertIsInstance(result[key], float)

    def test_size_units_decimal_and_binary(self):
        result = parse("a = 2KB\nb = 2MB\nc = 2GB\nd = 2KiB\ne = 2MiB\nf = 2GiB\ng = 10B")
        self.assertEqual(result, {
            "a": 2000, "b": 2_000_000, "c": 2_000_000_000,
            "d": 2048, "e": 2 * 1024 ** 2, "f": 2 * 1024 ** 3, "g": 10,
        })
        for key in result:
            self.assertIsInstance(result[key], int)

    def test_units_are_case_sensitive_and_fall_back_to_string(self):
        result = parse("a = 5mb\nb = 5S")
        self.assertEqual(result, {"a": "5mb", "b": "5S"})

    def test_quoted_string_with_escapes(self):
        text = r'greeting = "say \"hi\""'
        self.assertEqual(parse(text), {"greeting": 'say "hi"'})

    def test_quoted_string_with_escaped_backslash(self):
        text = r'path = "a\\b"'
        self.assertEqual(parse(text), {"path": "a\\b"})

    def test_bare_word_without_whitespace_is_a_string(self):
        self.assertEqual(parse("mode = fast"), {"mode": "fast"})

    def test_unquoted_value_with_whitespace_raises(self):
        with self.assertRaises(ConfigError) as cm:
            parse("x = hello world")
        self.assertEqual(cm.exception.line, 1)

    def test_unterminated_quote_raises(self):
        with self.assertRaises(ConfigError):
            parse('x = "never closed')

    def test_line_without_equals_raises_with_correct_line_number(self):
        with self.assertRaises(ConfigError) as cm:
            parse("a = 1\njustsomeword\nb = 2")
        self.assertEqual(cm.exception.line, 2)

    def test_empty_key_raises(self):
        with self.assertRaises(ConfigError) as cm:
            parse("= 5")
        self.assertEqual(cm.exception.line, 1)

    def test_empty_value_raises(self):
        with self.assertRaises(ConfigError) as cm:
            parse("x = ")
        self.assertEqual(cm.exception.line, 1)

    def test_duplicate_key_last_one_wins(self):
        self.assertEqual(parse("x = 1\ny = 2\nx = 3"), {"x": 3, "y": 2})

    def test_duplicate_key_raises_on_earlier_invalid_line_even_if_later_is_valid(self):
        text = "x = 5 nope\nx = 5s"
        with self.assertRaises(ConfigError) as cm:
            parse(text)
        self.assertEqual(cm.exception.line, 1)

    def test_multiple_valid_entries_of_mixed_types(self):
        text = "\n".join([
            "# server config",
            "name = \"edge-1\"",
            "timeout = 30s",
            "max_size = 4MiB",
            "debug = false",
            "weight = 1.5",
        ])
        self.assertEqual(parse(text), {
            "name": "edge-1",
            "timeout": 30.0,
            "max_size": 4 * 1024 ** 2,
            "debug": False,
            "weight": 1.5,
        })


if __name__ == "__main__":
    unittest.main()
