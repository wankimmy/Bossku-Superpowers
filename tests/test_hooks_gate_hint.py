import contextlib
import io
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from bossku.cli import main
from bossku.gate import VERIFY_REASON, decide, gate_output, needs_verification, shows_code_without_editing
from bossku.spec import extract_requirements
from bossku.hint import build_hint, hook_output
from bossku.hooks import (
    ensure_skill_hint_hook, ensure_verify_gate_hook, install_hooks, remove_skill_hint_hook, uninstall_hooks,
)

ROOT = Path(__file__).resolve().parents[1]


def call(name, **args):
    return json.dumps({"type": "assistant", "message": {"content": [{"type": "tool_use", "name": name, "input": args}]}})


class VerifyGateTests(unittest.TestCase):
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
            self.assertIn("ran nothing", gate_output(json.dumps({"transcript_path": str(path)}))["reason"])


def feedback(reason):
    return user("Stop hook feedback:\n" + reason, meta=True)


SPEC_REQUEST = (
    "Create `fmt.py` with `format_size(n)`.\n"
    "- It returns `0 B` for zero.\n"
    "- It uses powers of 1024 and the units B, KiB, MiB, GiB.\n"
    "- It rounds to one decimal place, half up, and drops a trailing `.0`.\n"
    "- It raises `ValueError` for a negative number.\n"
    "- It raises `TypeError` for a bool.\n"
)


class RepeatedAndAuditGateTests(unittest.TestCase):
    def write(self, tmp, lines):
        path = Path(tmp) / "t.jsonl"
        path.write_text("\n".join(lines), encoding="utf-8")
        return json.dumps({"transcript_path": str(path)})

    def test_an_unrun_change_gets_one_reminder_and_is_then_left_alone(self):
        # A second "run it now" reminder made a small model invent tool names and loop for 30+ turns.
        base = [user("Fix the parser."), call("Edit", file_path="p.py")]
        first = decide(base)
        self.assertEqual(first[0], "verify")
        self.assertIn("ran nothing", first[1])
        self.assertIsNone(decide(base + [feedback(first[1])]))

    def test_running_the_code_after_a_reminder_ends_the_reminders(self):
        lines = [user("Fix the parser."), call("Edit", file_path="p.py"), feedback(VERIFY_REASON),
                 call("Bash", command="python -m unittest")]
        self.assertIsNone(decide(lines))

    def test_the_counts_belong_to_the_latest_turn_only(self):
        lines = [user("Fix a."), call("Edit", file_path="a.py"), feedback(VERIFY_REASON),
                 user("Now fix b."), call("Edit", file_path="b.py")]
        self.assertEqual(decide(lines)[0], "verify")
        self.assertIn("ran nothing", decide(lines)[1])

    def test_a_reminder_the_transcript_does_not_show_never_loops(self):
        with tempfile.TemporaryDirectory() as tmp:
            payload = json.loads(self.write(tmp, [user("Fix it."), call("Edit", file_path="a.py")]))
            self.assertEqual(gate_output(json.dumps(payload))["decision"], "block")
            payload["stop_hook_active"] = True
            self.assertEqual(gate_output(json.dumps(payload)), {})

    def test_a_recorded_reminder_with_the_stop_flag_set_lets_the_agent_finish_unless_another_kind_is_due(self):
        with tempfile.TemporaryDirectory() as tmp:
            lines = [user("Fix it."), call("Edit", file_path="a.py"), feedback(VERIFY_REASON)]
            payload = json.loads(self.write(tmp, lines))
            payload["stop_hook_active"] = True
            self.assertEqual(gate_output(json.dumps(payload)), {})
            done = [user(SPEC_REQUEST), call("Write", file_path="fmt.py"), call("Bash", command="python t.py"),
                    feedback(VERIFY_REASON)]
            payload = json.loads(self.write(tmp, done))
            payload["stop_hook_active"] = True
            self.assertIn("requirement audit", gate_output(json.dumps(payload), audit=True)["reason"])

    def test_the_audit_lists_the_requirements_once_after_the_code_was_run(self):
        done = [user(SPEC_REQUEST), call("Write", file_path="fmt.py"), call("Bash", command="python -m unittest")]
        self.assertIsNone(decide(done))
        kind, reason = decide(done, audit=True)
        self.assertEqual(kind, "audit")
        self.assertIn("1. ", reason)
        self.assertIn("ValueError", reason)
        self.assertIsNone(decide(done + [feedback(reason)], audit=True))

    def test_the_audit_waits_for_the_code_to_be_run_and_skips_short_requests_and_non_code_work(self):
        unrun = [user(SPEC_REQUEST), call("Write", file_path="fmt.py")]
        self.assertEqual(decide(unrun, audit=True)[0], "verify")
        short = [user("Fix the typo in the header."), call("Edit", file_path="a.py"), call("Bash", command="python a.py")]
        self.assertIsNone(decide(short, audit=True))
        docs = [user(SPEC_REQUEST), call("Edit", file_path="README.md")]
        self.assertIsNone(decide(docs, audit=True))
        question = [user(SPEC_REQUEST), call("Read", file_path="fmt.py")]
        self.assertIsNone(decide(question, audit=True))

    def test_the_audit_can_be_switched_off_on_its_own(self):
        done = [user(SPEC_REQUEST), call("Write", file_path="fmt.py"), call("Bash", command="python t.py")]
        with mock.patch.dict(os.environ, {"BOSSKU_AUDIT": "0"}):
            self.assertIsNone(decide(done, audit=True))
        with mock.patch.dict(os.environ, {"BOSSKU_VERIFY_GATE": "0"}):
            with tempfile.TemporaryDirectory() as tmp:
                self.assertEqual(gate_output(self.write(tmp, done), audit=True), {})

    def test_the_audit_flag_reaches_the_hook_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            payload = self.write(tmp, [user(SPEC_REQUEST), call("Write", file_path="fmt.py"),
                                       call("Bash", command="python -m unittest")])
            self.assertEqual(gate_output(payload), {})
            self.assertIn("requirement audit", gate_output(payload, audit=True)["reason"])


class RequirementListTests(unittest.TestCase):
    def test_bullets_and_requirement_sentences_become_numbered_items(self):
        items = extract_requirements(SPEC_REQUEST)
        self.assertGreaterEqual(len(items), 5)
        self.assertIn("It raises `ValueError` for a negative number.", items)
        self.assertTrue(any("half up" in item for item in items))

    def test_short_or_vague_requests_get_no_list(self):
        self.assertEqual(extract_requirements("Fix the typo in the header."), [])
        self.assertEqual(extract_requirements("Thanks, that works."), [])
        self.assertEqual(extract_requirements(""), [])

    def test_code_fences_and_duplicates_do_not_pad_the_list(self):
        text = SPEC_REQUEST + "\n```python\nassert format_size(0) == '0 B'\n```\n" + SPEC_REQUEST
        items = extract_requirements(text)
        self.assertEqual(len(items), len(set(item.lower() for item in items)))
        self.assertFalse(any("assert" in item for item in items))

    def test_long_items_are_cut_and_the_list_is_capped(self):
        long_item = "- It must handle " + "very " * 80 + "long input."
        items = extract_requirements("\n".join([long_item] + [f"- Rule number {n} must hold." for n in range(60)]))
        self.assertLessEqual(len(items), 24)
        self.assertLessEqual(len(items[0]), 221)
        self.assertTrue(items[0].endswith("…"))

    def test_the_hint_hook_adds_the_list_only_when_asked(self):
        payload = json.dumps({"prompt": SPEC_REQUEST})
        plain = hook_output(payload)
        with_list = hook_output(payload, spec=True)
        self.assertNotIn("requirement list", json.dumps(plain))
        self.assertIn("requirement list", with_list["hookSpecificOutput"]["additionalContext"])
        self.assertIn("ValueError", with_list["hookSpecificOutput"]["additionalContext"])
        self.assertEqual(hook_output(json.dumps({"prompt": "thanks!"}), spec=True), {})


class SkillHintTests(unittest.TestCase):
    def test_short_prompts_and_slash_commands_get_no_hint(self):
        self.assertIsNone(build_hint("thanks", root=ROOT))
        self.assertIsNone(build_hint("/prototype a pricing page with three layouts to compare", root=ROOT))

    def test_a_clear_request_names_the_matching_skill_and_how_to_load_it(self):
        hint = build_hint("Please audit my website for SEO issues such as missing title tags and meta descriptions",
                          root=ROOT, home=Path(tempfile.gettempdir()) / "no-such-home")
        self.assertIsNotNone(hint)
        self.assertIn("seo", hint.lower())
        self.assertIn("bossku skills show", hint)   # not installed in that home, so it must say how to read it
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


if __name__ == "__main__":
    unittest.main()
