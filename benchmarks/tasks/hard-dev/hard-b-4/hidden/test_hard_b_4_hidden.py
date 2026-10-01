import unittest

from textstats.tokenize import tokenize
from textstats.frequency import word_frequencies, most_common
from textstats.report import summarize


class TextStatsHiddenTests(unittest.TestCase):
    # ---- tokenize ----

    def test_tokenize_splits_on_multiple_kinds_of_separators(self):
        self.assertEqual(
            tokenize("Hello,   world...123-go!"), ["hello", "world", "go"]
        )

    def test_tokenize_empty_or_non_alpha_string_returns_empty_list(self):
        self.assertEqual(tokenize(""), [])
        self.assertEqual(tokenize("  123 -- 456  "), [])

    def test_tokenize_casefold_unicode_sharp_s(self):
        # "Straße".casefold() == "strasse" == "STRASSE".casefold(), but
        # "Straße".lower() leaves the sharp s alone ("straße" != "strasse").
        self.assertEqual(tokenize("Straße STRASSE"), ["strasse", "strasse"])

    # ---- word_frequencies ----

    def test_word_frequencies_excludes_single_letter_words(self):
        counts = word_frequencies("a cat and a dog, i said")
        self.assertNotIn("a", counts)
        self.assertNotIn("i", counts)
        self.assertEqual(counts["cat"], 1)
        self.assertEqual(counts["dog"], 1)

    def test_word_frequencies_does_not_mutate_caller_stopwords(self):
        my_stopwords = {"the"}
        word_frequencies("the cat sat on the mat", my_stopwords)
        self.assertEqual(my_stopwords, {"the"})

    def test_word_frequencies_custom_stopwords_excluded(self):
        counts = word_frequencies("the cat sat on the mat", {"cat", "mat"})
        self.assertNotIn("cat", counts)
        self.assertNotIn("mat", counts)
        self.assertEqual(counts["the"], 2)
        self.assertEqual(counts["sat"], 1)

    def test_word_frequencies_two_default_calls_do_not_leak_state(self):
        first = word_frequencies("cat cat dog")
        second = word_frequencies("bird")
        self.assertEqual(first, {"cat": 2, "dog": 1})
        self.assertEqual(second, {"bird": 1})

    def test_word_frequencies_empty_text_returns_empty_dict(self):
        self.assertEqual(word_frequencies(""), {})

    # ---- most_common ----

    def test_most_common_includes_the_single_top_word(self):
        counts = {"dog": 5, "cat": 3, "bird": 1}
        self.assertEqual(most_common(counts, 2), [("dog", 5), ("cat", 3)])

    def test_most_common_different_sizes_distinct_counts(self):
        counts = {"x": 10, "y": 9, "z": 8, "w": 1}
        self.assertEqual(
            most_common(counts, 3), [("x", 10), ("y", 9), ("z", 8)]
        )

    def test_most_common_fewer_than_n_returns_all(self):
        counts = {"only": 2}
        self.assertEqual(most_common(counts, 5), [("only", 2)])

    def test_most_common_n_zero_returns_empty_list(self):
        self.assertEqual(most_common({"x": 1}, 0), [])

    def test_most_common_tie_break_is_alphabetical_not_first_seen(self):
        # "mango" is clearly #1 so it doesn't interfere with checking the
        # relative order of the tied pair below it.
        counts = {"mango": 10, "zebra": 2, "apple": 2}
        result_words = [w for w, _ in most_common(counts, 3)]
        tied = [w for w in result_words if w in ("zebra", "apple")]
        self.assertEqual(tied, ["apple", "zebra"])

    # ---- summarize ----

    def test_summarize_basic_integration(self):
        report = summarize("dog dog cat dog bird cat", top_n=2)
        self.assertEqual(report["total_words"], 6)
        self.assertEqual(report["distinct_words"], 3)
        self.assertEqual(report["top_words"], [("dog", 3), ("cat", 2)])

    def test_summarize_top_n_zero_returns_empty_top_words(self):
        report = summarize("dog dog cat", top_n=0)
        self.assertEqual(report["top_words"], [])
        self.assertEqual(report["total_words"], 3)

    def test_summarize_excludes_stopwords_and_single_letters(self):
        report = summarize("a dog and a cat", stopwords={"and"}, top_n=5)
        self.assertEqual(report["distinct_words"], 2)
        self.assertEqual(report["total_words"], 2)


if __name__ == "__main__":
    unittest.main()
