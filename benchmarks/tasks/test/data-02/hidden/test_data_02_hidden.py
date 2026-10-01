import io
import sys
import unittest

from textkit import main


class TextkitHiddenTests(unittest.TestCase):
    def run_main(self, argv, stdin_text=""):
        stdout = io.StringIO()
        rc = main(argv, io.StringIO(stdin_text), stdout)
        return rc, stdout.getvalue()

    def test_no_args_prints_usage_and_returns_zero(self):
        rc, out = self.run_main([])
        self.assertEqual(rc, 0)
        self.assertEqual(out, "usage: textkit <wordcount|filter|sort> [options]\n")

    def test_help_flag_prints_usage_and_returns_zero(self):
        rc, out = self.run_main(["--help"])
        self.assertEqual(rc, 0)
        self.assertEqual(out, "usage: textkit <wordcount|filter|sort> [options]\n")

    def test_does_not_write_to_real_stdout(self):
        real_stdout = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = real_stdout
        try:
            given_stdout = io.StringIO()
            rc = main([], io.StringIO(""), given_stdout)
        finally:
            sys.stdout = old_stdout
        self.assertEqual(real_stdout.getvalue(), "")
        self.assertEqual(rc, 0)
        self.assertEqual(given_stdout.getvalue(), "usage: textkit <wordcount|filter|sort> [options]\n")

    def test_unknown_command_is_a_usage_error(self):
        rc, out = self.run_main(["bogus"])
        self.assertEqual(rc, 2)
        self.assertEqual(out, "unknown command: bogus\n")

    def test_wordcount_counts_lines_words_and_chars(self):
        rc, out = self.run_main(["wordcount"], "hello world\nfoo\n")
        self.assertEqual(rc, 0)
        self.assertEqual(out, "2 lines, 3 words, 16 chars\n")

    def test_wordcount_on_empty_input(self):
        rc, out = self.run_main(["wordcount"], "")
        self.assertEqual(rc, 0)
        self.assertEqual(out, "0 lines, 0 words, 0 chars\n")

    def test_wordcount_rejects_extra_arguments(self):
        rc, out = self.run_main(["wordcount", "extra"], "hi\n")
        self.assertEqual(rc, 2)
        self.assertEqual(out, "wordcount takes no arguments\n")

    def test_filter_returns_only_matching_lines_in_order(self):
        rc, out = self.run_main(["filter", "foo"], "foo bar\nbaz\nfoofoo\nqux\n")
        self.assertEqual(rc, 0)
        self.assertEqual(out, "foo bar\nfoofoo\n")

    def test_filter_with_no_matches_returns_empty_output(self):
        rc, out = self.run_main(["filter", "zzz"], "foo bar\nbaz\n")
        self.assertEqual(rc, 0)
        self.assertEqual(out, "")

    def test_filter_missing_argument_is_usage_error(self):
        rc, out = self.run_main(["filter"], "a\nb\n")
        self.assertEqual(rc, 2)
        self.assertEqual(out, "filter requires a substring argument\n")

    def test_filter_with_too_many_arguments_is_usage_error(self):
        rc, out = self.run_main(["filter", "a", "b"], "x\n")
        self.assertEqual(rc, 2)
        self.assertEqual(out, "filter requires a substring argument\n")

    def test_sort_ascending_by_default(self):
        rc, out = self.run_main(["sort"], "banana\napple\ncherry\n")
        self.assertEqual(rc, 0)
        self.assertEqual(out, "apple\nbanana\ncherry\n")

    def test_sort_reverse_flag(self):
        rc, out = self.run_main(["sort", "-r"], "banana\napple\ncherry\n")
        self.assertEqual(rc, 0)
        self.assertEqual(out, "cherry\nbanana\napple\n")

    def test_sort_unknown_option_is_usage_error(self):
        rc, out = self.run_main(["sort", "--bogus"], "b\na\n")
        self.assertEqual(rc, 2)
        self.assertEqual(out, "sort: unknown option: --bogus\n")

    def test_sort_with_multiple_arguments_is_usage_error(self):
        rc, out = self.run_main(["sort", "foo", "bar"], "b\na\n")
        self.assertEqual(rc, 2)
        self.assertEqual(out, "sort: unknown option: foo\n")

    def test_main_return_value_is_an_int(self):
        rc, _ = self.run_main(["wordcount"], "hi\n")
        self.assertIsInstance(rc, int)


if __name__ == "__main__":
    unittest.main()
