import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from settings import resolve_settings
from formatter import format_report


class SettingsOverrideTests(unittest.TestCase):
    def test_zero_indent_is_respected(self):
        settings = resolve_settings({"indent": 0})
        self.assertEqual(settings["indent"], 0)

    def test_empty_tags_is_respected(self):
        settings = resolve_settings({"tags": []})
        self.assertEqual(settings["tags"], [])

    def test_missing_key_falls_back_to_default(self):
        settings = resolve_settings({})
        self.assertEqual(settings["indent"], 4)

    def test_compact_report_has_no_tags_line(self):
        report = format_report(["hi"], {"show_header": False, "indent": 0, "prefix": "", "tags": []})
        self.assertEqual(report, "hi")


if __name__ == "__main__":
    unittest.main()
