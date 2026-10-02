import tempfile
import unittest
from pathlib import Path

import settings

CONFIG_TEXT = """
# config for admin app
max_retries=5
timeout_seconds = 30
max_login_attempts=3
db_url=postgres://user:pass@host/db_name
"""


def write_config():
    handle = tempfile.NamedTemporaryFile(
        mode="w", suffix=".cfg", delete=False, encoding="utf-8"
    )
    handle.write(CONFIG_TEXT)
    handle.close()
    return handle.name


class LoadSettingsFunctionalTests(unittest.TestCase):
    def setUp(self):
        self.path = write_config()
        self.addCleanup(lambda: Path(self.path).unlink(missing_ok=True))

    def test_parses_simple_keys(self):
        result = settings.load_settings(self.path)
        self.assertEqual(result["max_retries"], "5")

    def test_ignores_comments_and_blank_lines(self):
        result = settings.load_settings(self.path)
        self.assertNotIn("# config for admin app", result)
        self.assertEqual(len(result), 4)

    def test_strips_whitespace_around_key_and_value(self):
        result = settings.load_settings(self.path)
        self.assertEqual(result["timeout_seconds"], "30")

    def test_values_are_plain_strings(self):
        result = settings.load_settings(self.path)
        self.assertIsInstance(result["max_retries"], str)

    def test_internal_dict_keys_stay_snake_case(self):
        result = settings.load_settings(self.path)
        self.assertIn("max_login_attempts", result)
        self.assertIn("db_url", result)


class ApiResponseFunctionalTests(unittest.TestCase):
    def setUp(self):
        self.path = write_config()
        self.addCleanup(lambda: Path(self.path).unlink(missing_ok=True))
        self.loaded = settings.load_settings(self.path)

    def test_includes_source_file(self):
        response = settings.settings_api_response(self.loaded)
        self.assertEqual(response["source"], "file")

    def test_has_one_more_key_than_input(self):
        response = settings.settings_api_response(self.loaded)
        self.assertEqual(len(response), len(self.loaded) + 1)

    def test_returns_a_dict(self):
        response = settings.settings_api_response(self.loaded)
        self.assertIsInstance(response, dict)

    def test_values_preserved_exactly(self):
        response = settings.settings_api_response(self.loaded)
        self.assertEqual(response["dbUrl"], "postgres://user:pass@host/db_name")


class CamelCaseBoundaryRuleTests(unittest.TestCase):
    """Project rule: keys crossing the JSON/API boundary must be camelCase;
    internal dicts stay snake_case."""

    def setUp(self):
        self.path = write_config()
        self.addCleanup(lambda: Path(self.path).unlink(missing_ok=True))
        self.loaded = settings.load_settings(self.path)
        self.response = settings.settings_api_response(self.loaded)

    def test_two_word_key_converted(self):
        self.assertIn("maxRetries", self.response)
        self.assertEqual(self.response["maxRetries"], "5")

    def test_three_word_key_converted(self):
        self.assertIn("maxLoginAttempts", self.response)
        self.assertEqual(self.response["maxLoginAttempts"], "3")

    def test_two_word_key_with_spacing_converted(self):
        self.assertIn("timeoutSeconds", self.response)

    def test_db_url_key_converted(self):
        self.assertIn("dbUrl", self.response)

    def test_no_response_key_contains_an_underscore(self):
        for key in self.response:
            self.assertNotIn("_", key, f"key {key!r} should be camelCase, not snake_case")

    def test_original_snake_case_keys_not_present_in_response(self):
        for original_key in ("max_retries", "timeout_seconds", "max_login_attempts", "db_url"):
            self.assertNotIn(original_key, self.response)

    def test_source_level_loader_output_is_unaffected_by_camel_case(self):
        # load_settings itself must stay snake_case internally -- the
        # conversion only happens at the API-response boundary.
        self.assertIn("max_retries", self.loaded)
        self.assertNotIn("maxRetries", self.loaded)


if __name__ == "__main__":
    unittest.main()
