import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import textutils as t


class TextUtilsCharacterizationTests(unittest.TestCase):
    def test_clean_text(self):
        self.assertEqual(t.clean_text("  Hello   WORLD  \n\t there "), "hello world there")

    def test_strip_punctuation_leaves_other_characters(self):
        self.assertEqual(t.strip_punctuation("Hi, there -- ok?"), "Hi there -- ok")

    def test_normalize_strips_then_cleans(self):
        self.assertEqual(t.normalize("cat ; ; dog"), "cat dog")

    def test_word_count(self):
        self.assertEqual(t.word_count("Hi, there! Is this -- ok?"), 6)

    def test_sentence_count(self):
        self.assertEqual(t.sentence_count("Wait... Really?! Yes."), 6)

    def test_longest_word_tie_break(self):
        self.assertEqual(t.longest_word("cat dog owl bat"), "cat")


if __name__ == "__main__":
    unittest.main()
