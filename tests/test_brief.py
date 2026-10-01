import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from bossku.brief import memory_brief, session_output
from bossku.cli import main
from bossku.hooks import install_hooks, uninstall_hooks
from bossku.init_project import init_project
from bossku.memory import remember

ROOT = Path(__file__).resolve().parents[1]


class MemoryBriefTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.home = Path(self.tmp.name) / "home"
        self.home.mkdir()
        self.project = Path(self.tmp.name) / "app"
        init_project(self.project, root=ROOT, home=self.home)

    def tearDown(self):
        self.tmp.cleanup()

    def test_a_fresh_project_has_nothing_to_say(self):
        self.assertEqual(memory_brief(self.project, home=self.home), "")

    def test_newest_entries_come_first_and_each_is_labelled(self):
        remember(self.project, "decision", "Use SQLite for the cache.", home=self.home)
        remember(self.project, "learning", "The export job fails when the file name has a colon.", home=self.home)
        brief = memory_brief(self.project, home=self.home)
        self.assertIn("[decision", brief)
        self.assertIn("Use SQLite for the cache.", brief)
        self.assertIn("[learning", brief)
        self.assertNotIn("Durable decisions only.", brief)
        self.assertIn("do not read the memory files again", brief)

    def test_the_budget_is_respected_and_long_notes_are_clipped(self):
        for index in range(30):
            remember(self.project, "decision", f"Decision number {index}: " + "reason " * 80, home=self.home)
        brief = memory_brief(self.project, home=self.home, limit=700)
        self.assertLessEqual(len(brief), 700 + 140)
        self.assertIn("...", brief)

    def test_no_vault_or_missing_folder_stays_quiet(self):
        (self.home / ".bosskuai").mkdir(parents=True, exist_ok=True)
        (self.home / ".bosskuai" / "config.json").write_text(
            json.dumps({"memory_storage": "obsidian", "obsidian_vault": str(Path(self.tmp.name) / "missing")}), encoding="utf-8")
        self.assertEqual(memory_brief(self.project, home=self.home), "")

    def test_session_hook_output_has_the_shape_claude_code_expects(self):
        remember(self.project, "plan", "Ship the importer next.", home=self.home)
        out = session_output(json.dumps({"cwd": str(self.project)}), home=self.home)
        self.assertEqual(out["hookSpecificOutput"]["hookEventName"], "SessionStart")
        self.assertIn("Ship the importer next.", out["hookSpecificOutput"]["additionalContext"])
        self.assertEqual(session_output("", home=self.home), {})
        self.assertEqual(session_output("not json", home=self.home), {})
        self.assertEqual(session_output(json.dumps({"cwd": str(Path(self.tmp.name) / "empty")}), home=self.home), {})

    def test_cli_prints_the_brief_or_says_there_is_none(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            main(["--home", str(self.home), "memory-brief", "--project", str(self.project)])
        self.assertIn("No project notes yet.", out.getvalue())
        remember(self.project, "learning", "Retries need jitter.", home=self.home)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            main(["--home", str(self.home), "memory-brief", "--project", str(self.project)])
        self.assertIn("Retries need jitter.", out.getvalue())

    def test_session_hook_is_installed_and_removed_with_the_others(self):
        (self.home / ".claude").mkdir()
        result = install_hooks(home=self.home, tools=("claude_code",))["claude_code"]
        self.assertIn("session-brief", result["added"])
        settings = json.loads((self.home / ".claude" / "settings.json").read_text(encoding="utf-8"))
        self.assertIn("session-brief", json.dumps(settings["hooks"]["SessionStart"]))
        uninstall_hooks(home=self.home, tools=("claude_code",))
        settings = json.loads((self.home / ".claude" / "settings.json").read_text(encoding="utf-8"))
        self.assertNotIn("SessionStart", settings["hooks"])


if __name__ == "__main__":
    unittest.main()
