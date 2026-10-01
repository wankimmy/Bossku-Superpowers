import unittest

from globmatch import match, filter_paths, GlobPatternError


class LiteralAndWildcardTests(unittest.TestCase):
    def test_literal_match(self):
        self.assertTrue(match("a/b.py", "a/b.py"))

    def test_literal_mismatch(self):
        self.assertFalse(match("a/b.py", "a/b.txt"))

    def test_star_matches_within_segment(self):
        self.assertTrue(match("*.py", "main.py"))

    def test_star_does_not_cross_slash(self):
        self.assertFalse(match("*.py", "sub/main.py"))

    def test_star_matches_zero_chars(self):
        self.assertTrue(match("a*b", "ab"))

    def test_question_matches_exactly_one_char(self):
        self.assertTrue(match("a?c", "abc"))
        self.assertFalse(match("a?c", "ac"))
        self.assertFalse(match("a?c", "abbc"))
        self.assertFalse(match("a?c", "a/c"))

    def test_case_sensitive(self):
        self.assertFalse(match("*.PY", "main.py"))

    def test_dotfiles_matched_normally(self):
        self.assertTrue(match("*", ".hidden"))
        self.assertTrue(match(".*", ".hidden"))


class CharacterClassTests(unittest.TestCase):
    def test_simple_membership(self):
        self.assertTrue(match("[abc].txt", "a.txt"))
        self.assertFalse(match("[abc].txt", "d.txt"))

    def test_range(self):
        self.assertTrue(match("[a-z]*.py", "q.py"))
        self.assertFalse(match("[a-z]*.py", "Q.py"))

    def test_combined_range_and_literals(self):
        self.assertTrue(match("[a-cx]", "x"))
        self.assertTrue(match("[a-cx]", "b"))
        self.assertFalse(match("[a-cx]", "d"))

    def test_negation_bang_and_caret(self):
        self.assertTrue(match("[!abc].txt", "d.txt"))
        self.assertFalse(match("[!abc].txt", "a.txt"))
        self.assertTrue(match("[^abc].txt", "d.txt"))
        self.assertFalse(match("[^abc].txt", "a.txt"))

    def test_literal_closing_bracket_as_first_member(self):
        self.assertTrue(match("[]ab]", "]"))
        self.assertTrue(match("[]ab]", "a"))
        self.assertFalse(match("[]ab]", "c"))

    def test_literal_hyphen_leading_and_trailing(self):
        self.assertTrue(match("[-ab]", "-"))
        self.assertFalse(match("[-ab]", "c"))
        self.assertTrue(match("[ab-]", "-"))
        self.assertFalse(match("[ab-]", "c"))

    def test_backslash_has_no_special_meaning_inside_class(self):
        # a literal backslash character is just an ordinary member here
        self.assertTrue(match("[a" + chr(92) + "b]", chr(92)))

    def test_unterminated_class_raises(self):
        with self.assertRaises(GlobPatternError):
            match("a[bc", "abc")

    def test_backward_range_raises(self):
        with self.assertRaises(GlobPatternError):
            match("[z-a]", "m")


class EscapeTests(unittest.TestCase):
    def test_escaped_star_is_literal(self):
        pat = "a" + chr(92) + "*b"
        self.assertTrue(match(pat, "a*b"))
        self.assertFalse(match(pat, "axb"))

    def test_escaped_question_is_literal(self):
        pat = "a" + chr(92) + "?b"
        self.assertTrue(match(pat, "a?b"))
        self.assertFalse(match(pat, "axb"))

    def test_escaped_backslash_is_literal(self):
        pat = "a" + chr(92) + chr(92) + "b"
        self.assertTrue(match(pat, "a" + chr(92) + "b"))

    def test_trailing_backslash_raises(self):
        with self.assertRaises(GlobPatternError):
            match("a" + chr(92), "a")


class GlobstarTests(unittest.TestCase):
    def test_globstar_matches_variable_segment_counts(self):
        self.assertTrue(match("a/**/b", "a/b"))
        self.assertTrue(match("a/**/b", "a/x/b"))
        self.assertTrue(match("a/**/b", "a/x/y/z/b"))

    def test_globstar_requires_prefix_and_suffix_to_match(self):
        self.assertFalse(match("a/**/b", "c/x/b"))
        self.assertFalse(match("a/**/b", "a/x/c"))

    def test_leading_globstar(self):
        self.assertTrue(match("**/b.py", "b.py"))
        self.assertTrue(match("**/b.py", "x/y/b.py"))

    def test_trailing_globstar(self):
        self.assertTrue(match("a/**", "a"))
        self.assertTrue(match("a/**", "a/b/c"))

    def test_trailing_globstar_requires_prefix(self):
        self.assertFalse(match("a/**", "x/b/c"))

    def test_consecutive_globstars_behave_as_one(self):
        self.assertTrue(match("a/**/**/b", "a/b"))
        self.assertTrue(match("a/**/**/b", "a/x/y/b"))

    def test_bare_globstar_matches_everything(self):
        self.assertTrue(match("**", "a"))
        self.assertTrue(match("**", "a/b/c"))

    def test_three_stars_is_not_globstar(self):
        # "***" is an ordinary single-segment wildcard, not a globstar: it
        # must occupy exactly one path segment.
        self.assertFalse(match("a/***/b", "a/x/y/b"))
        self.assertTrue(match("a/***/b", "a/xyz/b"))
        self.assertTrue(match("a/***/b", "a//b"))

    def test_double_star_adjacent_to_text_is_not_globstar(self):
        # "a**b" is the ordinary segment a,*,*,b -- same language as "a*b" --
        # and still must not cross a slash.
        self.assertTrue(match("a**b", "axyzb"))
        self.assertFalse(match("a**b", "a/b"))
        self.assertEqual(match("a**b", "axyzb"), match("a*b", "axyzb"))


class ValidationTests(unittest.TestCase):
    def test_malformed_slash_patterns_raise(self):
        with self.assertRaises(GlobPatternError):
            match("/a", "a")
        with self.assertRaises(GlobPatternError):
            match("a/", "a")
        with self.assertRaises(GlobPatternError):
            match("a//b", "a/b")

    def test_empty_pattern_raises(self):
        with self.assertRaises(GlobPatternError):
            match("", "a")

    def test_pattern_type_error(self):
        with self.assertRaises(TypeError):
            match(123, "a")

    def test_path_type_error(self):
        with self.assertRaises(TypeError):
            match("a", 123)

    def test_empty_path_segment_matched_by_star_not_literal(self):
        # path "a//b" has segments ["a", "", "b"]; an empty segment is not
        # an error in a *path* -- it is matched by ordinary segment rules.
        self.assertTrue(match("a/*/b", "a//b"))
        self.assertFalse(match("a/x/b", "a//b"))


class FilterPathsTests(unittest.TestCase):
    def test_preserves_order_and_filters(self):
        paths = ["a/b.py", "a/c.txt", "x/y/b.py", "a/d.py"]
        self.assertEqual(filter_paths("a/*.py", paths), ["a/b.py", "a/d.py"])

    def test_globstar_filter(self):
        paths = ["a/b.py", "a/c.txt", "x/y/b.py"]
        self.assertEqual(filter_paths("**/*.py", paths), ["a/b.py", "x/y/b.py"])

    def test_does_not_mutate_input_list(self):
        paths = ["a/b.py", "a/c.txt"]
        original = list(paths)
        filter_paths("a/*.py", paths)
        self.assertEqual(paths, original)

    def test_accepts_tuple(self):
        paths = ("a/b.py", "a/c.txt")
        self.assertEqual(filter_paths("a/*.py", paths), ["a/b.py"])

    def test_rejects_non_list_tuple(self):
        with self.assertRaises(TypeError):
            filter_paths("a/*.py", "a/b.py")

    def test_rejects_non_str_entries(self):
        with self.assertRaises(TypeError):
            filter_paths("a/*.py", ["a/b.py", 42])

    def test_validates_pattern_even_with_empty_paths(self):
        with self.assertRaises(GlobPatternError):
            filter_paths("", [])

    def test_empty_result_on_no_matches(self):
        self.assertEqual(filter_paths("*.py", ["a.txt", "b.txt"]), [])


if __name__ == "__main__":
    unittest.main()
