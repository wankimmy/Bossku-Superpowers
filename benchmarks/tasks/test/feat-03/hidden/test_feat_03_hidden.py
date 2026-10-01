import unittest

from template import render, wrap, TemplateError


class RenderTests(unittest.TestCase):
    def test_simple_substitution(self):
        self.assertEqual(render("Hello {{name}}!", {"name": "World"}), "Hello World!")

    def test_whitespace_inside_braces_is_ignored(self):
        self.assertEqual(render("{{  name  }}", {"name": "x"}), "x")

    def test_nested_dotted_path(self):
        self.assertEqual(render("{{user.city}}", {"user": {"city": "KL"}}), "KL")

    def test_three_level_nested_path(self):
        self.assertEqual(render("{{a.b.c}}", {"a": {"b": {"c": 42}}}), "42")

    def test_plain_text_with_no_placeholders_is_unchanged(self):
        self.assertEqual(render("just plain text", {}), "just plain text")

    def test_missing_top_level_key_raises_with_name(self):
        with self.assertRaises(TemplateError) as cm:
            render("{{missing}}", {})
        self.assertIn("missing", str(cm.exception))

    def test_missing_nested_key_raises_with_full_dotted_path(self):
        with self.assertRaises(TemplateError) as cm:
            render("{{user.address.city}}", {"user": {"name": "Al"}})
        self.assertIn("user.address.city", str(cm.exception))

    def test_non_dict_intermediate_value_raises(self):
        with self.assertRaises(TemplateError) as cm:
            render("{{user.name}}", {"user": "Al"})
        self.assertIn("user.name", str(cm.exception))

    def test_unclosed_placeholder_raises(self):
        with self.assertRaises(TemplateError):
            render("hello {{oops", {})

    def test_escaped_double_brace_is_literal_and_rest_is_plain_text(self):
        self.assertEqual(render(r"\{{x}}", {"x": "ignored"}), "{{x}}")

    def test_escaped_backslash_then_real_placeholder(self):
        self.assertEqual(render(r"\\{{x}}", {"x": "Y"}), "\\Y")

    def test_mixed_escaped_and_real_placeholder(self):
        self.assertEqual(render(r"a \{{b}} c {{d}}", {"d": "D"}), "a {{b}} c D")

    def test_non_string_values_are_stringified(self):
        result = render("{{n}}-{{b}}-{{v}}", {"n": 5, "b": True, "v": None})
        self.assertEqual(result, "5-True-None")


class WrapTests(unittest.TestCase):
    def test_basic_greedy_packing(self):
        result = wrap("the quick brown fox jumps", 10)
        self.assertEqual(result, "the quick\nbrown fox\njumps")

    def test_whitespace_runs_collapse_to_single_spaces(self):
        result = wrap("a   b\nc\n\nd", 10)
        self.assertEqual(result, "a b c d")

    def test_overlong_word_stays_alone_on_its_own_line(self):
        result = wrap("hi there supercalifragilistic now", 5)
        self.assertEqual(result, "hi\nthere\nsupercalifragilistic\nnow")

    def test_consecutive_overlong_words_each_get_their_own_line(self):
        result = wrap("aaaaaaaaaa bbbbbbbbbb ok", 5)
        self.assertEqual(result, "aaaaaaaaaa\nbbbbbbbbbb\nok")

    def test_non_positive_width_raises(self):
        with self.assertRaises(ValueError):
            wrap("text", 0)
        with self.assertRaises(ValueError):
            wrap("text", -3)

    def test_empty_or_whitespace_only_text_returns_empty_string(self):
        self.assertEqual(wrap("   \n  ", 10), "")
        self.assertEqual(wrap("", 10), "")


if __name__ == "__main__":
    unittest.main()
