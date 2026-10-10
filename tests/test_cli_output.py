"""Commands that report a result print JSON for scripts and agents, and a short summary on a terminal.

Not a terminal (a pipe, an agent, a test) or `--json`: exactly the JSON the command printed before. A terminal: plain
words, the one next step, no colour. Every test uses a temporary home; none touches the real one or a real vault.
"""

import contextlib
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from bossku import cli
from bossku import vault as vault_module
from bossku.cli import main
from bossku.paths import user_config_dir

ROOT = Path(__file__).resolve().parents[1]


class Terminal(io.StringIO):
    def isatty(self):   # what sys.stdout.isatty() says in front of a person
        return True


class OutputCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.home = Path(self.tmp.name) / "home"
        self.home.mkdir()
        self.project = Path(self.tmp.name) / "project"
        self.addCleanup(self.tmp.cleanup)

    def run_cli(self, *argv, tty=False, spy=None):
        """(exit code, stdout, what `spy` returned). `spy` is a name in bossku.cli, or (module, name): its result is recorded."""
        out = Terminal() if tty else io.StringIO()
        seen = []
        owner, name = spy if isinstance(spy, tuple) else (cli, spy)
        real = getattr(owner, name) if spy else None

        def recorded(*a, **k):
            seen.append(real(*a, **k))
            return seen[-1]

        with contextlib.ExitStack() as stack, contextlib.redirect_stdout(out):
            if spy:
                stack.enter_context(mock.patch.object(owner, name, recorded))
            code = main(["--home", str(self.home), "--root", str(ROOT), *argv])
        return code, out.getvalue(), (seen[0] if seen else None)

    def set_vault(self) -> Path:
        vault = Path(self.tmp.name) / "vault"
        vault.mkdir()
        user_config_dir(self.home).mkdir(parents=True, exist_ok=True)
        (user_config_dir(self.home) / "config.json").write_text(json.dumps({"obsidian_vault": str(vault)}), encoding="utf-8")
        return vault

    def assertPlainSummary(self, text, *needles):
        self.assertFalse(text.lstrip().startswith(("{", "[")), text)
        self.assertNotIn("\x1b", text)
        self.assertNotIn(chr(0x2014), text)   # no em dash
        for needle in needles:
            self.assertIn(needle, text)

    def assertJsonLikeBefore(self, text, result):
        """Byte for byte what the command printed before this change: json.dumps(result, indent=2) and a newline."""
        self.assertEqual(text, json.dumps(result, indent=2) + "\n")
        self.assertEqual(json.loads(text), json.loads(json.dumps(result)))


class InstallAndUpdateTests(OutputCase):
    def test_install_is_the_same_json_when_stdout_is_not_a_terminal(self):
        code, text, result = self.run_cli("install", "--profile", "core", spy="install_user")
        self.assertEqual(code, 0)
        self.assertJsonLikeBefore(text, result)
        self.assertIn("hooks", json.loads(text))

    def test_install_on_a_terminal_says_what_changed_and_the_one_next_step(self):
        code, text, _ = self.run_cli("install", "--profile", "core", tty=True)
        self.assertEqual(code, 0)
        self.assertPlainSummary(text, "Bossku is installed (skill profile: core).", "Skills: ", "Subagents: 6 contracts",
                                "Hooks:", "Claude Code: set up", "Next: cd your-project && bossku init .")
        self.assertEqual(text.count("Next:"), 1)

    def test_install_on_a_terminal_names_what_was_skipped_and_why(self):
        _, text, _ = self.run_cli("install", "--profile", "core", "--no-claude", "--no-agents", tty=True)
        self.assertPlainSummary(text, "Skills in ~/.claude/skills: left out (--no-claude)", "Cursor: skipped, nothing found at")
        self.assertNotIn("Subagents: 6", text)

    def test_json_flag_forces_the_json_on_a_terminal(self):
        code, text, result = self.run_cli("install", "--profile", "core", "--json", tty=True, spy="install_user")
        self.assertEqual(code, 0)
        self.assertJsonLikeBefore(text, result)

    def test_a_failed_hook_still_exits_1_and_the_summary_points_at_the_fix(self):
        broken = {"cursor": {"status": "error", "message": "disk full"}}
        with mock.patch.object(cli, "install_hooks", return_value=broken):
            code, text, _ = self.run_cli("hooks", "install", tty=True)
            code_json, text_json, _ = self.run_cli("hooks", "install")
        self.assertEqual((code, code_json), (1, 1))
        self.assertPlainSummary(text, "Cursor: error (disk full)", "Next: fix the error above, then run `bossku hooks install`")
        self.assertEqual(json.loads(text_json), broken)

    def test_a_failed_hook_removal_does_not_tell_you_to_install_the_hooks_again(self):
        broken = {"cursor": {"status": "error", "message": "locked"}}
        with mock.patch.object(cli, "uninstall_hooks", return_value=broken):
            code, text, _ = self.run_cli("hooks", "uninstall", tty=True)
            code_json, text_json, _ = self.run_cli("hooks", "uninstall")
        self.assertEqual((code, code_json), (1, 1))
        self.assertPlainSummary(text, "Cursor: error (locked)", "Next: fix the error above, then run `bossku hooks uninstall` again.")
        self.assertNotIn("bossku hooks install", text)
        self.assertEqual(json.loads(text_json), broken)

    def test_update_is_json_when_piped_and_a_summary_on_a_terminal(self):
        self.run_cli("install", "--profile", "core")
        code, text, result = self.run_cli("update", spy="update_user")
        self.assertEqual(code, 0)
        self.assertJsonLikeBefore(text, result)
        _, human, _ = self.run_cli("update", tty=True)
        self.assertPlainSummary(human, "Bossku is updated (skill profile: core).", "Claude Code: already set up", "Next: bossku doctor")
        _, forced, result = self.run_cli("update", "--json", tty=True, spy="update_user")
        self.assertJsonLikeBefore(forced, result)

    def test_update_with_a_choice_flag_is_summarised_too(self):
        self.run_cli("install", "--profile", "core")
        code, human, _ = self.run_cli("update", "--no-agents", tty=True)
        self.assertEqual(code, 0)
        self.assertPlainSummary(human, "Bossku is updated", "Subagents: 6 removed (--no-agents).")


class InitTests(OutputCase):
    def test_init_is_the_same_json_when_stdout_is_not_a_terminal(self):
        code, text, result = self.run_cli("init", str(self.project), spy="init_project")
        self.assertEqual(code, 0)
        self.assertJsonLikeBefore(text, result)
        self.assertEqual(set(json.loads(text)), {"project", "meta", "memory", "design_md", "omp", "portable_skills"})

    def test_init_on_a_terminal_names_the_files_and_the_next_step(self):
        code, text, _ = self.run_cli("init", str(self.project), tty=True)
        self.assertEqual(code, 0)
        self.assertPlainSummary(text, "AGENTS.md has the Bossku block", ".bossku/DESIGN.md: created",
                                f'Next: bossku doctor --project "{self.project.resolve()}"')
        _, again, _ = self.run_cli("init", str(self.project), tty=True)
        self.assertIn("DESIGN.md: already there, left alone.", again)

    def test_init_in_the_current_folder_suggests_a_dot(self):
        self.project.mkdir()
        with mock.patch.object(Path, "cwd", return_value=self.project.resolve()):
            _, text, _ = self.run_cli("init", str(self.project), tty=True)
        self.assertEqual(text.splitlines()[-1], "Next: bossku doctor --project .")

    def test_a_summary_that_cannot_be_built_falls_back_to_the_json_and_keeps_exit_0(self):
        with mock.patch.object(cli, "_init_summary", side_effect=KeyError("memory")):
            code, text, result = self.run_cli("init", str(self.project), tty=True, spy="init_project")
        self.assertEqual(code, 0)
        self.assertJsonLikeBefore(text, result)

    def test_init_json_flag_forces_json_on_a_terminal(self):
        _, text, result = self.run_cli("init", str(self.project), "--json", tty=True, spy="init_project")
        self.assertJsonLikeBefore(text, result)

    def test_init_in_a_real_pipe_prints_json(self):
        done = subprocess.run([sys.executable, "-m", "bossku", "--home", str(self.home), "--root", str(ROOT),
                               "init", str(self.project)], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(json.loads(done.stdout)["project"], str(self.project.resolve()))


class MemoryTests(OutputCase):
    def test_remember_is_the_same_json_when_stdout_is_not_a_terminal(self):
        code, text, result = self.run_cli("remember", "--project", str(self.project), "--kind", "decision", "Keep it.", spy="remember")
        self.assertEqual(code, 0)
        self.assertJsonLikeBefore(text, result)
        self.assertTrue(json.loads(text)["saved"])

    def test_remember_on_a_terminal_prints_the_saved_message(self):
        _, text, _ = self.run_cli("remember", "--project", str(self.project), "--kind", "learning", "Keep it.", tty=True)
        self.assertPlainSummary(text, "Saved the learning note to ", "Nothing more to do.")
        self.assertEqual(len(text.splitlines()), 1)

    def test_remember_json_flag_forces_json_on_a_terminal(self):
        _, text, result = self.run_cli("remember", "--project", str(self.project), "--kind", "plan", "Later.", "--json",
                                       tty=True, spy="remember")
        self.assertJsonLikeBefore(text, result)

    def test_sync_without_a_vault_says_why_and_how_to_add_one(self):
        code, text, result = self.run_cli("sync", "--project", str(self.project), spy="sync_project")
        self.assertEqual((code, json.loads(text)), (0, {"status": "skipped", "reason": "no vault configured"}))
        self.assertJsonLikeBefore(text, result)
        _, human, _ = self.run_cli("sync", "--project", str(self.project), tty=True)
        self.assertPlainSummary(human, "Nothing was copied to the vault: no vault configured.", "Next: bossku install --vault")

    def test_sync_with_a_vault_counts_the_copied_notes(self):
        vault = self.set_vault()
        self.run_cli("remember", "--project", str(self.project), "--kind", "decision", "Keep it.")
        _, human, _ = self.run_cli("sync", "--project", str(self.project), tty=True)
        self.assertPlainSummary(human, "1 note file(s) are in the vault at ", str(vault))
        _, text, result = self.run_cli("sync", "--project", str(self.project), "--json", tty=True, spy="sync_project")
        self.assertJsonLikeBefore(text, result)

    def test_sync_does_not_say_copied_when_every_file_was_already_the_same(self):
        self.set_vault()
        self.run_cli("remember", "--project", str(self.project), "--kind", "decision", "Keep it.")
        self.run_cli("sync", "--project", str(self.project))
        _, again, result = self.run_cli("sync", "--project", str(self.project), tty=True, spy="sync_project")
        self.assertEqual(result["exported"], ["decisions.md"])   # sync_project lists unchanged files as exported too
        self.assertPlainSummary(again, "1 note file(s) are in the vault at ")
        self.assertNotIn("Copied", again)

    def test_sync_in_obsidian_storage_shows_a_failed_mirror_instead_of_hiding_it(self):
        vault = self.set_vault()
        config = user_config_dir(self.home) / "config.json"
        config.write_text(json.dumps({"obsidian_vault": str(vault), "memory_storage": "obsidian"}), encoding="utf-8")
        with mock.patch.object(vault_module, "sync", side_effect=OSError("disk full")):
            code, human, _ = self.run_cli("sync", "--project", str(self.project), tty=True)
            _, text, result = self.run_cli("sync", "--project", str(self.project), spy="sync_project")
        self.assertEqual(code, 0)
        self.assertPlainSummary(human, "Your notes are kept in the vault already: ",
                                "Mirroring auto-memory and rules to the vault failed: disk full")
        self.assertEqual(result["mirrored"], {"status": "error", "reason": "disk full"})
        self.assertJsonLikeBefore(text, result)

    def test_vault_sync_is_json_when_piped_and_a_summary_on_a_terminal(self):
        _, text, result = self.run_cli("vault", "sync", "--project", str(self.project), spy=(vault_module, "sync"))
        self.assertEqual(json.loads(text), {"status": "skipped", "reason": "no vault configured or vault unavailable"})
        self.assertJsonLikeBefore(text, result)
        _, human, _ = self.run_cli("vault", "sync", "--project", str(self.project), tty=True)
        self.assertPlainSummary(human, "Nothing was copied to the vault: no vault configured or vault unavailable.")
        (self.set_vault() / "BosskuAI").mkdir()
        _, human, _ = self.run_cli("vault", "sync", "--project", str(self.project), tty=True)
        self.assertPlainSummary(human, "Updated 1 file(s) in the vault: Index.md")
        _, text, result = self.run_cli("vault", "sync", "--project", str(self.project), spy=(vault_module, "sync"))
        self.assertEqual(result["status"], "ok")
        self.assertJsonLikeBefore(text, result)
        _, human, _ = self.run_cli("vault", "sync", "--project", str(self.project), tty=True)
        self.assertPlainSummary(human, "The vault is already up to date.")
        _, forced, result = self.run_cli("vault", "sync", "--project", str(self.project), "--json", tty=True,
                                         spy=(vault_module, "sync"))
        self.assertJsonLikeBefore(forced, result)

    def test_vault_tidy_apply_ends_with_a_summary_on_a_terminal_and_the_json_otherwise(self):
        vault = self.set_vault()
        (vault / "BosskuAI" / "old-empty-project").mkdir(parents=True)
        _, preview, _ = self.run_cli("vault", "tidy", tty=True)
        self.assertIn("remove-empty-folder", preview)
        self.assertIn("Nothing was changed. Run again with --apply", preview)
        _, human, _ = self.run_cli("vault", "tidy", "--apply", tty=True)
        self.assertIn("remove-empty-folder", human)
        self.assertIn("Tidy finished (ok): 1 remove-empty-folder.", human)
        self.assertIn("A zip backup of the vault is at ", human)
        self.assertNotIn('"status"', human)
        (vault / "BosskuAI" / "old-empty-project").mkdir(parents=True)
        _, text, _ = self.run_cli("vault", "tidy", "--apply")
        tail = text[text.index("{"):]
        self.assertEqual(json.loads(tail)["status"], "ok")
        self.assertEqual(tail, json.dumps(json.loads(tail), indent=2) + "\n")
        (vault / "BosskuAI" / "old-empty-project").mkdir(parents=True)
        _, forced, _ = self.run_cli("vault", "tidy", "--apply", "--json", tty=True)
        self.assertEqual(json.loads(forced[forced.index("{"):])["done"]["remove-empty-folder"], 1)


class HooksAndUninstallTests(OutputCase):
    def setUp(self):
        super().setUp()
        (self.home / ".claude").mkdir()   # `hooks install` only wires a tool whose folder exists

    def test_hooks_when_no_tool_is_found_say_nothing_changed(self):
        (self.home / ".claude").rmdir()
        _, text, _ = self.run_cli("hooks", "install", tty=True)
        self.assertPlainSummary(text, "Claude Code: skipped, nothing found at ", "Nothing was changed: none of these tools was found.")
        self.assertNotIn("Next:", text)

    def test_hooks_install_and_uninstall_are_the_same_json_when_stdout_is_not_a_terminal(self):
        _, text, result = self.run_cli("hooks", "install", spy="install_hooks")
        self.assertJsonLikeBefore(text, result)
        _, text, result = self.run_cli("hooks", "uninstall", spy="uninstall_hooks")
        self.assertJsonLikeBefore(text, result)
        self.assertEqual(json.loads(text)["claude_code"]["status"], "removed")

    def test_hooks_on_a_terminal_list_each_tool_and_the_next_step(self):
        _, text, _ = self.run_cli("hooks", "install", tty=True)
        self.assertPlainSummary(text, "Hooks:", "Claude Code: set up", "Next: bossku doctor")
        _, text, _ = self.run_cli("hooks", "uninstall", tty=True)
        self.assertPlainSummary(text, "Claude Code: removed", "Next: put them back any time with `bossku hooks install`.")
        _, text, _ = self.run_cli("hooks", "uninstall", "--tools", "claude_code", tty=True)
        self.assertIn("Claude Code: was not set up, nothing to remove", text)

    def test_hooks_json_flag_forces_json_on_a_terminal(self):
        _, text, result = self.run_cli("hooks", "install", "--json", tty=True, spy="install_hooks")
        self.assertJsonLikeBefore(text, result)

    def test_uninstall_is_the_same_json_when_stdout_is_not_a_terminal(self):
        self.run_cli("install", "--profile", "core")
        code, text, result = self.run_cli("uninstall", spy="uninstall_user")
        self.assertEqual(code, 0)
        self.assertJsonLikeBefore(text, result)

    def test_uninstall_on_a_terminal_points_at_purge_and_purge_says_what_it_removed(self):
        self.run_cli("install", "--profile", "core")
        _, text, _ = self.run_cli("uninstall", tty=True)
        self.assertPlainSummary(text, "subagent contracts.", "The hooks and the config are still in place.",
                                "Next: bossku uninstall --purge")
        self.run_cli("install", "--profile", "core")
        _, text, _ = self.run_cli("uninstall", "--purge", tty=True)
        self.assertPlainSummary(text, "Also removed the Bossku config and hooks", "Claude Code: removed",
                                "Your projects and their notes were not touched.")
        self.assertNotIn("Next:", text)

    def test_uninstall_json_flag_forces_json_on_a_terminal(self):
        _, text, result = self.run_cli("uninstall", "--purge", "--json", tty=True, spy="uninstall_user")
        self.assertJsonLikeBefore(text, result)


class UnchangedCommandTests(OutputCase):
    def test_commands_that_agents_read_stay_json_on_a_terminal(self):
        for argv in (("memory-path", "--project", str(self.project)), ("skills", "find", "write a unit test")):
            with self.subTest(argv=argv):
                _, text, _ = self.run_cli(*argv, tty=True)
                self.assertIsInstance(json.loads(text), dict)

    def test_the_json_flag_is_listed_in_help(self):
        for argv in (["install"], ["init"], ["update"], ["remember"], ["sync"], ["hooks", "install"], ["hooks", "uninstall"],
                     ["vault", "sync"], ["vault", "tidy"], ["uninstall"]):
            with self.subTest(argv=argv):
                with contextlib.redirect_stdout(io.StringIO()) as out, self.assertRaises(SystemExit):
                    main([*argv, "--help"])
                self.assertIn("--json", out.getvalue())

    def test_vault_tidy_help_says_what_json_does_there(self):
        with contextlib.redirect_stdout(io.StringIO()) as out, self.assertRaises(SystemExit):
            main(["vault", "tidy", "--help"])
        text = " ".join(out.getvalue().split())   # argparse wraps long help lines
        self.assertIn("--json", text)
        self.assertIn("with --apply", text)
        self.assertNotIn("always JSON when piped", text)   # without --apply nothing is JSON, piped or not


if __name__ == "__main__":
    unittest.main()
