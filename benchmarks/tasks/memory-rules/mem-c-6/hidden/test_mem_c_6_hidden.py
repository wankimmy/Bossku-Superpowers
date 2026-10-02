import tempfile
import unittest
from pathlib import Path

import mailmerge


class LoadTemplateFunctionalTests(unittest.TestCase):
    def test_reads_file_contents_unchanged(self):
        handle = tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        )
        handle.write("Hi {{first_name}}!")
        handle.close()
        try:
            self.assertEqual(mailmerge.load_template(handle.name), "Hi {{first_name}}!")
        finally:
            Path(handle.name).unlink(missing_ok=True)


class RenderTemplateFunctionalTests(unittest.TestCase):
    def test_single_placeholder(self):
        result = mailmerge.render_template("Hi {{first_name}}!", {"first_name": "Alice"})
        self.assertEqual(result, "Hi Alice!")

    def test_multiple_placeholders(self):
        result = mailmerge.render_template(
            "Hi {{first_name}}, your code is {{code}}.",
            {"first_name": "Alice", "code": "1234"},
        )
        self.assertEqual(result, "Hi Alice, your code is 1234.")

    def test_repeated_placeholder_substituted_everywhere(self):
        result = mailmerge.render_template("{{name}} and {{name}} again", {"name": "Bo"})
        self.assertEqual(result, "Bo and Bo again")

    def test_missing_key_leaves_placeholder_unchanged(self):
        result = mailmerge.render_template("Hi {{first_name}}!", {})
        self.assertEqual(result, "Hi {{first_name}}!")

    def test_returns_a_string(self):
        result = mailmerge.render_template("plain text", {})
        self.assertIsInstance(result, str)

    def test_template_with_no_placeholders_is_unchanged(self):
        result = mailmerge.render_template("Just plain text here.", {"unused": "x"})
        self.assertEqual(result, "Just plain text here.")


class DoubleBracePlaceholderRuleTests(unittest.TestCase):
    """Project rule: only doubled {{name}} is a placeholder; a lone '{' or
    '}' in the template is left completely untouched, never crashes."""

    def test_literal_single_braces_untouched(self):
        template = 'Example payload: {"key": "value"}'
        try:
            result = mailmerge.render_template(template, {})
        except Exception as exc:  # pragma: no cover - failure path under test
            self.fail(f"render_template raised {exc!r} on a literal brace")
        self.assertEqual(result, template)

    def test_literal_braces_with_values_provided_still_untouched(self):
        template = 'Config: {"ok": true}'
        result = mailmerge.render_template(template, {"ok": "yes", "key": "val"})
        self.assertEqual(result, template)

    def test_numeric_single_brace_not_treated_as_format_placeholder(self):
        # A naive str.format(**values)-style implementation chokes on or
        # mis-substitutes a bare '{0}'-looking token; it must stay literal.
        template = "Item {0} of {1}"
        try:
            result = mailmerge.render_template(template, {"first_name": "Alice"})
        except Exception as exc:  # pragma: no cover - failure path under test
            self.fail(f"render_template raised {exc!r} on single-brace numeric text")
        self.assertEqual(result, template)

    def test_mixed_placeholder_and_literal_braces(self):
        template = 'Hi {{first_name}}, your payload is {"ok": true}.'
        result = mailmerge.render_template(template, {"first_name": "Alice"})
        self.assertEqual(result, 'Hi Alice, your payload is {"ok": true}.')

    def test_placeholder_immediately_next_to_literal_brace(self):
        template = '{{code}}{"x": 1}'
        result = mailmerge.render_template(template, {"code": "99"})
        self.assertEqual(result, '99{"x": 1}')

    def test_unmatched_single_brace_does_not_raise(self):
        template = "An orphan brace: { not closed"
        try:
            result = mailmerge.render_template(template, {})
        except Exception as exc:  # pragma: no cover - failure path under test
            self.fail(f"render_template raised {exc!r} on an unmatched brace")
        self.assertEqual(result, template)


if __name__ == "__main__":
    unittest.main()
