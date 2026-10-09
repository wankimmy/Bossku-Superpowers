"""Core-misc fixes: the verify gate ignores edits outside the project, sync never copies a temp-folder project into a
real vault, and `skills find` builds the routing index once.

Every path here lives under a temp folder or is a made-up absolute path. Nothing touches the real home, the real
~/.claude/settings.json or the Obsidian vault. The OS temp folder is faked with a sub-folder so the test can place a
"real" vault next to it.
"""
import contextlib
import io
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import bossku.index
from bossku.cli import main
from bossku.gate import _outside_project, gate_output, needs_verification
from bossku.memory import init_memory_templates, memory_directory, remember, save_user_config, sync_project

ROOT = Path(__file__).resolve().parents[1]
ANCHOR = Path(Path.cwd().anchor)   # "C:\" or "/": a made-up absolute path under it is never in the temp folder


def call(name, **args):
    return json.dumps({"type": "assistant", "message": {"content": [{"type": "tool_use", "name": name, "input": args}]}})


class OutsideProjectEditTests(unittest.TestCase):
    """Editing a file under ~/.claude or the OS temp folder is not a source edit, so it needs no test run."""

    def setUp(self):
        self.home = ANCHOR / "someone"
        patcher = mock.patch.object(Path, "home", return_value=self.home)
        patcher.start()
        self.addCleanup(patcher.stop)

    def edit(self, path, name="Write"):
        return call(name, file_path=str(path))

    def test_an_edit_under_the_claude_folder_needs_no_run(self):
        for name in ("Write", "Edit", "MultiEdit"):
            self.assertFalse(needs_verification([self.edit(self.home / ".claude" / "hooks" / "guard.py", name)]), name)

    def test_an_edit_in_the_os_temp_folder_needs_no_run(self):
        self.assertFalse(needs_verification([self.edit(Path(tempfile.gettempdir()) / "scratch" / "probe.py")]))

    def test_an_edit_in_the_project_still_needs_a_run(self):
        self.assertTrue(needs_verification([self.edit(self.home / "shop" / "cart.py")]))
        self.assertTrue(needs_verification([call("Write", file_path="cart.py")]))   # relative: assume the project

    def test_a_project_edit_next_to_a_skipped_one_still_counts(self):
        skipped = self.edit(self.home / ".claude" / "hooks" / "guard.py")
        project = self.edit(self.home / "shop" / "cart.py")
        self.assertTrue(needs_verification([skipped, project]))
        self.assertTrue(needs_verification([project, skipped]))   # the skipped edit must not erase the earlier one

    def test_folders_that_only_share_a_prefix_are_not_skipped(self):
        self.assertTrue(needs_verification([self.edit(self.home / ".claude-notes" / "x.py")]))
        self.assertTrue(needs_verification([self.edit(self.home / ".claudex" / "x.py")]))
        self.assertTrue(needs_verification([self.edit(Path(tempfile.gettempdir() + "-other") / "x.py")]))

    @unittest.skipUnless(os.name == "nt", "Windows paths ignore case")
    def test_the_comparison_ignores_case_on_windows(self):
        self.assertFalse(needs_verification([self.edit(str(self.home / ".claude" / "hooks" / "guard.py").upper())]))
        self.assertFalse(needs_verification([self.edit(tempfile.gettempdir().upper() + os.sep + "probe.py")]))

    def test_a_project_that_lives_in_the_temp_folder_is_still_gated(self):
        # benchmark workspaces are temp folders: a session working in one gates every edit in that folder, as the
        # Node gate does (hooks/_lib.mjs isScratch), but being in the temp folder does not open ~/.claude
        project = Path(tempfile.gettempdir()) / "bb" / "run1"
        self.assertTrue(needs_verification([self.edit(project / "app.py")], project=str(project)))
        self.assertTrue(needs_verification([self.edit(Path(tempfile.gettempdir()) / "other" / "x.py")],
                                           project=str(project)))
        self.assertTrue(needs_verification([self.edit(project.with_name("run10") / "x.py")], project=str(project)))
        self.assertFalse(needs_verification([self.edit(self.home / ".claude" / "hooks" / "guard.py")],
                                            project=str(project)))

    def test_a_session_started_in_the_home_folder_still_skips_both_roots(self):
        for target in (self.home / ".claude" / "hooks" / "guard.py", Path(tempfile.gettempdir()) / "probe.py"):
            self.assertFalse(needs_verification([self.edit(target)], project=str(self.home)), str(target))
        self.assertTrue(needs_verification([self.edit(self.home / "shop" / "cart.py")], project=str(self.home)))

    def test_a_session_inside_the_claude_folder_gates_its_own_edits_only(self):
        skills = self.home / ".claude" / "skills"
        self.assertTrue(needs_verification([self.edit(skills / "x" / "run.py")], project=str(skills)))
        self.assertTrue(needs_verification([self.edit(self.home / ".claude" / "hooks" / "guard.py")],
                                           project=str(skills)))
        self.assertFalse(needs_verification([self.edit(Path(tempfile.gettempdir()) / "probe.py")],
                                            project=str(skills)))

    def test_the_stop_hook_skips_a_home_folder_edit_when_the_session_started_in_the_home_folder(self):
        with tempfile.TemporaryDirectory() as tmp, mock.patch.dict(os.environ, {"CLAUDE_PROJECT_DIR": ""}):
            log = Path(tmp) / "t.jsonl"
            log.write_text(self.edit(self.home / ".claude" / "hooks" / "guard.py"), encoding="utf-8")
            self.assertEqual(gate_output(json.dumps({"transcript_path": str(log), "cwd": str(self.home)})), {})

    def test_the_stop_hook_lets_the_turn_end_after_an_out_of_project_edit(self):
        with tempfile.TemporaryDirectory() as tmp, mock.patch.dict(os.environ, {"CLAUDE_PROJECT_DIR": ""}):
            outside = Path(tmp) / "t.jsonl"
            outside.write_text(self.edit(self.home / ".claude" / "hooks" / "guard.py"), encoding="utf-8")
            self.assertEqual(gate_output(json.dumps({"transcript_path": str(outside)})), {})
            inside = Path(tmp) / "u.jsonl"
            inside.write_text(self.edit(self.home / "shop" / "cart.py"), encoding="utf-8")
            self.assertEqual(gate_output(json.dumps({"transcript_path": str(inside)}))["decision"], "block")

    def test_the_stop_hook_finds_the_project_from_cwd_or_the_environment(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "bench"   # inside the temp folder, like a benchmark workspace
            log = Path(tmp) / "t.jsonl"
            log.write_text(self.edit(project / "app.py"), encoding="utf-8")
            payload = {"transcript_path": str(log), "cwd": str(project)}
            with mock.patch.dict(os.environ, {"CLAUDE_PROJECT_DIR": ""}):
                self.assertEqual(gate_output(json.dumps(payload))["decision"], "block")
                self.assertEqual(gate_output(json.dumps({**payload, "cwd": str(ANCHOR / "elsewhere")})), {})
            with mock.patch.dict(os.environ, {"CLAUDE_PROJECT_DIR": str(project)}):
                self.assertEqual(gate_output(json.dumps({**payload, "cwd": ""}))["decision"], "block")


class GatesAgreeTests(unittest.TestCase):
    """The Python verify gate and the Node stop gate must give one verdict on one edit. Both rules run on the same
    cases, with the home and the temp folder faked as sub-folders of a temp dir. A case table, so a change to one
    rule that is not made to the other fails here."""

    @staticmethod
    def cases(home, ostemp):
        """(label, session folder or "", edited file, skipped as scratch?)"""
        return [
            ("A  session in the home folder, edit in ~/.claude", home, home / ".claude" / "hooks" / "x.py", True),
            ("A2 session in the home folder, edit in the temp folder", home, ostemp / "x.py", True),
            ("B  session in a temp workspace, edit in another temp folder", ostemp / "bb" / "run1",
             ostemp / "other" / "x.py", False),
            ("B2 session in a temp workspace, edit in it", ostemp / "bb" / "run1", ostemp / "bb" / "run1" / "app.py",
             False),
            ("B3 session in a temp workspace, edit in a sibling with the same prefix", ostemp / "bb" / "run1",
             ostemp / "bb" / "run10" / "x.py", False),
            ("C  session in a repo, edit in ~/.claude", home / "repo", home / ".claude" / "x.py", True),
            ("C2 session in a repo, edit in the temp folder", home / "repo", ostemp / "x.py", True),
            ("D  session in ~/.claude/skills, edit in ~/.claude/hooks", home / ".claude" / "skills",
             home / ".claude" / "hooks" / "x.py", False),
            ("E  no session folder, edit in ~/.claude", "", home / ".claude" / "x.py", True),
            ("E2 no session folder, edit in the temp folder", "", ostemp / "x.py", True),
            ("F  session in a temp workspace does not open ~/.claude", ostemp / "bb" / "run1",
             home / ".claude" / "x.py", True),
            ("G  session in ~/.claude does not open the temp folder", home / ".claude" / "skills",
             ostemp / "x.py", True),
            ("H  edit inside the session's repo", home / "repo", home / "repo" / "src" / "a.py", False),
            ("I  a look-alike of ~/.claude", home / "repo", home / ".claudex" / "x.py", False),
            ("J  a relative path is a project edit", home / "repo", Path("src") / "a.py", False),
        ]

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        base = Path(self.tmp.name).resolve()
        self.home, self.ostemp = base / "home", base / "ostemp"
        for folder in (self.home, self.ostemp):
            folder.mkdir()

    def test_the_python_rule_matches_the_table(self):
        with mock.patch.object(Path, "home", return_value=self.home), \
                mock.patch("tempfile.gettempdir", return_value=str(self.ostemp)):
            for label, cwd, file, skipped in self.cases(self.home, self.ostemp):
                self.assertEqual(_outside_project(str(file), str(cwd)), skipped, label)

    @unittest.skipUnless(shutil.which("node"), "node is not installed")
    def test_the_node_rule_gives_the_same_verdicts(self):
        cases = self.cases(self.home, self.ostemp)
        script = (f'import {{ isScratch }} from "{(ROOT / "hooks" / "_lib.mjs").as_uri()}";'
                  'const cases = JSON.parse(process.env.GATE_CASES);'
                  'console.log(JSON.stringify(cases.map(([cwd, file]) => isScratch(file, cwd || undefined))));')
        env = {**os.environ, "GATE_CASES": json.dumps([[str(cwd), str(file)] for _, cwd, file, _ in cases]),
               "HOME": str(self.home), "USERPROFILE": str(self.home),
               "TEMP": str(self.ostemp), "TMP": str(self.ostemp), "TMPDIR": str(self.ostemp)}
        done = subprocess.run(["node", "--input-type=module", "-e", script], capture_output=True, text=True,
                              encoding="utf-8", env=env, timeout=60)
        self.assertEqual(done.returncode, 0, done.stderr)
        for (label, _, _, skipped), node_says in zip(cases, json.loads(done.stdout)):
            self.assertEqual(node_says, skipped, label)


class TempProjectIsNotSyncedTests(unittest.TestCase):
    """A project inside the OS temp folder is never copied into a vault that lives outside it (test agents left
    about 45 junk folders in the real vault this way). The temp folder is faked as <base>/ostemp."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        base = Path(self.tmp.name).resolve()
        self.ostemp = base / "ostemp"
        self.home = base / "home"
        self.vault = base / "vault"
        for folder in (self.ostemp, self.home, self.vault):
            folder.mkdir()
        save_user_config({"obsidian_vault": str(self.vault)}, self.home)
        patcher = mock.patch("tempfile.gettempdir", return_value=str(self.ostemp))
        patcher.start()
        self.addCleanup(patcher.stop)

    def project_with_notes(self, parent, name="shop"):
        project = parent / name
        notes = project / ".bossku" / "memory"
        notes.mkdir(parents=True)
        (notes / "decisions.md").write_text("# Decisions\n\nKeep it small.\n", encoding="utf-8")
        return project

    def assert_vault_untouched(self, project):
        self.assertEqual(list(self.vault.iterdir()), [])
        self.assertFalse((project / ".bossku" / "memory" / "sync-state.json").exists())

    def test_a_temp_project_is_skipped_before_any_write(self):
        project = self.project_with_notes(self.ostemp)
        result = sync_project(project, home=self.home)
        self.assertEqual(result["status"], "skipped")
        self.assertIn("temp", result["reason"])
        self.assert_vault_untouched(project)

    def test_the_same_holds_when_notes_live_in_the_vault(self):
        save_user_config({"obsidian_vault": str(self.vault), "memory_storage": "obsidian"}, self.home)
        project = self.ostemp / "shop"
        project.mkdir()
        (project / "AGENTS.md").write_text("# Rules\n", encoding="utf-8")   # vault sync would mirror this file
        self.assertEqual(sync_project(project, home=self.home)["status"], "skipped")
        self.assertEqual(list(self.vault.iterdir()), [])

    def test_obsidian_storage_keeps_a_temp_project_out_of_the_vault_on_remember_and_init(self):
        save_user_config({"obsidian_vault": str(self.vault), "memory_storage": "obsidian"}, self.home)
        project = self.ostemp / "shop"
        project.mkdir()
        local = project / ".bossku" / "memory"
        self.assertEqual(memory_directory(project, home=self.home), local)
        init_memory_templates(project, home=self.home)
        result = remember(project, "decision", "Keep it small.", home=self.home)
        self.assertTrue(result["saved"])
        self.assertIn("temp", result["message"])
        self.assertIn("Keep it small.", (local / "decisions.md").read_text(encoding="utf-8"))
        self.assertEqual(list(self.vault.iterdir()), [], "no junk folder in the vault")
        self.assertFalse((self.home / ".bosskuai" / "memory-project-registry").exists(), "no ownership claim either")

    def test_obsidian_storage_still_writes_a_project_outside_the_temp_folder_to_the_vault(self):
        save_user_config({"obsidian_vault": str(self.vault), "memory_storage": "obsidian"}, self.home)
        project = self.home / "work" / "shop"
        project.mkdir(parents=True)
        remember(project, "decision", "Keep it small.", home=self.home)
        self.assertIn("Keep it small.", (self.vault / "BosskuAI" / "shop" / "decisions.md").read_text(encoding="utf-8"))
        self.assertFalse((project / ".bossku" / "memory").exists())

    def test_the_sync_commands_skip_a_temp_project_too(self):
        project = self.project_with_notes(self.ostemp)
        for argv in (["sync", "--project", str(project)], ["sync-hook", "--project", str(project)]):
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                self.assertEqual(main(["--home", str(self.home), *argv]), 0)
            self.assertEqual(json.loads(out.getvalue())["status"], "skipped", argv[0])
        self.assert_vault_untouched(project)

    def test_remember_saves_the_note_and_says_why_there_is_no_vault_copy(self):
        project = self.ostemp / "shop"
        project.mkdir()
        result = remember(project, "decision", "Keep it small.", home=self.home)
        self.assertTrue(result["saved"])
        self.assertIn("Keep it small.", (project / ".bossku" / "memory" / "decisions.md").read_text(encoding="utf-8"))
        self.assertIn("temp", result["message"])
        self.assertNotIn("no vault is configured", result["message"])
        self.assertEqual(list(self.vault.iterdir()), [])

    def test_a_nested_temp_project_is_skipped(self):
        project = self.project_with_notes(self.ostemp / "deep" / "er")
        self.assertEqual(sync_project(project, home=self.home)["status"], "skipped")
        self.assertEqual(list(self.vault.iterdir()), [])

    def test_a_project_outside_the_temp_folder_still_syncs(self):
        project = self.project_with_notes(self.home / "work")
        self.assertEqual(sync_project(project, home=self.home)["status"], "ok")
        self.assertIn("Keep it small.", (self.vault / "BosskuAI" / "shop" / "decisions.md").read_text(encoding="utf-8"))

    def test_a_folder_that_only_shares_the_temp_prefix_still_syncs(self):
        sibling = self.ostemp.with_name("ostemp-keep")
        sibling.mkdir()
        project = self.project_with_notes(sibling)
        self.assertEqual(sync_project(project, home=self.home)["status"], "ok")

    def test_a_vault_that_is_itself_in_the_temp_folder_is_a_sandbox_and_still_syncs(self):
        sandbox = self.ostemp / "vault"
        sandbox.mkdir()
        save_user_config({"obsidian_vault": str(sandbox)}, self.home)
        project = self.project_with_notes(self.ostemp)
        self.assertEqual(sync_project(project, home=self.home)["status"], "ok")
        self.assertTrue((sandbox / "BosskuAI" / "shop" / "decisions.md").is_file())

    @unittest.skipUnless(os.name == "nt", "Windows paths ignore case")
    def test_the_comparison_ignores_case_on_windows(self):
        project = self.project_with_notes(self.ostemp)
        with mock.patch("tempfile.gettempdir", return_value=str(self.ostemp).upper()):
            self.assertEqual(sync_project(project, home=self.home)["status"], "skipped")
        self.assertEqual(list(self.vault.iterdir()), [])


class SkillsFindIndexTests(unittest.TestCase):
    def test_skills_find_loads_the_routing_index_once(self):
        with tempfile.TemporaryDirectory() as tmp:
            out, err = io.StringIO(), io.StringIO()
            with mock.patch("bossku.index.load_index", wraps=bossku.index.load_index) as loaded, \
                    contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                code = main(["--root", str(ROOT), "--home", tmp, "skills", "find", "fix the failing login test"])
        self.assertEqual(code, 0)
        self.assertEqual(loaded.call_count, 1)
        payload = json.loads(out.getvalue())
        self.assertTrue(payload["skill_id"])
        self.assertTrue(payload["matches"])
        self.assertEqual(payload["selection"]["primary"], payload["skill_id"])


if __name__ == "__main__":
    unittest.main()
