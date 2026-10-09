"""`bossku install` and `bossku update` take --[no-]claude/--[no-]agents/--[no-]harness; `hooks install` wires the harness.

Every test uses a temporary home; none touches the real one.
"""

import contextlib
import io
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from bossku import __version__
from bossku.cli import main
from bossku.doctor import format_doctor_success, gather_doctor_issues
from bossku.hooks import HARNESS_MARKER
from bossku.install import AGENT_FILES, claude_agents_dir
from bossku.paths import claude_skills_dir, user_config_dir
from bossku.skills import PROFILES

ROOT = Path(__file__).resolve().parents[1]
NODE = unittest.skipUnless(shutil.which("node"), "the harness hooks need node on PATH")


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class CliCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.home = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def run_cli(self, *argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = main(["--home", str(self.home), "--root", str(ROOT), *argv])
        return code, out.getvalue()

    def config(self) -> dict:
        return read_json(user_config_dir(self.home) / "config.json")

    def settings(self) -> dict:
        return read_json(self.home / ".claude" / "settings.json")

    def gates(self) -> dict:
        """What is in settings.json: harness events, and whether the Python verify-gate is also there."""
        hooks = self.settings().get("hooks", {})
        harness = sorted(event for event, entries in hooks.items() if HARNESS_MARKER in json.dumps(entries))
        return {"harness": harness, "verify_gate": "verify-gate" in json.dumps(hooks.get("Stop", []))}

    def managed_in(self, folder: Path) -> list:
        return sorted(p.name for p in folder.iterdir() if p.is_dir()) if folder.is_dir() else []

    def hooks_line(self) -> str:
        lines = format_doctor_success(ROOT, self.home, version=__version__)
        return next(line for line in lines if line.startswith("  claude_code hooks:"))


class ChoiceFlagTests(CliCase):
    def test_no_claude_turns_the_claude_copies_off_and_a_plain_install_keeps_it(self):
        self.assertEqual(self.run_cli("install", "--profile", "core")[0], 0)
        self.assertTrue(self.managed_in(claude_skills_dir(self.home)))
        self.assertEqual(self.run_cli("install", "--no-claude")[0], 0)
        self.assertIs(self.config()["claude_skills"], False)
        self.assertEqual(self.managed_in(claude_skills_dir(self.home)), [])
        self.assertEqual(self.run_cli("install")[0], 0)
        self.assertIs(self.config()["claude_skills"], False)
        self.assertEqual(self.managed_in(claude_skills_dir(self.home)), [])
        self.assertEqual(self.run_cli("install", "--claude")[0], 0)
        self.assertIs(self.config()["claude_skills"], True)
        self.assertTrue(self.managed_in(claude_skills_dir(self.home)))

    def test_no_agents_removes_the_contracts_and_a_plain_install_keeps_it(self):
        self.run_cli("install", "--profile", "core")
        self.assertEqual(self.managed_in(claude_agents_dir(self.home)), [])        # files, not folders
        self.assertEqual(len(list(claude_agents_dir(self.home).glob("*.md"))), len(AGENT_FILES))
        self.assertEqual(self.run_cli("install", "--no-agents")[0], 0)
        self.assertIs(self.config()["agents"], False)
        self.assertEqual(list(claude_agents_dir(self.home).glob("*.md")), [])
        self.run_cli("install")
        self.assertEqual(list(claude_agents_dir(self.home).glob("*.md")), [])
        self.run_cli("install", "--agents")
        self.assertEqual(len(list(claude_agents_dir(self.home).glob("*.md"))), len(AGENT_FILES))

    @NODE
    def test_no_harness_leaves_the_node_gates_out_and_the_python_stop_gate_takes_over(self):
        self.run_cli("install", "--profile", "core")
        self.assertEqual(self.gates(), {"harness": ["PostToolUse", "PreToolUse", "SessionStart", "Stop"], "verify_gate": False})
        self.assertEqual(self.run_cli("install", "--no-harness")[0], 0)
        self.assertIs(self.config()["harness"], False)
        self.assertEqual(self.gates(), {"harness": [], "verify_gate": True})
        self.assertNotIn("deny", self.settings().get("permissions", {}))
        self.run_cli("install")                                               # a plain install keeps the choice
        self.assertEqual(self.gates(), {"harness": [], "verify_gate": True})
        self.assertEqual(self.run_cli("install", "--harness")[0], 0)
        self.assertIs(self.config()["harness"], True)
        self.assertEqual(self.gates(), {"harness": ["PostToolUse", "PreToolUse", "SessionStart", "Stop"], "verify_gate": False})

    @NODE
    def test_update_takes_the_same_flags_and_otherwise_keeps_the_saved_choices_and_profile(self):
        self.run_cli("install", "--profile", "core", "--no-agents")
        self.assertEqual(self.run_cli("update", "--no-harness")[0], 0)
        config = self.config()
        self.assertEqual((config["profile"], config["agents"], config["harness"]), ("core", False, False))
        self.assertEqual(self.gates()["harness"], [])
        self.assertEqual(self.run_cli("update")[0], 0)
        self.assertIs(self.config()["harness"], False)
        self.assertEqual(self.gates()["harness"], [])
        self.assertEqual(self.run_cli("update", "--harness", "--agents")[0], 0)
        config = self.config()
        self.assertEqual((config["profile"], config["agents"], config["harness"]), ("core", True, True))
        self.assertEqual(len(list(claude_agents_dir(self.home).glob("*.md"))), len(AGENT_FILES))

    def test_only_the_flags_that_were_given_reach_install_user(self):
        with mock.patch("bossku.cli.install_user", return_value={"hooks": {}}) as install:
            self.run_cli("install", "--no-claude", "--agents")
            self.run_cli("install")
        first, second = install.call_args_list
        self.assertEqual({k: v for k, v in first.kwargs.items() if k in ("claude", "agents", "harness")},
                         {"claude": False, "agents": True})
        self.assertEqual({k for k in second.kwargs if k in ("claude", "agents", "harness")}, set())

    def test_an_update_with_a_flag_uses_the_saved_profile_vault_and_checkout(self):
        user_config_dir(self.home).mkdir(parents=True)
        (user_config_dir(self.home) / "config.json").write_text(json.dumps(
            {"profile": "engineering", "obsidian_vault": "V", "installed_from": str(ROOT)}), encoding="utf-8")
        with mock.patch("bossku.cli.install_user", return_value={"hooks": {}}) as install, \
                mock.patch("bossku.cli.update_user", return_value={"hooks": {}}) as plain, \
                contextlib.redirect_stdout(io.StringIO()):
            main(["--home", str(self.home), "update", "--no-harness"])
            self.assertEqual(install.call_args.kwargs, {"root": ROOT, "home": self.home, "profile": "engineering",
                                                       "vault": "V", "harness": False})
            plain.assert_not_called()
            main(["--home", str(self.home), "update"])
            plain.assert_called_once()


class ProfileTests(CliCase):
    def test_every_profile_the_library_knows_is_accepted_and_kept(self):
        self.assertIn("engineering", PROFILES)
        self.assertEqual(self.run_cli("install", "--profile", "engineering")[0], 0)
        self.assertEqual(self.config()["profile"], "engineering")
        self.assertEqual(self.run_cli("install")[0], 0)                       # a plain install keeps it, not "lean"
        self.assertEqual(self.config()["profile"], "engineering")

    def test_an_unknown_profile_is_refused(self):
        with contextlib.redirect_stderr(io.StringIO()) as err, self.assertRaises(SystemExit) as stop:
            self.run_cli("install", "--profile", "bogus")
        self.assertEqual(stop.exception.code, 2)
        for name in PROFILES:
            self.assertIn(name, err.getvalue())

    def test_init_and_skills_find_take_the_same_profiles(self):
        project = self.home / "proj"
        self.assertEqual(self.run_cli("init", str(project), "--profile", "engineering")[0], 0)
        code, out = self.run_cli("skills", "find", "audit my seo", "--profile", "engineering")
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out)["profile"], "engineering")


@NODE
class HooksInstallTests(CliCase):
    def setUp(self):
        super().setUp()
        (self.home / ".claude").mkdir()

    def test_hooks_install_wires_the_harness_and_never_a_second_stop_gate(self):
        code, out = self.run_cli("hooks", "install")
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out)["claude_harness"]["status"], "installed")
        self.assertEqual(self.gates(), {"harness": ["PostToolUse", "PreToolUse", "SessionStart", "Stop"], "verify_gate": False})
        self.assertIn("Bash(git reset --hard:*)", self.settings()["permissions"]["deny"])
        self.assertEqual(self.run_cli("hooks", "install")[0], 0)              # again: still one Stop gate
        self.assertEqual(self.gates()["verify_gate"], False)
        self.assertEqual(json.dumps(self.settings()["hooks"]["Stop"]).count(HARNESS_MARKER), 1)
        self.assertEqual(self.run_cli("hooks", "uninstall")[0], 0)
        self.assertEqual(self.settings().get("hooks", {}), {})
        self.assertNotIn("permissions", self.settings())

    def test_the_saved_no_harness_choice_is_kept(self):
        user_config_dir(self.home).mkdir(parents=True)
        (user_config_dir(self.home) / "config.json").write_text(json.dumps({"harness": False}), encoding="utf-8")
        code, out = self.run_cli("hooks", "install")
        self.assertEqual(code, 0)
        self.assertNotIn("claude_harness", json.loads(out))
        self.assertEqual(self.gates(), {"harness": [], "verify_gate": True})

    def test_without_a_checkout_nothing_is_guessed_and_the_python_gate_stays(self):
        with mock.patch("bossku.cli.repo_root", side_effect=FileNotFoundError("no checkout")):
            code, out = self.run_cli("hooks", "install")
        self.assertEqual(code, 0)
        self.assertNotIn("claude_harness", json.loads(out))
        self.assertEqual(self.gates(), {"harness": [], "verify_gate": True})

    def test_only_the_tools_asked_for_are_touched(self):
        code, out = self.run_cli("hooks", "install", "--tools", "cursor")
        self.assertEqual(code, 0)
        self.assertNotIn("claude_harness", json.loads(out))
        self.assertFalse((self.home / ".claude" / "settings.json").exists())


class DoctorHooksLineTests(CliCase):
    @NODE
    def test_the_verify_gate_is_not_called_missing_while_the_node_stop_gate_does_its_job(self):
        self.run_cli("install", "--profile", "core")
        line = self.hooks_line()
        self.assertEqual(line, "  claude_code hooks: sync (Stop), sync (SessionEnd), skill-hint, session-brief")
        self.assertEqual(gather_doctor_issues(ROOT, self.home), [])

    def test_with_the_harness_off_the_verify_gate_is_listed_as_installed_or_as_missing(self):
        self.run_cli("install", "--profile", "core", "--no-harness")
        self.assertIn("verify-gate", self.hooks_line())
        self.assertNotIn("not installed", self.hooks_line())
        path = self.home / ".claude" / "settings.json"
        data = read_json(path)
        data["hooks"]["Stop"] = [e for e in data["hooks"]["Stop"] if "verify-gate" not in json.dumps(e)]
        path.write_text(json.dumps(data), encoding="utf-8")
        self.assertTrue(self.hooks_line().endswith("(not installed: verify-gate)"), self.hooks_line())


if __name__ == "__main__":
    unittest.main()
