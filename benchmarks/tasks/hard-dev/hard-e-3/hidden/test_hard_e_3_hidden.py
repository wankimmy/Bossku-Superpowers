import unittest

from justify import justify_paragraph, justify_text, JustifyError


class JustifyParagraphTests(unittest.TestCase):
    def test_classic_example(self):
        self.assertEqual(
            justify_paragraph("This is an example of text justification.", 16),
            ["This    is    an", "example  of text", "justification.  "],
        )

    def test_empty_text_returns_empty_list(self):
        self.assertEqual(justify_paragraph("", 10), [])

    def test_whitespace_only_text_returns_empty_list(self):
        self.assertEqual(justify_paragraph("   \t  \n  ", 10), [])

    def test_tabs_and_newlines_are_whitespace(self):
        self.assertEqual(justify_paragraph("a\tb\nc", 10), ["a b c     "])

    def test_single_line_paragraph_not_stretched(self):
        # the only line of a paragraph is also its last line -- never
        # stretched, just left-justified and padded.
        self.assertEqual(justify_paragraph("a b c", 10), ["a b c     "])

    def test_exact_fit_two_words(self):
        self.assertEqual(justify_paragraph("ab cd", 5), ["ab cd"])

    def test_remainder_goes_to_leftmost_gaps(self):
        words = " ".join(["a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
                           "k", "l", "m", "n", "o", "p", "q", "r", "s", "t"])
        self.assertEqual(
            justify_paragraph(words, 10),
            ["a  b c d e", "f  g h i j", "k  l m n o", "p q r s t "],
        )

    def test_every_non_last_line_is_exactly_width(self):
        lines = justify_paragraph(
            "the quick brown fox jumps over the lazy dog again and again", 12
        )
        for line in lines[:-1]:
            self.assertEqual(len(line), 12)

    def test_single_word_line_in_middle_not_stretched(self):
        self.assertEqual(
            justify_paragraph("x " + "Y" * 12 + " z", 8),
            ["x       ", "Y" * 12, "z       "],
        )

    def test_overlong_word_placed_alone_unpadded(self):
        self.assertEqual(
            justify_paragraph("supercalifragilisticexpialidocious", 10),
            ["supercalifragilisticexpialidocious"],
        )

    def test_word_exactly_equal_to_width_not_padded(self):
        self.assertEqual(justify_paragraph("abcde", 5), ["abcde"])

    def test_narrow_width_forces_one_word_per_line(self):
        self.assertEqual(justify_paragraph("a b c", 1), ["a", "b", "c"])

    def test_two_word_non_last_line_single_gap_stretch(self):
        self.assertEqual(justify_paragraph("aaa bb c dd", 6), ["aaa bb", "c dd  "])

    def test_type_error_text_not_str(self):
        with self.assertRaises(TypeError):
            justify_paragraph(123, 10)

    def test_type_error_width_not_int(self):
        with self.assertRaises(TypeError):
            justify_paragraph("abc", "10")

    def test_type_error_width_bool(self):
        with self.assertRaises(TypeError):
            justify_paragraph("abc", True)

    def test_type_error_width_float(self):
        with self.assertRaises(TypeError):
            justify_paragraph("abc", 10.5)

    def test_justify_error_width_zero(self):
        with self.assertRaises(JustifyError):
            justify_paragraph("abc", 0)

    def test_justify_error_width_negative(self):
        with self.assertRaises(JustifyError):
            justify_paragraph("abc", -5)

    def test_justify_error_is_value_error(self):
        self.assertTrue(issubclass(JustifyError, ValueError))


class JustifyTextTests(unittest.TestCase):
    def test_multi_paragraph_and_blank_line_collapsing(self):
        text = "Hello world\nthis is one paragraph.\n\n\nSecond paragraph here.\n\n\n"
        expected = (
            "Hello     \nworld this\nis     one\nparagraph.\n\n"
            "Second    \nparagraph \nhere.     "
        )
        self.assertEqual(justify_text(text, 10), expected)

    def test_leading_blank_lines_dropped(self):
        text = "\n\n\nLeading blanks then text.\n\nMore.\n\n\n"
        expected = "Leading   \nblanks    \nthen text.\n\nMore.     "
        self.assertEqual(justify_text(text, 10), expected)

    def test_internal_line_breaks_are_reflowed(self):
        # the same paragraph content, split across physical lines
        # differently, must justify identically.
        text_a = "one two three four five six"
        text_b = "one two\nthree four\nfive six"
        self.assertEqual(justify_text(text_a, 10), justify_text(text_b, 10))

    def test_empty_text_returns_empty_string(self):
        self.assertEqual(justify_text("", 10), "")

    def test_all_blank_text_returns_empty_string(self):
        self.assertEqual(justify_text("\n\n   \n\t\n", 10), "")

    def test_single_paragraph_matches_justify_paragraph(self):
        text = "a plain single paragraph with several words in it"
        self.assertEqual(
            justify_text(text, 9),
            "\n".join(justify_paragraph(text, 9)),
        )

    def test_type_error_text_not_str(self):
        with self.assertRaises(TypeError):
            justify_text(None, 10)

    def test_type_error_width_bool(self):
        with self.assertRaises(TypeError):
            justify_text("abc", False)

    def test_justify_error_width_zero(self):
        with self.assertRaises(JustifyError):
            justify_text("abc", 0)

    def test_single_blank_line_between_paragraphs_same_as_many(self):
        one_blank = justify_text("para one\n\npara two", 10)
        three_blanks = justify_text("para one\n\n\n\npara two", 10)
        self.assertEqual(one_blank, three_blanks)


if __name__ == "__main__":
    unittest.main()
