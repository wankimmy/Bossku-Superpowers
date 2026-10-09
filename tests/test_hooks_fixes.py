"""Regression tests for the hook installers, the sync hook and the Stop gate (audit items A02, A07, A10, A11, A12,
A15, A29, A30, B03, B13, B16, B25). Every test uses a temporary home; nothing here touches the real one."""

import contextlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import tomllib
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest import mock

from bossku.cli import main
from bossku.gate import VERIFY_REASON, _turn_lines, decide, gate_output
from bossku.hooks import (
    enable_codex_hooks_feature,
    install_hooks,
    read_hook_stdin,
    run_sync_hook,
    uninstall_hooks,
)
from bossku.memory import save_user_config
from bossku.skills import audit_skills

ROOT = Path(__file__).resolve().parents[1]


def command_hook(command):
    return {"hooks": [{"type": "command", "command": command}]}


def settings_of(home):
    return json.loads((home / ".claude" / "settings.json").read_text(encoding="utf-8"))


def commands_in(entries):
    return [h["command"] for e in entries for h in e["hooks"]]


class OwnershipTests(unittest.TestCase):
    """A02: only commands bossku wrote count as bossku's, whatever else the user's command is called."""

    def test_claude_install_and_uninstall_keep_a_users_own_hook_named_like_ours(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            (home / ".claude").mkdir()
            mine = ["node C:/tools/sync-hook.js", "bash ~/scripts/my-sync-hook-notes.sh"]
            existing = {"hooks": {
                "Stop": [command_hook(c) for c in mine],
                "UserPromptSubmit": [command_hook("node ~/tools/skill-hint.js")],
                "SessionStart": [command_hook("echo session-brief")],
            }}
            (home / ".claude" / "settings.json").write_text(json.dumps(existing), encoding="utf-8")

            install_hooks(home=home, tools=("claude_code",))
            hooks = settings_of(home)["hooks"]
            stop = commands_in(hooks["Stop"])
            self.assertEqual(stop[:2], mine)
            self.assertEqual(len(stop), 4)   # the two of the user, the sync and the verify gate
            self.assertEqual(len(hooks["UserPromptSubmit"]), 2)
            self.assertEqual(len(hooks["SessionStart"]), 2)

            uninstall_hooks(home=home, tools=("claude_code",))
            self.assertEqual(settings_of(home)["hooks"], existing["hooks"])

    def test_cursor_install_and_uninstall_keep_a_users_own_hook_named_like_ours(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            (home / ".cursor").mkdir()
            existing = {"version": 1, "hooks": {"stop": [{"command": "node C:/tools/sync-hook.js"}]}}
            path = home / ".cursor" / "hooks.json"
            path.write_text(json.dumps(existing), encoding="utf-8")

            self.assertEqual(install_hooks(home=home, tools=("cursor",))["cursor"]["status"], "installed")
            self.assertEqual(len(json.loads(path.read_text(encoding="utf-8"))["hooks"]["stop"]), 2)
            uninstall_hooks(home=home, tools=("cursor",))
            self.assertEqual(json.loads(path.read_text(encoding="utf-8"))["hooks"], existing["hooks"])

    def test_every_command_shape_bossku_has_written_is_still_removed(self):
        shapes = [
            "bossku sync-hook",
            '"C:/Program Files/Python312/Scripts/bossku.EXE" sync-hook',
            "C:" + chr(92) + "Users" + chr(92) + "x" + chr(92) + "Scripts" + chr(92) + "bossku.EXE sync-hook",
            '"C:/Python 312/python.exe" -m bossku sync-hook',
            "bossku sync-hook # sync-hook",
            "powershell -NoProfile -ExecutionPolicy Bypass -File 'C:" + chr(92) + "Users" + chr(92)
            + "x" + chr(92) + ".bosskuai" + chr(92) + "codex-sync-hook.ps1'",
            "/home/x/.bosskuai/codex-sync-hook.sh",
        ]
        for shape in shapes:
            with self.subTest(shape=shape), tempfile.TemporaryDirectory() as tmp:
                home = Path(tmp)
                (home / ".cursor").mkdir()
                path = home / ".cursor" / "hooks.json"
                path.write_text(json.dumps({"version": 1, "hooks": {"stop": [{"command": shape}]}}), encoding="utf-8")
                self.assertEqual(uninstall_hooks(home=home, tools=("cursor",))["cursor"]["status"], "removed")
                self.assertNotIn("stop", json.loads(path.read_text(encoding="utf-8"))["hooks"])


class HookStdinTests(unittest.TestCase):
    """A07: the payload is UTF-8 bytes; a Windows pipe hands text decoding to the console code page."""

    def project_with_note(self, root, name):
        project = root / name
        (project / ".bossku" / "memory").mkdir(parents=True)
        (project / ".bossku" / "memory" / "decisions.md").write_text(
            "## 2026-01-01\n\nKeep the unique rule about macrons.\n", encoding="utf-8")
        return project

    def run_cli(self, home, command, payload):
        env = {k: v for k, v in os.environ.items() if k not in ("PYTHONUTF8", "PYTHONIOENCODING")}
        done = subprocess.run([sys.executable, "-m", "bossku", "--home", str(home), command], input=payload,
                              capture_output=True, env=env, cwd=str(ROOT), timeout=120)
        self.assertEqual(done.returncode, 0, done.stderr.decode("utf-8", "replace"))
        return done.stdout.decode("utf-8")

    def test_read_hook_stdin_decodes_utf8_whatever_the_stream_encoding_is(self):
        raw = json.dumps({"cwd": "/work/P" + chr(0x101) + "g" + chr(0x117)}, ensure_ascii=False).encode("utf-8")
        pipe = io.TextIOWrapper(io.BytesIO(raw), encoding="cp1252")   # what a Windows pipe gives
        with mock.patch("sys.stdin", pipe):
            self.assertEqual(json.loads(read_hook_stdin())["cwd"], "/work/P" + chr(0x101) + "g" + chr(0x117))

    def test_sync_hook_and_session_brief_read_a_non_ascii_project_path_from_a_byte_pipe(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "home"
            vault = Path(tmp) / "vault"
            vault.mkdir()
            save_user_config({"obsidian_vault": str(vault)}, home)
            name = "P" + chr(0x101) + "g" + chr(0x117) + "-proj"
            project = self.project_with_note(Path(tmp), name)
            payload = json.dumps({"cwd": str(project)}, ensure_ascii=False).encode("utf-8")

            synced = json.loads(self.run_cli(home, "sync-hook", payload))
            self.assertEqual(synced["exported"], ["decisions.md"], synced)
            self.assertEqual(Path(synced["vault_dir"]).name, name)
            self.assertTrue((vault / "BosskuAI" / name / "decisions.md").is_file())

            brief = json.loads(self.run_cli(home, "session-brief", payload))
            self.assertIn("unique rule about macrons", brief["hookSpecificOutput"]["additionalContext"])

    def test_a_cwd_that_is_not_an_existing_folder_is_skipped_not_a_crash(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            save_user_config({"obsidian_vault": str(home / "vault")}, home)
            (home / "vault").mkdir()
            for cwd in (5, ["x"], str(home / "no-such-folder")):
                with self.subTest(cwd=cwd):
                    with mock.patch("sys.stdin", io.StringIO(json.dumps({"cwd": cwd}))):
                        self.assertEqual(run_sync_hook(home=home)["status"], "skipped")
                    out = io.StringIO()
                    with mock.patch("sys.stdin", io.StringIO(json.dumps({"cwd": cwd}))), contextlib.redirect_stdout(out):
                        self.assertEqual(main(["--home", str(home), "sync-hook"]), 0)
                    self.assertEqual(json.loads(out.getvalue())["status"], "skipped")
            self.assertEqual([p.name for p in (home / "vault").iterdir()], [])

    def test_cursor_payload_with_workspace_roots_syncs_the_workspace_not_the_process_folder(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "home"
            vault = Path(tmp) / "vault"
            vault.mkdir()
            save_user_config({"obsidian_vault": str(vault)}, home)
            empty = Path(tmp) / "empty-root"
            empty.mkdir()
            project = self.project_with_note(Path(tmp), "projB")
            payload = json.dumps({"workspace_roots": [str(empty), str(project)]})
            with mock.patch("sys.stdin", io.StringIO(payload)):
                result = run_sync_hook(home=home)
            self.assertEqual(Path(result["vault_dir"]).name, "projB")
            self.assertEqual(result["exported"], ["decisions.md"])


class OpenCodePluginTests(unittest.TestCase):
    """A10: the plugin gets the command as an argument list, and a missing binary must not end the host."""

    def install_plugin(self, tmp, which):
        home = Path(tmp)
        (home / ".config" / "opencode").mkdir(parents=True)
        with mock.patch("bossku.hooks.shutil.which", return_value=which):
            install_hooks(home=home, tools=("opencode",))
        return home / ".config" / "opencode" / "plugins" / "bossku-sync.js"

    def test_a_path_with_spaces_stays_one_argument_and_a_spawn_error_is_handled(self):
        with tempfile.TemporaryDirectory() as tmp:
            spaced = (Path(tmp) / "Program Files" / "bossku.exe").as_posix()
            text = self.install_plugin(tmp, spaced).read_text(encoding="utf-8")
            line = next(l for l in text.splitlines() if l.startswith("const BOSSKU_ARGV = "))
            self.assertEqual(json.loads(line[len("const BOSSKU_ARGV = "):].rstrip(";")), [spaced])
            self.assertIn('child.on("error"', text)

    @unittest.skipUnless(shutil.which("node"), "node is not installed")
    def test_a_missing_binary_warns_and_the_host_process_keeps_running(self):
        with tempfile.TemporaryDirectory() as tmp:
            plugin = self.install_plugin(tmp, (Path(tmp) / "no such dir" / "bossku.exe").as_posix())
            module = plugin.with_suffix(".mjs")
            module.write_text(plugin.read_text(encoding="utf-8"), encoding="utf-8")
            script = (f'import {{ BosskuSyncPlugin }} from "{module.as_uri()}";'
                      'const p = await BosskuSyncPlugin({ directory: process.cwd() });'
                      'p.event({ event: { type: "session.idle" } });'
                      'await new Promise((done) => setTimeout(done, 500));')
            done = subprocess.run(["node", "--input-type=module", "-e", script], capture_output=True, text=True,
                                  encoding="utf-8", timeout=60)
            self.assertEqual(done.returncode, 0, done.stderr)
            self.assertIn("[bossku-sync]", done.stderr)


class InstallProfileTests(unittest.TestCase):
    """A11: a plain `bossku install` keeps the installed profile; only a new install starts at lean."""

    def run_install(self, home, *flags):
        with mock.patch("bossku.cli.install_user", return_value={"hooks": {}}) as install:
            with contextlib.redirect_stdout(io.StringIO()):
                code = main(["install", "--root", str(ROOT), "--home", str(home), *flags])
        self.assertEqual(code, 0)
        return install.call_args.kwargs["profile"]

    def test_the_installed_profile_is_kept_and_new_installs_get_lean(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            self.assertEqual(self.run_install(home), "lean")
            for kept in ("full", "core", "lean"):
                save_user_config({"installed_from": str(ROOT), "profile": kept}, home)
                self.assertEqual(self.run_install(home), kept)
            save_user_config({"profile": "full"}, home)
            self.assertEqual(self.run_install(home, "--profile", "core"), "core")
            save_user_config({"profile": "nonsense"}, home)
            self.assertEqual(self.run_install(home), "lean")


class CodexConfigTests(unittest.TestCase):
    """A15: edit only [features], leave an explicit false alone, never write TOML Codex cannot read."""

    def config(self, tmp, text):
        codex = Path(tmp) / ".codex"
        codex.mkdir()
        path = codex / "config.toml"
        path.write_bytes(text.encode("utf-8"))
        return path

    def test_an_explicit_false_is_kept_and_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            original = "[features]\nhooks = false # off on purpose\n"
            path = self.config(tmp, original)
            result = install_hooks(home=Path(tmp), tools=("codex",))["codex"]
            self.assertEqual(path.read_bytes().decode("utf-8"), original)
            self.assertEqual(result["status"], "disabled_by_user")
            self.assertEqual(result["features"]["status"], "disabled_by_user")
            self.assertIn("hooks = false", result["features"]["warning"])
            self.assertFalse(list(path.parent.glob("config.toml.bak-*")))

    def test_only_the_features_table_is_edited_and_other_tables_keep_their_hooks_key(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.config(tmp, "[other]\nhooks = false\n\n[features]   # flags\nfoo = 1\n")
            result = enable_codex_hooks_feature(Path(tmp))
            self.assertEqual(result["status"], "installed")
            data = tomllib.loads(path.read_text(encoding="utf-8"))
            self.assertIs(data["features"]["hooks"], True)
            self.assertIs(data["other"]["hooks"], False)
            self.assertEqual(data["features"]["foo"], 1)

    def test_a_hooks_key_in_another_table_is_not_taken_for_ours(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.config(tmp, "[other]\nhooks = true\n")
            self.assertEqual(enable_codex_hooks_feature(Path(tmp))["status"], "installed")
            data = tomllib.loads(path.read_text(encoding="utf-8"))
            self.assertIs(data["features"]["hooks"], True)

    def test_windows_line_endings_stay_windows_line_endings(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.config(tmp, "[model]\r\nname = \"gpt\"\r\n\r\n[features] # x\r\nfoo = 1\r\n")
            enable_codex_hooks_feature(Path(tmp))
            raw = path.read_bytes()
            self.assertEqual(raw.count(b"\n"), raw.count(b"\r\n"))
            self.assertIs(tomllib.loads(raw.decode("utf-8"))["features"]["hooks"], True)

    def test_a_utf8_bom_is_kept_and_does_not_block_the_edit(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.config(tmp, chr(0xFEFF) + "[features] # x" + chr(13) + chr(10) + "foo = 1" + chr(13) + chr(10))
            self.assertEqual(enable_codex_hooks_feature(Path(tmp))["status"], "installed")
            raw = path.read_bytes()
            self.assertTrue(raw.startswith(b"\xef\xbb\xbf[features]"))
            self.assertEqual(raw.count(b"\n"), raw.count(b"\r\n"))
            data = tomllib.loads(raw.decode("utf-8-sig"))
            self.assertEqual(data["features"], {"foo": 1, "hooks": True})
            self.assertEqual(enable_codex_hooks_feature(Path(tmp))["status"], "already_installed")

    def test_a_config_that_is_not_valid_toml_is_left_untouched(self):
        with tempfile.TemporaryDirectory() as tmp:
            broken = "[features\nhooks =\n"
            path = self.config(tmp, broken)
            result = enable_codex_hooks_feature(Path(tmp))
            self.assertEqual(result["status"], "skipped_invalid_toml")
            self.assertIn("warning", result)
            self.assertEqual(path.read_text(encoding="utf-8"), broken)


class SavedAfterAReadTests(unittest.TestCase):
    """A29: `grep x && bossku remember ...` is a save; a read-only command that merely mentions it is not."""

    RULE = "From now on we always run the tests before committing."

    @staticmethod
    def turn(command):
        return [
            json.dumps({"type": "user", "message": {"role": "user", "content": SavedAfterAReadTests.RULE}}),
            json.dumps({"type": "assistant", "message": {"content": [
                {"type": "tool_use", "name": "Bash", "input": {"command": command}}]}}),
        ]

    def test_a_save_chained_after_a_read_only_command_counts(self):
        save = 'bossku remember --kind decision "Always run the tests before committing"'
        for command in (f'grep -rn "tests" docs && {save}', f"ls; {save}", f"cat notes.txt | {save}",
                        f"cd /work && {save} && cat decisions.md"):
            with self.subTest(command=command):
                self.assertIsNone(decide(self.turn(command)))

    def test_commands_that_only_read_or_only_mention_the_save_still_do_not_count(self):
        for command in ('grep -n "bossku remember" README.md', 'echo "x; bossku remember --kind decision y"',
                        'cat a.txt && grep -rn "bossku remember" docs', "ls"):
            with self.subTest(command=command):
                self.assertEqual(decide(self.turn(command))[0], "rule")

    def test_a_line_shlex_cannot_read_is_still_judged(self):
        self.assertIsNone(decide(self.turn('bossku remember --kind decision "unbalanced')))


class SettingsBackupTests(unittest.TestCase):
    """A30 / B16: a backup never replaces an earlier one, and an uninstall makes exactly one."""

    @staticmethod
    def clock(step):
        base = datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        ticks = iter(range(10_000))

        class Clock:
            @classmethod
            def now(cls, tz=None):
                return base + timedelta(seconds=step * next(ticks))

        return Clock

    def test_install_then_uninstall_in_the_same_instant_keeps_the_original_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            (home / ".claude").mkdir()
            settings = home / ".claude" / "settings.json"
            original = json.dumps({"hooks": {"Stop": [command_hook("echo mine")]}}, indent=2)
            settings.write_text(original, encoding="utf-8")
            with mock.patch("bossku.hooks.datetime", self.clock(0)):
                install_hooks(home=home, tools=("claude_code",))
                uninstall_hooks(home=home, tools=("claude_code",))
            backups = list(settings.parent.glob("settings.json.bak-*"))
            self.assertEqual([b.read_text(encoding="utf-8") for b in backups], [original])

    def test_uninstalling_every_claude_hook_makes_one_backup_of_the_full_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            (home / ".claude").mkdir()
            settings = home / ".claude" / "settings.json"
            with mock.patch("bossku.hooks.datetime", self.clock(1)):
                install_hooks(home=home, tools=("claude_code",))
                before = set(settings.parent.glob("settings.json.bak-*"))
                full_state = settings.read_text(encoding="utf-8")
                self.assertEqual(uninstall_hooks(home=home, tools=("claude_code",))["claude_code"]["status"], "removed")
            made = set(settings.parent.glob("settings.json.bak-*")) - before
            self.assertEqual(len(made), 1)
            self.assertEqual(json.loads(made.pop().read_text(encoding="utf-8")), json.loads(full_state))
            self.assertEqual(settings_of(home)["hooks"], {})


class ExitCodeTests(unittest.TestCase):
    """B13: a hook installer that failed turns into exit code 1; the JSON on stdout stays the same."""

    def run_main(self, *argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = main(list(argv))
        return code, out.getvalue()

    def test_a_corrupt_hook_file_fails_the_command_but_the_other_tools_are_still_installed(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            (home / ".cursor").mkdir()
            (home / ".cursor" / "hooks.json").write_text("{ not json", encoding="utf-8")
            (home / ".claude").mkdir()
            code, output = self.run_main("--home", str(home), "hooks", "install")
            self.assertEqual(code, 1)
            result = json.loads(output)
            self.assertEqual(result["cursor"]["status"], "error")
            self.assertEqual(result["claude_code"]["status"], "installed")
            self.assertEqual(self.run_main("--home", str(home), "hooks", "uninstall")[0], 1)

    def test_an_unknown_tool_fails_and_a_clean_run_still_succeeds(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            self.assertEqual(self.run_main("--home", str(home), "hooks", "install", "--tools", "bogus")[0], 1)
            self.assertEqual(self.run_main("--home", str(home), "hooks", "install")[0], 0)
            self.assertEqual(self.run_main("--home", str(home), "hooks", "uninstall")[0], 0)

    def test_install_update_and_purge_report_a_hook_failure_in_their_exit_code(self):
        failed = {"cursor": {"status": "error", "message": "boom"}, "codex": {"status": "installed"}}
        fine = {"cursor": {"status": "installed"}}
        with tempfile.TemporaryDirectory() as tmp:
            base = ("--home", tmp, "--root", str(ROOT))
            for target, argv, key in (("bossku.cli.install_user", ("install",), "hooks"),
                                      ("bossku.cli.update_user", ("update",), "hooks"),
                                      ("bossku.cli.uninstall_user", ("uninstall", "--purge"), "hooks_removed")):
                with self.subTest(command=argv[0]):
                    with mock.patch(target, return_value={key: failed}):
                        self.assertEqual(self.run_main(*argv, *base)[0], 1)
                    with mock.patch(target, return_value={key: fine}):
                        self.assertEqual(self.run_main(*argv, *base)[0], 0)
            with mock.patch("bossku.cli.uninstall_user", return_value={"hooks_removed": None}):
                self.assertEqual(self.run_main("uninstall", *base)[0], 0)


class ColdStartAndAuditTests(unittest.TestCase):
    """A15 / B03: every hook run starts with `import bossku.cli`, so what that import loads is paid on each prompt."""

    def test_the_hook_entry_point_does_not_load_tomllib_or_shlex(self):
        code = "import sys, bossku.cli; print(sorted({'tomllib', 'shlex'} & set(sys.modules)))"
        with tempfile.TemporaryDirectory() as tmp:
            run = subprocess.run([sys.executable, "-c", code], cwd=tmp, capture_output=True, text=True,
                                 env={**os.environ, "PYTHONPATH": str(ROOT)})
        self.assertEqual(run.stdout.strip(), "[]", run.stderr)

    def test_the_skill_audit_prints_how_many_descriptions_lack_use_when(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(main(["skills", "audit", "--root", str(ROOT)]), 0)
        missing = len(audit_skills(ROOT)["custom_descriptions_without_use_when"])
        self.assertIn(f"custom descriptions without 'Use when': {missing}", out.getvalue().splitlines())


class BoundedTranscriptReadTests(unittest.TestCase):
    """B25: the gate reads the session from the end; its verdict must equal the one from reading all of it."""

    @staticmethod
    def user(text):
        return json.dumps({"type": "user", "message": {"role": "user", "content": text}}, ensure_ascii=False)

    @staticmethod
    def edit(path):
        return json.dumps({"type": "assistant", "message": {"content": [
            {"type": "tool_use", "name": "Edit", "input": {"file_path": path}}]}})

    @staticmethod
    def shell(command):
        return json.dumps({"type": "assistant", "message": {"content": [
            {"type": "tool_use", "name": "Bash", "input": {"command": command}}]}})

    @staticmethod
    def whole_read(path):
        """The gate's read before B25: the whole file, one line per LF (the Node gate splits the same way)."""
        text = path.read_bytes().decode("utf-8", errors="replace")
        return [line.removesuffix("\r") for line in text.split("\n")]

    def transcript(self):
        feedback = json.dumps({"type": "user", "isMeta": True, "message": {"content": "x " + VERIFY_REASON}})
        return [
            self.user("Fix a.py"), self.edit("a.py"), feedback, self.shell("python a.py"),
            self.user("From now on we always lint first. Also add b" + chr(0x2028) + "c"), self.edit("b.py"),
            json.dumps({"type": "assistant", "message": {"content": [{"type": "text", "text": "ok " + "x" * 400}]}}),
            self.user("Add c.py with a helper function " + "y" * 3000), self.edit("c.py"), feedback,
            self.user("<system-reminder>not typed by a person</system-reminder>"),
            self.shell('grep -n x && bossku remember --kind decision "lint first"'),
            self.user("Now fix d.py"), self.edit("d.py"), "not json", "",
        ]

    def test_every_prefix_of_a_transcript_gets_the_same_verdict_from_the_bounded_read(self):
        lines = self.transcript()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "t.jsonl"
            for newline in ("\n", "\r\n"):
                for count in range(len(lines) + 1):
                    path.write_bytes(newline.join(lines[:count]).encode("utf-8"))
                    whole = decide(self.whole_read(path))
                    for block in (16, 200, 5000, 1 << 19):
                        with self.subTest(count=count, block=block, newline=repr(newline)):
                            self.assertEqual(decide(_turn_lines(str(path), block)), whole)

    def test_a_long_session_is_cut_at_the_latest_prompt(self):
        older = [self.user(f"Question {i}") for i in range(300)]
        recent = [self.user("Fix e.py"), self.edit("e.py")]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "t.jsonl"
            path.write_text("\n".join(older + recent), encoding="utf-8")
            self.assertEqual(_turn_lines(str(path), 400), recent)
            self.assertEqual(gate_output(json.dumps({"transcript_path": str(path)}))["decision"], "block")

    def test_a_turn_longer_than_one_block_is_parsed_for_prompts_only_once(self):
        lines = [self.user("Fix f.py")] + [self.edit(f"{i}.py") for i in range(600)]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "t.jsonl"
            path.write_text("\n".join(lines), encoding="utf-8")
            with mock.patch("bossku.gate._is_prompt_line", return_value=False) as checked:
                self.assertEqual(_turn_lines(str(path), 1000), lines)   # no prompt in the tail: the whole file
            self.assertLess(checked.call_count, len(lines) // 10)   # the tail block only, not every line again per pass
            self.assertEqual(len({call.args[0] for call in checked.call_args_list}), checked.call_count)

    def test_a_prompt_with_a_raw_line_separator_is_still_one_line(self):
        prompt = self.user("From now on we always lint first. Also add b" + chr(0x2028) + "c")
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "t.jsonl"
            path.write_text("\n".join([self.user("Hello")] * 200 + [prompt, self.edit("b.py")]), encoding="utf-8")
            for block in (400, 1 << 19):
                with self.subTest(block=block):
                    lines = _turn_lines(str(path), block)
                    self.assertIn(prompt, lines)
                    self.assertEqual(decide(lines)[0], "verify")

    def test_without_a_prompt_every_line_is_read(self):
        lines = [self.edit(f"{i}.py") for i in range(40)]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "t.jsonl"
            path.write_text("\n".join(lines), encoding="utf-8")
            self.assertEqual(_turn_lines(str(path), 64), lines)
            path.write_text("", encoding="utf-8")
            self.assertEqual(_turn_lines(str(path), 64), [])


@unittest.skipUnless(sys.platform == "win32" and shutil.which("powershell"), "Windows PowerShell only")
class CodexWrapperEncodingTests(unittest.TestCase):
    """A07: the PowerShell wrapper must pass a non-ASCII project path on to bossku unchanged."""

    def test_wrapper_syncs_a_project_whose_folder_name_is_not_ascii(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "home"
            vault = Path(tmp) / "vault"
            vault.mkdir()
            save_user_config({"obsidian_vault": str(vault)}, home)
            name = "P" + chr(0x101) + "g" + chr(0x117) + "-proj"
            project = Path(tmp) / name
            (project / ".bossku" / "memory").mkdir(parents=True)
            (project / ".bossku" / "memory" / "decisions.md").write_text("## 2026-01-01\n\nA rule.\n", encoding="utf-8")
            env = {k: v for k, v in os.environ.items() if k not in ("PYTHONUTF8", "PYTHONIOENCODING")}
            env.update(USERPROFILE=str(home), HOME=str(home), PYTHONPATH=str(ROOT))
            done = subprocess.run(
                ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File",
                 str(ROOT / "scripts" / "codex-sync-hook.ps1")],
                input=json.dumps({"cwd": str(project)}, ensure_ascii=False).encode("utf-8"),
                capture_output=True, env=env, cwd=str(ROOT), timeout=180)
            self.assertIn(b'"continue"', done.stdout)
            self.assertTrue((vault / "BosskuAI" / name / "decisions.md").is_file())


if __name__ == "__main__":
    unittest.main()
