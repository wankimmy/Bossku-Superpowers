import io
import os
import tempfile
import unittest
import warnings
from contextlib import redirect_stdout
from dataclasses import FrozenInstanceError
from datetime import datetime

import cli
from render import RenderOptions, render_message
from history import render_history


TS = datetime(2024, 1, 1, 9, 30)


class RenderMessageTests(unittest.TestCase):
    def test_defaults_match_explicit_default_options(self):
        a = render_message("alice", "hello", TS)
        b = render_message("alice", "hello", TS, options=RenderOptions())
        self.assertEqual(a, b)

    def test_no_warning_with_pure_defaults(self):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            render_message("alice", "hello", TS)
        self.assertEqual(len(caught), 0)

    def test_legacy_positional_width_warns_and_still_works(self):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            out = render_message("alice", "x" * 60, TS, 40)
        self.assertEqual(len(caught), 1)
        self.assertIs(caught[0].category, DeprecationWarning)
        self.assertEqual(len(out), 40)
        self.assertTrue(out.endswith("..."))

    def test_legacy_keyword_equal_to_default_still_warns(self):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            render_message("alice", "hello", TS, width=72)
        self.assertEqual(len(caught), 1)
        self.assertIs(caught[0].category, DeprecationWarning)

    def test_legacy_show_timestamp_false(self):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            out = render_message("alice", "hello", TS, show_timestamp=False)
        self.assertEqual(len(caught), 1)
        self.assertFalse(out.startswith("["))

    def test_options_object_no_warning(self):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            render_message("alice", "hello", TS, options=RenderOptions(width=40))
        self.assertEqual(len(caught), 0)

    def test_conflicting_options_and_legacy_raises_typeerror(self):
        with self.assertRaises(TypeError):
            render_message("alice", "hello", TS, width=40, options=RenderOptions())

    def test_author_truncated_with_ellipsis(self):
        out = render_message(
            "averyverylongname", "hi", TS, options=RenderOptions(author_width=8)
        )
        label = out.split(": ", 1)[0].split("] ")[-1]
        self.assertTrue(label.endswith("…"))
        self.assertEqual(len(label), 8)

    def test_author_padded_when_short(self):
        out = render_message(
            "bo", "hi", TS, options=RenderOptions(author_width=8, show_timestamp=False)
        )
        label = out.split(":", 1)[0]
        self.assertEqual(len(label), 8)

    def test_width_too_small_raises_valueerror(self):
        with self.assertRaises(ValueError):
            render_message("bob", "hello", TS, options=RenderOptions(width=2))

    def test_render_options_is_frozen(self):
        opts = RenderOptions()
        with self.assertRaises(FrozenInstanceError):
            opts.width = 10

    def test_render_options_equality(self):
        self.assertEqual(RenderOptions(), RenderOptions(72, True, "%H:%M", 12))


class RenderHistoryTests(unittest.TestCase):
    def _messages(self, n):
        return [
            {"author": f"user{i}", "text": f"message {i}", "timestamp": TS}
            for i in range(n)
        ]

    def test_empty_history_is_empty_string(self):
        self.assertEqual(render_history([]), "")

    def test_matches_individual_render_message_calls(self):
        msgs = self._messages(3)
        expected = "\n".join(
            render_message(m["author"], m["text"], m["timestamp"]) for m in msgs
        )
        self.assertEqual(render_history(msgs), expected)

    def test_legacy_kwarg_warns_exactly_once_for_whole_call(self):
        msgs = self._messages(5)
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            render_history(msgs, width=30)
        self.assertEqual(len(caught), 1)
        self.assertIs(caught[0].category, DeprecationWarning)

    def test_options_object_no_warning(self):
        msgs = self._messages(4)
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            render_history(msgs, options=RenderOptions(width=30))
        self.assertEqual(len(caught), 0)

    def test_conflicting_raises_typeerror(self):
        with self.assertRaises(TypeError):
            render_history(self._messages(2), width=30, options=RenderOptions())


class CliCompatibilityTests(unittest.TestCase):
    def test_cli_main_still_works_with_legacy_call_site(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "log.txt")
            with open(path, "w", encoding="utf-8") as handle:
                handle.write("09:30|alice|hello there this is a long message\n")
                handle.write("09:31|bob|hi\n")
            buf = io.StringIO()
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                with redirect_stdout(buf):
                    cli.main([path])
        lines = buf.getvalue().splitlines()
        self.assertEqual(len(lines), 2)
        self.assertEqual(len(lines[0]), 40)
        self.assertTrue(lines[0].endswith("..."))
        self.assertIn("hi", lines[1])

    def test_cli_main_legacy_call_site_still_warns(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "log.txt")
            with open(path, "w", encoding="utf-8") as handle:
                handle.write("09:30|alice|hi\n")
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter("always")
                with redirect_stdout(io.StringIO()):
                    cli.main([path])
        self.assertEqual(len(caught), 1)
        self.assertIs(caught[0].category, DeprecationWarning)


if __name__ == "__main__":
    unittest.main()
