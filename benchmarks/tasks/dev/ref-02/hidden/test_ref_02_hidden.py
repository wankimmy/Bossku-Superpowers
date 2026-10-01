import unittest

import textutils as t


class TextUtilsCharacterizationHiddenTests(unittest.TestCase):
    def test_clean_text_lowercases_collapses_and_strips(self):
        self.assertEqual(t.clean_text("  Hello   WORLD  \n\t there "), "hello world there")

    def test_strip_punctuation_removes_only_the_specified_set(self):
        text = "Hi, there! Is this -- ok? (yes) [sure] 'quote\" end."
        self.assertEqual(
            t.strip_punctuation(text),
            "Hi there Is this -- ok yes sure quote end",
        )

    def test_normalize_order_matters(self):
        # stripping punctuation first can leave extra whitespace that still needs collapsing
        self.assertEqual(t.normalize("cat ; ; dog"), "cat dog")

    def test_title_case(self):
        self.assertEqual(t.title_case("the Quick-brown fox!!"), "The Quick-brown Fox")

    def test_word_count_counts_whitespace_separated_tokens(self):
        self.assertEqual(t.word_count("Hi, there! Is this -- ok?"), 6)

    def test_word_count_empty_is_zero(self):
        self.assertEqual(t.word_count(""), 0)
        self.assertEqual(t.word_count("...!!!"), 0)

    def test_sentence_count_counts_only_period_bang_question(self):
        self.assertEqual(t.sentence_count("Wait... Really?! Yes."), 6)
        self.assertEqual(t.sentence_count("No sentence punctuation here"), 0)

    def test_average_word_length_rounds_to_two_decimals(self):
        self.assertEqual(t.average_word_length("a bb ccc"), 2.0)

    def test_average_word_length_empty_is_zero(self):
        self.assertEqual(t.average_word_length("   "), 0.0)

    def test_longest_word_ties_use_first_occurrence(self):
        self.assertEqual(t.longest_word("cat dog owl bat"), "cat")

    def test_longest_word_empty_is_empty_string(self):
        self.assertEqual(t.longest_word("..."), "")


class ModuleSplitStructuralHiddenTests(unittest.TestCase):
    def test_cleaning_module_exports_working_functions(self):
        import cleaning

        self.assertEqual(cleaning.clean_text("  A   B "), "a b")
        self.assertEqual(cleaning.strip_punctuation("a@b#c!"), "a@b#c")
        self.assertEqual(cleaning.normalize("cat ; ; dog"), "cat dog")
        self.assertEqual(cleaning.title_case("hello world"), "Hello World")

    def test_analysis_module_exports_working_functions(self):
        import analysis

        self.assertEqual(analysis.word_count("one two three"), 3)
        self.assertEqual(analysis.sentence_count("Hi! Bye?"), 2)
        self.assertEqual(analysis.average_word_length("aa bb"), 2.0)
        self.assertEqual(analysis.longest_word("aa bbb c"), "bbb")

    def test_textutils_reexports_are_the_same_objects_not_copies(self):
        import cleaning
        import analysis

        self.assertIs(t.clean_text, cleaning.clean_text)
        self.assertIs(t.strip_punctuation, cleaning.strip_punctuation)
        self.assertIs(t.normalize, cleaning.normalize)
        self.assertIs(t.title_case, cleaning.title_case)
        self.assertIs(t.word_count, analysis.word_count)
        self.assertIs(t.sentence_count, analysis.sentence_count)
        self.assertIs(t.average_word_length, analysis.average_word_length)
        self.assertIs(t.longest_word, analysis.longest_word)


if __name__ == "__main__":
    unittest.main()
