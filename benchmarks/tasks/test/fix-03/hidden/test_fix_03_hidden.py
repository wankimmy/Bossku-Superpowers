import unittest

from settings import resolve_settings
from formatter import format_report


class ResolveSettingsHiddenTests(unittest.TestCase):
    def test_none_overrides_gives_all_defaults(self):
        self.assertEqual(
            resolve_settings(None),
            {"indent": 4, "prefix": ">> ", "show_header": True, "tags": ("general",)},
        )

    def test_empty_dict_overrides_gives_all_defaults(self):
        self.assertEqual(
            resolve_settings({}),
            {"indent": 4, "prefix": ">> ", "show_header": True, "tags": ("general",)},
        )

    def test_explicit_none_per_key_falls_back_to_default(self):
        settings = resolve_settings({"indent": None, "tags": None})
        self.assertEqual(settings["indent"], 4)
        self.assertEqual(settings["tags"], ("general",))

    def test_zero_indent_is_respected(self):
        self.assertEqual(resolve_settings({"indent": 0})["indent"], 0)

    def test_empty_prefix_is_respected(self):
        self.assertEqual(resolve_settings({"prefix": ""})["prefix"], "")

    def test_false_show_header_is_respected(self):
        self.assertEqual(resolve_settings({"show_header": False})["show_header"], False)

    def test_empty_tags_is_respected(self):
        self.assertEqual(resolve_settings({"tags": []})["tags"], [])

    def test_mixed_overrides_combine_with_defaults(self):
        settings = resolve_settings({"indent": 0, "show_header": False})
        self.assertEqual(
            settings,
            {"indent": 0, "prefix": ">> ", "show_header": False, "tags": ("general",)},
        )


class FormatReportHiddenTests(unittest.TestCase):
    def test_default_report(self):
        self.assertEqual(
            format_report(["a line", "b line"]),
            "REPORT\n>>     a line\n>>     b line\ntags: general",
        )

    def test_show_header_false_omits_header(self):
        self.assertEqual(format_report(["x"], {"show_header": False}), ">>     x\ntags: general")

    def test_empty_tags_omits_tags_line(self):
        self.assertEqual(format_report(["x"], {"tags": []}), "REPORT\n>>     x")

    def test_zero_indent_and_empty_prefix_remove_padding(self):
        self.assertEqual(
            format_report(["x"], {"indent": 0, "prefix": ""}),
            "REPORT\nx\ntags: general",
        )

    def test_empty_lines_with_defaults(self):
        self.assertEqual(format_report([]), "REPORT\ntags: general")

    def test_empty_lines_header_and_tags_suppressed_gives_empty_string(self):
        self.assertEqual(format_report([], {"show_header": False, "tags": []}), "")

    def test_custom_tags_are_joined(self):
        self.assertEqual(format_report([], {"tags": ["a", "b"]}), "REPORT\ntags: a, b")

    def test_falsy_overrides_end_to_end(self):
        report = format_report(
            ["hi"],
            {"show_header": False, "indent": 0, "prefix": "", "tags": []},
        )
        self.assertEqual(report, "hi")


if __name__ == "__main__":
    unittest.main()
