import contextlib
import io
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from bossku.cli import main
from bossku.gate import SECURITY_REASON, VERIFY_REASON, decide, gate_output, needs_verification, shows_code_without_editing
from bossku.hint import build_hint, hook_output
from bossku.hooks import (
    ensure_skill_hint_hook, ensure_verify_gate_hook, install_hooks, remove_skill_hint_hook, uninstall_hooks,
)

ROOT = Path(__file__).resolve().parents[1]


def call(name, **args):
    return json.dumps({"type": "assistant", "message": {"content": [{"type": "tool_use", "name": name, "input": args}]}})


def run_call(name, id, **args):
    return json.dumps({"type": "assistant", "timestamp": "2026-01-01T00:00:00Z",
                       "message": {"content": [{"type": "tool_use", "id": id, "name": name, "input": args}]}})


def result(id, is_error=False):
    return json.dumps({"type": "user", "message": {"role": "user", "content": [
        {"type": "tool_result", "tool_use_id": id, "content": "x", "is_error": is_error}]}})


class EvidenceGateTests(unittest.TestCase):
    def setUp(self):
        patcher = mock.patch.dict(os.environ, {"BOSSKU_SECURITY_GATE": "off"})
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_read_or_print_commands_are_not_a_verification(self):
        for command in ('grep -r "npm test" .', "cat vitest.config.ts", "echo pytest", "cat pytest.ini",
                        "Get-Content pytest.ini", 'Select-String -Path a.py -Pattern "pytest"',
                        "sed -n 1,5p pytest.ini", "wc -l tests/test_a.py", "ls tests | grep pytest",
                        "type pytest.ini", 'echo "next step:\npytest -q"',
                        "cat >> docs/decisions.md <<'EOF'\n- npm run check: lint and unit tests pass\nEOF",
                        "git commit -q -F - <<'EOF'\nfix\n\nNot verified: npm run dev could not start\nEOF",
                        "Write-Output \"npm test\"", "Write-Host pytest", "gc pytest.ini", "which pytest",
                        "git grep -n pytest", "sudo cat pytest.ini", "/bin/cat pytest.ini"):
            with self.subTest(command=command):
                self.assertTrue(needs_verification([call("Edit", file_path="a.py"), call("Bash", command=command)]))

    def test_a_real_runner_segment_still_verifies(self):
        for command in ("cat x && python -m pytest", "echo go; pytest -q", "cat a.py\npython check.py",
                        "cat > c.py <<'EOF'\nx\nEOF\npython c.py",
                        'ls -la a.wav; node -e "\nconsole.log(1)\n"',
                        'grep -n x a.py | head -4; python -c "\nimport a\nprint(a.f())\n"',
                        'grep -c "a\\"" f; npx tsc --noEmit', "python - <<EOF\nprint(1)\nEOF",
                        'echo "== $(python -m pytest -q 2>&1 | tail -1)"'):
            with self.subTest(command=command):
                self.assertFalse(needs_verification([call("Edit", file_path="a.py"), call("Bash", command=command)]))

    def test_a_failed_check_leaves_the_edit_unverified_and_the_reminder_names_it(self):
        lines = [run_call("Edit", "e1", file_path="a.py"), result("e1"),
                 run_call("Bash", "b1", command="python -m pytest -q\n--tb=short"), result("b1", True)]
        self.assertTrue(needs_verification(lines))
        kind, reason = decide(lines)
        self.assertEqual(kind, "verify")
        self.assertIn("failed", reason)
        self.assertIn("python -m pytest -q --tb=short", reason)
        self.assertTrue(reason.startswith("BosskuAI verify gate: you "))

    def test_a_passing_missing_or_unknown_result_counts_as_verified(self):
        edit = [run_call("Edit", "e1", file_path="a.py"), result("e1")]
        run = run_call("Bash", "b1", command="pytest")
        self.assertFalse(needs_verification(edit + [run, result("b1", False)]))
        self.assertFalse(needs_verification(edit + [run]))
        self.assertFalse(needs_verification(edit + [run, result("other", True)]))

    def test_a_security_verdict_must_start_a_line(self):
        mock.patch.dict(os.environ).start()
        os.environ.pop("BOSSKU_SECURITY_GATE")
        self.addCleanup(mock.patch.stopall)
        base = [call("Edit", file_path="a.py"), call("Bash", command="pytest")]
        self.assertIsNotNone(decide(base + [json.dumps({"type": "assistant", "message": {"content": [
            {"type": "text", "text": "Done. Security gate: PASS"}]}})]))
        self.assertIsNone(decide(base + [json.dumps({"type": "assistant", "message": {"content": [
            {"type": "text", "text": "Done.\n  Security gate: PASS"}]}})]))


class VerifyGateTests(unittest.TestCase):
    def setUp(self):
        # These tests cover the verify reminders; the security gate has its own tests below.
        patcher = mock.patch.dict(os.environ, {"BOSSKU_SECURITY_GATE": "off"})
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_code_edited_and_nothing_run_afterwards_needs_verification(self):
        self.assertTrue(needs_verification([call("Write", file_path="ttl.py")]))
        self.assertTrue(needs_verification([call("Write", file_path="a.py"), call("Bash", command="cat a.py"),
                                            call("Bash", command="git status")]))

    def test_running_the_code_or_a_test_runner_after_the_last_edit_satisfies_the_gate(self):
        for command in ("python -m unittest -v", "python3 check.py", "pytest -q", "npm test", "cd app && node index.js",
                        "go test ./...", "cargo test", "make test", "python -c 'import ttl; print(ttl.X)'"):
            with self.subTest(command=command):
                self.assertFalse(needs_verification([call("Edit", file_path="a.py"), call("Bash", command=command)]))
        self.assertFalse(needs_verification([call("Edit", file_path="a.py"), call("PowerShell", command="python t.py")]))

    def test_an_edit_after_the_last_run_needs_another_run(self):
        calls = [call("Write", file_path="a.py"), call("Bash", command="python -m unittest"),
                 call("Edit", file_path="a.py")]
        self.assertTrue(needs_verification(calls))

    def test_prose_and_config_edits_and_pure_analysis_never_trigger_the_gate(self):
        self.assertFalse(needs_verification([call("Write", file_path="README.md")]))
        self.assertFalse(needs_verification([call("Edit", file_path="config.yml"), call("Edit", file_path="notes.txt")]))
        self.assertFalse(needs_verification([call("Read", file_path="a.py"), call("Bash", command="ls")]))
        self.assertFalse(needs_verification([]))

    def test_words_like_make_in_a_message_are_not_a_test_run(self):
        calls = [call("Edit", file_path="a.py"), call("Bash", command="git commit -m 'make it work'")]
        self.assertTrue(needs_verification(calls))

    def test_subagent_work_is_not_the_agents_own(self):
        sidechain = json.loads(call("Edit", file_path="a.py"))
        sidechain["isSidechain"] = True
        self.assertFalse(needs_verification([json.dumps(sidechain)]))

    def transcript(self, tmp, lines):
        path = Path(tmp) / "t.jsonl"
        path.write_text("\n".join(lines), encoding="utf-8")
        return path

    def test_hook_output_blocks_once_and_only_when_needed(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.transcript(tmp, [call("Write", file_path="a.py")])
            blocked = gate_output(json.dumps({"transcript_path": str(path)}))
            self.assertEqual(blocked["decision"], "block")
            self.assertIn("run", blocked["reason"])
            self.assertEqual(gate_output(json.dumps({"transcript_path": str(path), "stop_hook_active": True})), {})
            done = self.transcript(tmp, [call("Write", file_path="a.py"), call("Bash", command="python a.py")])
            self.assertEqual(gate_output(json.dumps({"transcript_path": str(done)})), {})

    def test_the_gate_fails_open(self):
        self.assertEqual(gate_output(""), {})
        self.assertEqual(gate_output("not json"), {})
        self.assertEqual(gate_output(json.dumps({"transcript_path": "/no/such/file.jsonl"})), {})

    def test_it_can_be_switched_off(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.transcript(tmp, [call("Write", file_path="a.py")])
            with mock.patch.dict(os.environ, {"BOSSKU_VERIFY_GATE": "0"}):
                self.assertEqual(gate_output(json.dumps({"transcript_path": str(path)})), {})

    def test_cli_entrypoint_prints_the_decision(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.transcript(tmp, [call("Write", file_path="a.py")])
            out = io.StringIO()
            with contextlib.redirect_stdout(out), mock.patch("sys.stdin", io.StringIO(json.dumps({"transcript_path": str(path)}))):
                self.assertEqual(main(["verify-gate"]), 0)
            self.assertEqual(json.loads(out.getvalue())["decision"], "block")


def user(text, meta=False):
    event = {"type": "user", "message": {"role": "user", "content": text}}
    if meta:
        event["isMeta"] = True
    return json.dumps(event)


def say(text):
    return json.dumps({"type": "assistant", "message": {"content": [{"type": "text", "text": text}]}})


PASTED = "Here is the file:\n```python\nprint('hi')\n```"


class PastedCodeGateTests(unittest.TestCase):
    """Small models sometimes answer a request for a change by pasting the code into the chat."""

    def test_a_change_request_answered_with_a_code_block_and_no_edit_is_sent_back(self):
        self.assertTrue(shows_code_without_editing([user("Add a helper `slugify(text)` to utils.py."), say(PASTED)]))
        self.assertTrue(shows_code_without_editing(
            [user("Please fix the bug in cart.py"), call("Read", file_path="cart.py"), say(PASTED)]))

    def test_any_edit_or_file_writing_command_means_the_work_was_done(self):
        request = user("Create `ttlcache.py` with a TTLCache class.")
        self.assertFalse(shows_code_without_editing([request, call("Write", file_path="ttlcache.py"), say(PASTED)]))
        for command in ("cat > ttlcache.py <<'EOF'\nx\nEOF", "sed -i 's/a/b/' x.py", "echo hi >> notes.py",
                        "tee out.py", "git apply fix.patch", "cp a.py b.py"):
            with self.subTest(command=command):
                self.assertFalse(shows_code_without_editing([request, call("Bash", command=command), say(PASTED)]))
        self.assertTrue(shows_code_without_editing([request, call("Bash", command="ls -la && cat a.py"), say(PASTED)]))

    def test_questions_and_replies_without_code_are_left_alone(self):
        self.assertFalse(shows_code_without_editing([user("Why does this test fail?"), say(PASTED)]))
        self.assertFalse(shows_code_without_editing([user("Explain how the router scores skills."), say(PASTED)]))
        self.assertFalse(shows_code_without_editing([user("Add a retry to the client."), say("Done, nothing else to add.")]))
        self.assertFalse(shows_code_without_editing([]))

    def test_only_the_latest_turn_counts(self):
        edited_then_asked = [user("Fix the parser."), call("Edit", file_path="p.py"), say("Fixed."),
                             user("Now add a flag --strict to it."), say(PASTED)]
        self.assertTrue(shows_code_without_editing(edited_then_asked))
        pasted_then_asked = [user("Add a flag."), say(PASTED), user("Thanks, why did you pick that name?"), say(PASTED)]
        self.assertFalse(shows_code_without_editing(pasted_then_asked))

    def test_context_the_hooks_add_is_not_a_user_prompt(self):
        lines = [user("Add a flag."), say(PASTED), user("Stop hook feedback: write the change", meta=True), say(PASTED)]
        self.assertTrue(shows_code_without_editing(lines))
        lines = [user("Why is this slow?"), user("Stop hook feedback: please add a fix", meta=True), say(PASTED)]
        self.assertFalse(shows_code_without_editing(lines))

    def test_the_hook_blocks_once_with_its_own_reason_and_respects_the_off_switch(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "t.jsonl"
            path.write_text("\n".join([user("Implement `add(a, b)` in calc.py."), say(PASTED)]), encoding="utf-8")
            blocked = gate_output(json.dumps({"transcript_path": str(path)}))
            self.assertEqual(blocked["decision"], "block")
            self.assertIn("edited no file", blocked["reason"])
            self.assertEqual(gate_output(json.dumps({"transcript_path": str(path), "stop_hook_active": True})), {})
            with mock.patch.dict(os.environ, {"BOSSKU_VERIFY_GATE": "0"}):
                self.assertEqual(gate_output(json.dumps({"transcript_path": str(path)})), {})

    def test_editing_code_without_running_it_keeps_its_own_reason(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "t.jsonl"
            path.write_text("\n".join([user("Fix the bug."), call("Edit", file_path="a.py"), say(PASTED)]), encoding="utf-8")
            self.assertIn("have not run anything", gate_output(json.dumps({"transcript_path": str(path)}))["reason"])


def feedback(reason):
    return user("Stop hook feedback:\n" + reason, meta=True)


class RepeatedReminderTests(unittest.TestCase):
    def setUp(self):
        # These tests cover the verify reminders; the security gate has its own tests below.
        patcher = mock.patch.dict(os.environ, {"BOSSKU_SECURITY_GATE": "off"})
        patcher.start()
        self.addCleanup(patcher.stop)

    def write(self, tmp, lines):
        path = Path(tmp) / "t.jsonl"
        path.write_text("\n".join(lines), encoding="utf-8")
        return json.dumps({"transcript_path": str(path)})

    def test_an_unrun_change_gets_one_reminder_and_is_then_left_alone(self):
        # A second "run it now" reminder made a small model invent tool names and loop for 30+ turns.
        base = [user("Fix the parser."), call("Edit", file_path="p.py")]
        first = decide(base)
        self.assertEqual(first[0], "verify")
        self.assertIn("have not run anything", first[1])
        self.assertIsNone(decide(base + [feedback(first[1])]))

    def test_running_the_code_after_a_reminder_ends_the_reminders(self):
        lines = [user("Fix the parser."), call("Edit", file_path="p.py"), feedback(VERIFY_REASON),
                 call("Bash", command="python -m unittest")]
        self.assertIsNone(decide(lines))

    def test_the_counts_belong_to_the_latest_turn_only(self):
        lines = [user("Fix a."), call("Edit", file_path="a.py"), feedback(VERIFY_REASON),
                 user("Now fix b."), call("Edit", file_path="b.py")]
        self.assertEqual(decide(lines)[0], "verify")
        self.assertIn("have not run anything", decide(lines)[1])

    def test_a_reminder_the_transcript_does_not_show_never_loops(self):
        with tempfile.TemporaryDirectory() as tmp:
            payload = json.loads(self.write(tmp, [user("Fix it."), call("Edit", file_path="a.py")]))
            self.assertEqual(gate_output(json.dumps(payload))["decision"], "block")
            payload["stop_hook_active"] = True
            self.assertEqual(gate_output(json.dumps(payload)), {})

    def test_a_recorded_reminder_with_the_stop_flag_set_lets_the_agent_finish(self):
        with tempfile.TemporaryDirectory() as tmp:
            lines = [user("Fix it."), call("Edit", file_path="a.py"), feedback(VERIFY_REASON)]
            payload = json.loads(self.write(tmp, lines))
            payload["stop_hook_active"] = True
            self.assertEqual(gate_output(json.dumps(payload)), {})


class SecurityGateTests(unittest.TestCase):
    def test_a_verified_change_still_needs_the_security_verdict_once(self):
        base = [user("Add a refund endpoint."), call("Edit", file_path="refund.py"), call("Bash", command="python -m unittest")]
        self.assertEqual(decide(base + [say("Done.")])[0], "security")
        self.assertIsNone(decide(base + [say("Done.\nSecurity gate: PASS (quick)")]))
        self.assertIsNone(decide(base + [say("Done."), feedback(SECURITY_REASON), say("Still done.")]))

    def test_dependency_and_infra_files_count_and_stylesheets_and_docs_do_not(self):
        from bossku.gate import _needs_security

        for target in ("refund.py", "package-lock.json", "requirements.txt", "Dockerfile", ".github/workflows/ci.yml",
                       "infra/main.tf"):
            self.assertTrue(_needs_security([("Edit", {"file_path": target})]), target)
        for target in ("site.css", "README.md", "config/labels.yml"):
            self.assertFalse(_needs_security([("Edit", {"file_path": target})]), target)

    def test_it_has_its_own_off_switch(self):
        lines = [user("Bump it."), call("Edit", file_path="package.json"), say("Done.")]
        with mock.patch.dict(os.environ, {"BOSSKU_SECURITY_GATE": "off"}):
            self.assertIsNone(decide(lines))


class SecurityReminderTests(unittest.TestCase):
    def test_a_change_request_gets_the_rule_and_a_question_does_not(self):
        from bossku.security import security_reminders

        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "home"
            self.assertIn("Security gate: PASS", security_reminders("add a coupon endpoint", "", home=home)[0])
            self.assertEqual(security_reminders("what does this function return?", "", home=home), [])

    def test_the_daily_dependency_check_asks_once_per_project_per_day(self):
        from bossku.security import security_reminders

        with tempfile.TemporaryDirectory() as tmp:
            home, project = Path(tmp) / "home", Path(tmp) / "proj"
            project.mkdir()
            ask = lambda day: security_reminders("explain the router", str(project), home=home, today=day)
            self.assertEqual(ask("2026-10-28"), [])   # no manifest, nothing to check
            (project / "package.json").write_text("{}", encoding="utf-8")
            first = ask("2026-10-28")
            self.assertEqual(len(first), 1)
            self.assertIn("package.json", first[0])
            self.assertEqual(ask("2026-10-28"), [])
            self.assertEqual(len(ask("2026-10-29")), 1)

    def test_the_prompt_hook_carries_the_reminders(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = hook_output(json.dumps({"prompt": "fix the refund double-charge bug", "cwd": tmp}), home=Path(tmp))
            self.assertIn("security gate (must rule)", out["hookSpecificOutput"]["additionalContext"])


class SkillHintTests(unittest.TestCase):
    def test_short_prompts_and_slash_commands_get_no_hint(self):
        self.assertIsNone(build_hint("thanks", root=ROOT))
        self.assertIsNone(build_hint("/prototype a pricing page with three layouts to compare", root=ROOT))

    def test_short_tasks_and_explicit_requests_are_hinted(self):
        for prompt, sid in (("audit SEO", "seo-audit"), ("use bosskuai-tdd-loop", "bosskuai-tdd-loop")):
            with self.subTest(prompt=prompt):
                text = build_hint(prompt, root=ROOT)
                self.assertIsNotNone(text)
                self.assertIn(sid, text)

    def test_a_clear_request_names_the_matching_skill_and_how_to_load_it(self):
        hint = build_hint("Please audit my website for SEO issues such as missing title tags and meta descriptions",
                          root=ROOT, home=Path(tempfile.gettempdir()) / "no-such-home")
        self.assertIsNotNone(hint)
        self.assertIn("seo", hint.lower())
        self.assertIn(f"Read {(ROOT / 'skills' / 'seo-audit' / 'SKILL.md').as_posix()}", hint)
        self.assertIn("skills show <id>", hint)
        self.assertLessEqual(len(hint.splitlines()), 4)

    def test_hook_output_has_the_shape_claude_code_expects(self):
        payload = json.dumps({"prompt": "Please audit my website for SEO issues such as missing title tags"})
        out = hook_output(payload, root=ROOT)
        self.assertEqual(out["hookSpecificOutput"]["hookEventName"], "UserPromptSubmit")
        self.assertIn("additionalContext", out["hookSpecificOutput"])

    def test_bad_input_never_breaks_the_prompt(self):
        for text in ("", "not json", json.dumps({"prompt": 5}), json.dumps([])):
            self.assertEqual(hook_output(text, root=ROOT), {})


class HookInstallTests(unittest.TestCase):
    def test_install_adds_hint_and_gate_once_and_uninstall_removes_only_ours(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            (home / ".claude").mkdir()
            settings = home / ".claude" / "settings.json"
            settings.write_text(json.dumps({"hooks": {"Stop": [{"hooks": [{"type": "command", "command": "echo mine"}]}]}}),
                                encoding="utf-8")
            first = install_hooks(home=home, tools=("claude_code",))["claude_code"]
            self.assertIn("verify-gate", first["added"])
            self.assertIn("skill-hint", first["added"])
            again = install_hooks(home=home, tools=("claude_code",))["claude_code"]
            self.assertEqual(again["status"], "already_installed")
            data = json.loads(settings.read_text(encoding="utf-8"))
            self.assertEqual(len(data["hooks"]["UserPromptSubmit"]), 1)
            self.assertEqual(sum("verify-gate" in json.dumps(e) for e in data["hooks"]["Stop"]), 1)
            uninstall_hooks(home=home, tools=("claude_code",))
            data = json.loads(settings.read_text(encoding="utf-8"))
            self.assertNotIn("UserPromptSubmit", data["hooks"])
            self.assertEqual(data["hooks"]["Stop"], [{"hooks": [{"type": "command", "command": "echo mine"}]}])

    def test_project_level_settings_can_carry_the_same_hooks(self):
        with tempfile.TemporaryDirectory() as tmp:
            settings = Path(tmp) / ".claude" / "settings.json"
            self.assertTrue(ensure_skill_hint_hook(settings, command="bossku skill-hint"))
            self.assertTrue(ensure_verify_gate_hook(settings, command="bossku verify-gate"))
            self.assertFalse(ensure_skill_hint_hook(settings, command="bossku skill-hint"))
            data = json.loads(settings.read_text(encoding="utf-8"))
            self.assertEqual(set(data["hooks"]), {"UserPromptSubmit", "Stop"})
            self.assertTrue(remove_skill_hint_hook(settings))


def error_result(id, text):
    return json.dumps({"type": "user", "message": {"role": "user", "content": [
        {"type": "tool_result", "tool_use_id": id, "content": text, "is_error": True}]}})


class CommandReaderAuditTests(unittest.TestCase):
    """The audit fixes G1-G11. Every input here is also in tests/hooks.test.mjs: the two gates must read alike."""

    def setUp(self):
        patcher = mock.patch.dict(os.environ, {"BOSSKU_SECURITY_GATE": "off"})
        patcher.start()
        self.addCleanup(patcher.stop)

    def checked(self, command, tool="Bash"):
        return not needs_verification([call("Edit", file_path="a.py"), call(tool, command=command)])

    def test_a_denied_or_aborted_check_did_not_run_and_the_last_one_that_ran_decides(self):
        def lines(first, second):
            return [run_call("Edit", "e1", file_path="a.py"), result("e1"), run_call("Bash", "b1", command="npm test"), first,
                    run_call("Bash", "b2", command="pytest -q"), second]
        for text in (
            "Permission for this action was denied by the Claude Code auto mode classifier. Reason: [Production Reads]. If you have other tasks, continue.",
            "Permission for this command was denied by a built-in Claude Code safety check, not by the user.",
            "Permission to use Bash with command pytest -q has been denied.",
            "The user doesn't want to proceed with this tool use. The tool use was rejected (eg. if it was a file edit, the new_string was NOT written).",
            "<error>Command was aborted before completion</error>",
            "[Request interrupted by user for tool use]",
            "PreToolUse:Bash hook error: BosskuAI guard denied: docker stop x (stops a running container).",
            "Permission to use Bash with command cd app &&\nnpm test has been denied.",
            "Permission to use Bash with command " + "x" * 1200 + " has been denied.",
            "The server-side auto mode classifier gave no verdict for Bash, so the command was not run.",
            "<tool_use_error>Blocked: sleep 30 followed by: npm test. Run it in the background instead.</tool_use_error>",
            "This agent is isolated in the worktree C:/w/x and may not run commands outside it.",
        ):
            with self.subTest(text=text):
                self.assertFalse(needs_verification(lines(result("b1"), error_result("b2", text))))
        blocks = [{"type": "text", "text": "Permission for this action was denied by the Claude Code auto mode classifier."}]
        self.assertFalse(needs_verification(lines(result("b1"), error_result("b2", blocks))))
        aborted = "<error>Command was aborted before completion</error>"
        kind, reason = decide(lines(error_result("b1", "Exit code 1\nFAILED"), error_result("b2", aborted)))
        self.assertIn("`npm test`", reason)
        both = lines(error_result("b1", aborted), error_result("b2", "Permission for this action was denied"))
        self.assertTrue(needs_verification(both))
        self.assertEqual(decide(both)[1], VERIFY_REASON)
        for text in ("Exit code 1\nPermission denied: ./run.sh", "Exit code 2\nCommand was aborted before completion",
                     "Error: spawn pytest ENOENT"):
            with self.subTest(text=text):
                self.assertIn("`pytest -q`", decide(lines(result("b1"), error_result("b2", text)))[1])

    def test_a_hash_at_the_start_of_a_word_is_a_comment(self):
        self.assertTrue(self.checked("cat package.json  # what's in it\nnpm test"))
        self.assertTrue(self.checked("echo hi # it's done\nnpm test"))
        self.assertFalse(self.checked("true # npm test"))
        self.assertTrue(self.checked("echo a#b; npm test"))
        self.assertTrue(self.checked('echo "a # b"; npm test'))

    def test_powershell_reads_a_backslash_as_plain_and_a_backtick_as_the_escape(self):
        for command in ('Get-ChildItem "C:\\Users\\Me\\proj\\"; npm test', "dir C:\\Users\\Me\\proj\\; npm test",
                        'Write-Host "a `" b"; npm test'):
            with self.subTest(command=command):
                self.assertTrue(self.checked(command, "PowerShell"))
        self.assertFalse(self.checked("dir C:\\Users\\Me\\proj\\; npm test", "Bash"))

    def test_a_script_named_after_a_read_word_is_not_read_only(self):
        for command in ("./scripts/type-check.sh", "./tools/stat-report.py"):
            with self.subTest(command=command):
                self.assertTrue(self.checked(command))
        for command in ("type pytest.ini", "cat.exe pytest.ini", "C:\\Windows\\System32\\findstr.exe pytest setup.cfg",
                        "/usr/bin/grep -n pytest a.py"):
            with self.subTest(command=command):
                self.assertFalse(self.checked(command))

    def test_a_path_qualified_or_quoted_interpreter_counts(self):
        for command in (".venv/bin/python smoke.py", "/usr/bin/python3 smoke.py",
                        '"C:/Program Files/Python312/python.exe" smoke.py', "C:/tools/python.exe - <<'EOF'\nprint(1)\nEOF",
                        "PYTHONPATH=. .venv/bin/python smoke.py", "timeout 60 .venv/bin/python smoke.py"):
            with self.subTest(command=command):
                self.assertTrue(self.checked(command))
        self.assertTrue(self.checked("& 'C:\\Program Files\\nodejs\\node.exe' smoke.js", "PowerShell"))
        for command in ("git add src/python docs", ".venv/bin/python --version", "ls .venv/bin/python x",
                        "NODE=/usr/bin/node npm install", "x=/usr/bin/python3 y"):
            with self.subTest(command=command):
                self.assertFalse(self.checked(command))

    def test_the_heredoc_skip_is_linear_and_an_unterminated_one_swallows_nothing(self):
        import time
        for count, limit in ((2000, 1.0), (18000, 2.0)):
            start = time.perf_counter()
            self.assertFalse(self.checked("cat <<A\nx\nA\n" * count))
            self.assertLess(time.perf_counter() - start, limit, f"{count} heredocs")
        self.assertTrue(self.checked("echo $((1<<2))\nnpm test"))
        self.assertFalse(self.checked("cat <<EOF\nnpm test\nEOF"))

    def test_an_inline_secret_in_a_failed_command_is_masked(self):
        from bossku.evidence import summarize
        for command, secret in (("API_KEY=sk-FAKEFAKEFAKEFAKEFAKE1234 npm test", "FAKEFAKE"),
                                ("GH_TOKEN=ghp_FAKEFAKEFAKEFAKEFAKEFAKE1234 npx vitest run", "FAKEFAKE"),
                                ("python deploy_check.py --password hunter2secret", "hunter2secret"),
                                ("python deploy_check.py --api-key=hunter2secret", "hunter2secret"),
                                ("python deploy_check.py sk-FAKEFAKEFAKEFAKEFAKE1234", "FAKEFAKE"),
                                ("DB_PASSWORD=hunter2secret npm test", "hunter2secret"),
                                ("curl -u admin:hunter2secret http://localhost:3000/health && npm test", "hunter2secret"),
                                ("curl http://bob:hunter2secret@localhost:3000/x && npm test", "hunter2secret"),
                                ('curl -H "Authorization: Bearer abc123def456ghi789jkl" http://localhost:3000/health && npm test', "abc123def456"),
                                ('curl -H "Authorization: Basic dXNlcjpodW50ZXIyc2VjcmV0" http://localhost:3000/health && npm test', "dXNlcjpodW50"),
                                ("gh secret set FOO --body hunter2secret && npm test", "hunter2secret"),
                                ("mysql -phunter2secret -e x && npm test", "hunter2secret"),
                                ("docker login -u bob -p hunter2secret && npm test", "hunter2secret"),
                                ('npm test -- --header "X-Api-Key: hunter2secret"', "hunter2secret"),
                                ('npm test \'{"token": "hunter2secret"}\'', "hunter2secret"),
                                ('python check.py --password "my hunter2secret phrase"', "hunter2secret"),
                                ("python check.py --password 'my hunter2secret phrase'", "hunter2secret"),
                                ('python check.py --token="my hunter2secret phrase"', "hunter2secret"),
                                ("python check.py -Password hunter2secret", "hunter2secret"),
                                ('DB_PASSWORD="my hunter2secret phrase" npm test', "hunter2secret"),
                                ("API_TOKEN='my hunter2secret phrase' pytest", "hunter2secret"),
                                ("MYSQL -phunter2secret -e x && npm test", "hunter2secret"),
                                ('python check.py --password "my hunter2secret phrase', "hunter2secret"),
                                ("python check.py --api_key hunter2secret", "hunter2secret"),
                                ("python check.py --db_password hunter2secret", "hunter2secret"),
                                ("python smoke.py -AdminPassword hunter2secret", "hunter2secret"),
                                ('curl -u "admin:my hunter2secret phrase" http://localhost:3000/health && npm test', "hunter2secret"),
                                ('mysql -u root -p"my hunter2secret phrase" && npm test', "hunter2secret"),
                                ('docker login -u bob -p "my hunter2secret phrase" && npm test', "hunter2secret"),
                                ('gh secret set FOO --body "my hunter2secret phrase" && npm test', "hunter2secret")):
            with self.subTest(command=command):
                lines = [run_call("Edit", "e1", file_path="a.py"), result("e1"), run_call("Bash", "b1", command=command),
                         result("b1", True)]
                reason = decide(lines)[1]
                self.assertNotIn(secret, reason)
                self.assertIn("[REDACTED]", reason)
                with tempfile.TemporaryDirectory() as tmp:
                    path = Path(tmp) / "t.jsonl"
                    path.write_text("\n".join(lines), encoding="utf-8")
                    shown = summarize(str(path))["checks"][0]["command"]
                self.assertNotIn(secret, shown)
                self.assertIn("[REDACTED]", shown)
        plain = [run_call("Edit", "e1", file_path="a.py"), result("e1"),
                 run_call("Bash", "b1", command="npm test -- --silent"), result("b1", True)]
        self.assertIn("`npm test -- --silent`", decide(plain)[1])

    def test_ordinary_commands_are_not_mangled_by_the_secret_masks(self):
        from bossku.evidence import summarize
        for command in ("pytest -p no:cacheprovider", "git log --author=x && npm test", "npm test -- --passWithNoTests",
                        'curl --user-agent "x y" http://localhost:3000/health && npm test', "ssh -p 2222 host && pytest",
                        'python -m pytest -k "token and not slow"', 'grep -q "API_KEY=" .env.example && npm test',
                        'grep -q "password=" .env && npm test', 'grep -q "--token " x && npm test',
                        "./bin/reset-pass admin && npm test"):
            with self.subTest(command=command):
                lines = [run_call("Edit", "e1", file_path="a.py"), result("e1"), run_call("Bash", "b1", command=command),
                         result("b1", True)]
                self.assertIn(f"`{command}`", decide(lines)[1])
                with tempfile.TemporaryDirectory() as tmp:
                    path = Path(tmp) / "t.jsonl"
                    path.write_text("\n".join(lines), encoding="utf-8")
                    self.assertEqual(summarize(str(path))["checks"][0]["command"], command)

    def test_a_huge_failed_command_is_cut_before_it_is_masked(self):
        import time
        from bossku.evidence import summarize
        huge = 'x="' + "curl " * 40000 + '"; python check.py'
        cut = 'python check.py --password "' + "word " * 600       # the quote is still open where the cut falls
        for command in (huge, cut, "python check.py --password " + "A" * 3000):
            with self.subTest(command=command[:40]):
                lines = [run_call("Edit", "e1", file_path="a.py"), result("e1"), run_call("Bash", "b1", command=command),
                         result("b1", True)]
                start = time.perf_counter()
                reason = decide(lines)[1]
                with tempfile.TemporaryDirectory() as tmp:
                    path = Path(tmp) / "t.jsonl"
                    path.write_text("\n".join(lines), encoding="utf-8")
                    shown = summarize(str(path))["checks"][0]["command"]
                self.assertLess(time.perf_counter() - start, 5.0)
                for text in (reason, shown):
                    self.assertNotIn("word word", text)
                    self.assertNotIn("AAAA", text)
        self.assertIn("--password [REDACTED]", shown)

    def test_a_command_that_repeats_a_check_word_stays_fast_to_read(self):
        import time
        for word in ("curl ", "mvn "):
            start = time.perf_counter()
            self.checked(word * 40000)
            self.assertLess(time.perf_counter() - start, 1.5, word)

    def test_a_script_path_counts_only_as_the_command_word(self):
        for command in ("./run.sh", "./scripts/type-check.sh", "./tools/stat-report.py", "CI=1 ./run_tests.sh",
                        "timeout 60 ./run.sh", "bash ./run.sh", "cd app && ./run.sh"):
            with self.subTest(command=command):
                self.assertTrue(self.checked(command))
        for command in ("sudo ./x.sh", "time ./x.sh", "env A=1 ./x.sh", "! ./check.sh", "exec ./x.sh", "nohup ./x.sh",
                        "command ./x.sh", "{ ./x.sh; }", "if ./check.sh; then echo ok; fi", "if true; then ./check.sh; fi",
                        "for i in 1 2; do ./x.sh $i; done"):
            with self.subTest(command=command):
                self.assertTrue(self.checked(command))
        for command in ("chmod +x ./run.sh", "git add ./tools/check.py", "rm ./old.py", "git diff --stat ./scripts/build.sh"):
            with self.subTest(command=command):
                self.assertFalse(self.checked(command))

    def test_an_escaped_space_does_not_start_a_comment(self):
        self.assertTrue(self.checked("echo fix\\ #12; npm test"))
        self.assertTrue(self.checked("echo fix\\\n#12; npm test"))
        self.assertFalse(self.checked("true fix\\  # npm test"))
        self.assertFalse(self.checked("git add . \\\n# npm test"))
        self.assertFalse(self.checked("git add . `\n# npm test", "PowerShell"))
        self.assertTrue(self.checked("Write-Host fix` #12; npm test", "PowerShell"))

    def test_many_different_unterminated_heredoc_words_stay_linear(self):
        import time
        start = time.perf_counter()
        self.assertFalse(self.checked("".join(f": $((1<<a{n}))\n" for n in range(13000))))
        self.assertLess(time.perf_counter() - start, 2.0)
        self.assertTrue(self.checked("".join(f": $((1<<a{n}))\n" for n in range(50)) + "npm test"))
        closed = "".join(f"cat <<D{n}\n" for n in range(9000)) + "".join(f"D{n}\n" for n in range(9000))
        start = time.perf_counter()
        self.checked(closed)
        self.assertLess(time.perf_counter() - start, 2.0)

    def test_the_security_verdict_takes_the_review_line_prefixes(self):
        mock.patch.dict(os.environ).start()
        os.environ.pop("BOSSKU_SECURITY_GATE")
        self.addCleanup(mock.patch.stopall)
        base = [call("Edit", file_path="a.py"), call("Bash", command="pytest")]

        def verdict(text):
            return decide(base + [json.dumps({"type": "assistant", "message": {"content": [{"type": "text", "text": text}]}})])
        for line in ("> Security gate: PASS", "- Security gate: PASS", "* Security gate: PASS", "**Security gate:** PASS",
                     "_Security gate: PASS_", "Done.\rSecurity gate: PASS"):
            with self.subTest(line=line):
                self.assertIsNone(verdict(line))
        for prose in ("Done. Security gate: PASS", "see the Security gate: PASS line", "Done - Security gate: PASS"):
            with self.subTest(prose=prose):
                self.assertIsNotNone(verdict(prose))


if __name__ == "__main__":
    unittest.main()
