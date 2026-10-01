import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest

from textstats.tokenize import tokenize
from textstats.frequency import word_frequencies, most_common


class TextStatsTests(unittest.TestCase):
    def test_tokenize_splits_on_punctuation(self):
        self.assertEqual(tokenize("Hello, world!"), ["hello", "world"])

    def test_word_frequencies_basic_counts(self):
        counts = word_frequencies("the cat sat on the mat")
        self.assertEqual(counts["the"], 2)
        self.assertEqual(counts["cat"], 1)

    def test_single_letter_words_excluded(self):
        counts = word_frequencies("a cat and a dog")
        self.assertNotIn("a", counts)

    def test_most_common_top_two(self):
        counts = {"dog": 5, "cat": 3, "bird": 1}
        self.assertEqual(most_common(counts, 2), [("dog", 5), ("cat", 3)])


if __name__ == "__main__":
    unittest.main()
