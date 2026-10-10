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
from bossku.install import AUTO_MEMORY_BLOCK
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

    def test_a_long_rule_is_not_cut_before_its_exact_name(self):
        rule = ("Custom exception classes end in Failure, never Error, because the Error suffix collides with names "
                "our monitoring tool reserves, and the on-call rota greps for it. Every custom exception derives from one base class "
                "PaymentFailure.")
        self.assertGreater(len(rule), 220)
        remember(self.project, "decision", rule, home=self.home)
        brief = memory_brief(self.project, home=self.home)
        self.assertIn("PaymentFailure.", brief)
        remember(self.project, "learning", "Gotcha " + "word " * 80, home=self.home)
        self.assertIn("...", memory_brief(self.project, home=self.home))   # other kinds still clip at 220

    def test_the_intro_says_a_request_with_different_wording_does_not_cancel_a_rule(self):
        remember(self.project, "decision", "Env vars are prefixed OPSX_.", home=self.home)
        brief = memory_brief(self.project, home=self.home)
        self.assertIn("apply to this request even when its own wording differs", brief)
        self.assertIn("explicit instruction to change or drop a rule", brief)
        self.assertNotIn("unless the request says otherwise", brief)

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


class MemoryBlockTests(unittest.TestCase):
    def test_block_asks_for_rules_meant_for_later_work_with_exact_values_first(self):
        flat = " ".join(AUTO_MEMORY_BLOCK.split())
        self.assertIn("exact names and values first", flat)
        self.assertIn("also when it only applies to work you have not done yet", flat)
        self.assertLess(len(AUTO_MEMORY_BLOCK), 1100)   # always-on text: keep it small


if __name__ == "__main__":
    unittest.main()
