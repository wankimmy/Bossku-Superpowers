import os
import sys
import unittest
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from render import render_message
from history import render_history


class RenderTests(unittest.TestCase):
    def test_render_message_basic(self):
        ts = datetime(2024, 1, 1, 9, 30)
        line = render_message("alice", "hello there", ts)
        self.assertTrue(line.startswith("[09:30] alice"))
        self.assertIn("hello there", line)

    def test_render_history_joins_lines(self):
        ts = datetime(2024, 1, 1, 9, 30)
        messages = [
            {"author": "alice", "text": "hi", "timestamp": ts},
            {"author": "bob", "text": "yo", "timestamp": ts},
        ]
        out = render_history(messages)
        self.assertEqual(len(out.splitlines()), 2)

    def test_render_message_without_timestamp(self):
        ts = datetime(2024, 1, 1, 9, 30)
        line = render_message("alice", "hi", ts, show_timestamp=False)
        self.assertFalse(line.startswith("["))
        self.assertTrue(line.startswith("alice"))

    def test_render_history_empty_list(self):
        self.assertEqual(render_history([]), "")

    def test_render_message_truncates_long_text(self):
        ts = datetime(2024, 1, 1, 9, 30)
        line = render_message("alice", "x" * 100, ts, width=50)
        self.assertEqual(len(line), 50)
        self.assertTrue(line.endswith("..."))


if __name__ == "__main__":
    unittest.main()
