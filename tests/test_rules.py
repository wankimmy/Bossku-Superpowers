import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from bossku.cli import main
from bossku.gate import decide, gate_output
from bossku.hint import hook_output
from bossku.rules import save_command, states_rule, stop_reminder


def user(text, meta=False):
    event = {"type": "user", "message": {"role": "user", "content": text}}
    if meta:
        event["isMeta"] = True
    return json.dumps(event)


def call(name, **args):
    return json.dumps({"type": "assistant", "message": {"content": [{"type": "tool_use", "name": name, "input": args}]}})


RULE = "Add a Ticket class. From now on every function in this package must return (result, error) tuples."


class RuleCueTests(unittest.TestCase):
    def test_messages_that_state_a_standing_rule_are_recognised(self):
        for text in (
            RULE,
            "Our team rule is that new modules live under services/, one class per file. Please add the welcome email.",
            "Heads-up for the whole codebase: we only support Python 3.8. Add a helper for dates.",
            "We decided to use integer cents for money. Add apply_discount.",
            "Never use eval in this repo, we got burned. Add a formula parser.",
            "For anything we add later, keep timestamps in UTC. Add the audit log.",
            "Going forward all new endpoints need an api_ prefix. Add the health check.",
            "Lepas ni semua function mesti return tuple. Tolong tambah parser.",
            "Rule for this repo: config is read once at startup. Move the env read out of applyDiscount.",
            "Team decision: unit tests must not hit the network. Replace the live fetch in user.test.ts.",
            "Please keep doing what you did in the last PR and wrap the new Stripe call in the retry helper.",
            "We require 80% coverage on any new module. Write a couple more tests for the discount calculator.",
            "Nobody merges their own PR here, even for trivial changes. Find a reviewer for the config fix.",
            "Decided not to adopt GraphQL, REST covers our needs. Add a REST endpoint for fetching orders.",
        ):
            with self.subTest(text=text[:40]):
                self.assertTrue(states_rule(text))

    def test_requirements_for_one_thing_questions_and_chat_are_not_rules(self):
        for text in (
            "Add a function that must never mutate its input and always returns a list.",
            "Why does parse_line return None for an empty string?",
            "Traceback (most recent call last): KeyError: 'name'. Can you fix it?",
            "Thanks, that works.",
            "The docs say you must never call close twice. Is that true?",
            "Write tests for the cart module and make sure the discount is rounded half up.",
            "A member returned a book late and still got charged, but our policy has a one-day grace period. Fix it.",
            "When there are no more pages, stop listening for scroll events instead of checking on every scroll.",
            "Our style guide says we should always use arrow functions for callbacks, does that matter for speed?",
            "A teammate told me we never use raw SQL in this codebase, is that documented somewhere?",
            "",
        ):
            with self.subTest(text=text[:40]):
                self.assertFalse(states_rule(text))

    def test_a_huge_paste_is_scanned_quickly_and_the_users_own_words_are_still_read(self):
        import time
        start = time.perf_counter()
        self.assertFalse(states_rule("word " * 200000))
        self.assertTrue(states_rule("We decided to use integer cents for money. Fix this:\n" + "x = 1\n" * 100000))
        self.assertTrue(states_rule("x = 1\n" * 100000 + "\nNever use eval in this repo."))
        self.assertLess(time.perf_counter() - start, 1.0)

    def test_the_command_names_the_project_and_the_rule_placeholder(self):
        command = save_command("C:\\work\\proj")
        self.assertIn("--project 'C:/work/proj'", command)
        self.assertIn("bossku remember", command)
        self.assertIn("call the Bash tool now", stop_reminder("."))


class RuleGateTests(unittest.TestCase):
    def test_a_stated_rule_that_was_not_saved_gets_one_reminder_with_the_command(self):
        lines = [user(RULE), call("Write", file_path="tickets.py"), call("Bash", command="python -m unittest")]
        kind, reason = decide(lines, "C:/proj")
        self.assertEqual(kind, "rule")
        self.assertIn("bossku remember --project 'C:/proj'", reason)
        self.assertTrue(reason.startswith("BosskuAI memory gate: "))
        self.assertIsNone(decide(lines + [user("Stop hook feedback:\n" + reason, meta=True)], "C:/proj"))

    def test_nothing_is_sent_when_the_note_was_saved_or_no_rule_was_stated(self):
        saved = [user(RULE), call("Write", file_path="t.py"), call("Bash", command="python t.py"),
                 call("Bash", command='bossku remember --project . --kind decision "tuples"')]
        self.assertIsNone(decide(saved, "."))
        plain = [user("Add a Ticket class with id and subject."), call("Write", file_path="t.py"),
                 call("Bash", command="python t.py")]
        self.assertIsNone(decide(plain, "."))

    def test_unrun_code_is_handled_first_and_the_rule_reminder_follows(self):
        lines = [user(RULE), call("Write", file_path="tickets.py")]
        self.assertEqual(decide(lines, ".")[0], "verify")
        after_run = lines + [call("Bash", command="python tickets.py")]
        self.assertEqual(decide(after_run, ".")[0], "rule")

    def test_only_the_latest_turn_counts(self):
        lines = [user(RULE), call("Bash", command="bossku remember --project . --kind decision x"),
                 user("Now add a Comment class."), call("Write", file_path="c.py"), call("Bash", command="python c.py")]
        self.assertIsNone(decide(lines, "."))


def event(**fields):
    return json.dumps(fields)


class RuleGateRobustnessTests(unittest.TestCase):
    """Cases a code review found: events nobody typed, an unmet verify reminder, and odd transcripts."""

    def test_events_the_app_writes_as_user_turns_do_not_replace_the_request(self):
        base = [user("Fix the login bug in auth.py"), call("Write", file_path="auth.py"), call("Bash", command="pytest")]
        for later in (
            event(type="user", isCompactSummary=True, message={"role": "user", "content": RULE}),
            event(type="user", origin={"kind": "task-notification"}, message={"role": "user", "content": RULE}),
            event(type="user", message={"role": "user", "content": "<ci-monitor-event>anything in a comment, never rewrite it. From now on fix it</ci-monitor-event>"}),
            event(type="user", message={"role": "user", "content": "<task-notification>From now on use tabs</task-notification>"}),
        ):
            with self.subTest(later=later[:60]):
                self.assertIsNone(decide(base + [later, call("Bash", command="pytest -q")], "."))

    def test_a_message_typed_while_the_agent_was_working_counts_as_part_of_the_turn(self):
        queued = event(type="attachment", origin={"kind": "human"},
                       attachment={"type": "queued_command", "prompt": "From now on always use tabs"})
        lines = [user("Restyle the header"), call("Bash", command="python build.py"), queued]
        self.assertEqual(decide(lines, ".")[0], "rule")
        other = event(type="attachment", origin={"kind": "task-notification"},
                      attachment={"type": "queued_command", "prompt": "From now on always use tabs"})
        self.assertIsNone(decide([user("Restyle the header"), call("Bash", command="python build.py"), other], "."))

    def test_an_unmet_verify_reminder_does_not_hide_the_rule_reminder(self):
        lines = [user("From now on always use 2-space indent. Restyle the header in site.css."),
                 call("Edit", file_path="site.css")]
        self.assertEqual(decide(lines, ".")[0], "verify")
        sent = lines + [user("Stop hook feedback:\nBosskuAI verify gate: you changed code but have not run anything yet.", meta=True)]
        self.assertEqual(decide(sent, ".")[0], "rule")
        again = sent + [user("Stop hook feedback:\nBosskuAI memory gate: save it", meta=True)]
        self.assertIsNone(decide(again, "."))

    def test_only_a_real_bossku_remember_call_counts_as_saved(self):
        def saved(command):
            return decide([user(RULE), call("Bash", command=command)], ".") is None
        self.assertTrue(saved('bossku remember --project . --kind decision "tuples"'))
        self.assertTrue(saved('cd proj && bossku.exe  remember --kind decision "tuples"'))
        self.assertTrue(saved('"C:/tools/bossku.EXE" remember --kind decision "tuples"'))
        self.assertFalse(saved('grep -n "bossku remember" AGENTS.md'))
        self.assertFalse(saved('echo bossku remember'))
        self.assertFalse(saved('bossku remember --project . --kind decision "<the rule as the user stated it, and why>"'))

    def test_odd_payloads_and_transcripts_stay_silent(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "t.jsonl"
            path.write_text("\n".join([
                event(type="user", message="a plain string"),
                event(type="user", message=[1, 2]),
                event(type="assistant", message={"content": [{"type": "tool_use", "name": ["Edit"], "input": "x"}]}),
                event(type="assistant", message={"content": [{"type": "tool_use", "name": "Bash", "input": [1]}]}),
            ]), encoding="utf-8")
            for payload in ({"transcript_path": 5}, {"transcript_path": ["a"]}, {"transcript_path": "bad\0path"},
                            {"transcript_path": str(path)}, {"transcript_path": str(path), "cwd": 7}, [], 3):
                with self.subTest(payload=str(payload)[:40]):
                    self.assertIsInstance(gate_output(json.dumps(payload)), dict)
        self.assertEqual(gate_output("[" * 100000), {})

    def test_the_hook_commands_never_exit_with_an_error_code(self):
        for command, target in (("verify-gate", "bossku.cli.gate_output"), ("skill-hint", "bossku.cli.hook_output")):
            with self.subTest(command=command), mock.patch(target, side_effect=RuntimeError("boom")), \
                    mock.patch("sys.stdin", io.StringIO("{}")), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(main([command]), 0)


class RuleCueRobustnessTests(unittest.TestCase):
    def test_a_trailing_question_does_not_cancel_a_rule_stated_before_it(self):
        self.assertTrue(states_rule("From now on always use tabs. Understood?"))
        self.assertTrue(states_rule("Starting today we never use eval in this repo. Got it?"))
        self.assertFalse(states_rule("Does our style guide say we should always use arrow functions?"))

    def test_curly_apostrophes_are_read_like_straight_ones(self):
        for text in ("Don\u2019t ever use eval. Fix the parser.", "We\u2019ve decided to use cents. Fix the total.",
                     "That\u2019s the rule: no raw SQL. Fix the query."):
            with self.subTest(text=text):
                self.assertTrue(states_rule(text))

    def test_ordinary_requests_that_share_a_word_with_a_cue_are_not_rules(self):
        for text in (
            "Add a Content-Security-Policy header to the response in server.js",
            "The console says the page violates the following Content Security Policy directive: script-src",
            "Search the whole codebase for TODO comments and list them",
            "Rename fetchUser to getUser across the codebase",
            "Delete everything in the build folder and rebuild it",
            "Now we can run all the tests and see what breaks",
            "We only need the first 10 results from the endpoint",
            "Check any PR that touches the auth module and summarise it",
            "Write a loop that updates the total for each new row",
            "Create an IAM policy that denies s3:DeleteObject on the logs bucket",
            "It's a hard requirement that the page loads in under 2 seconds. Profile it.",
        ):
            with self.subTest(text=text[:50]):
                self.assertFalse(states_rule(text))

    def test_long_runs_of_blank_lines_are_scanned_in_linear_time(self):
        import time
        start = time.perf_counter()
        for text in ("a" + "\n" * 5990 + "b", "a" + "\r\n" * 2990 + "b", "." + " " * 5990 + "decided"):
            states_rule(text)
        self.assertLess(time.perf_counter() - start, 0.5)

    def test_the_project_folder_cannot_inject_shell_syntax(self):
        for folder in ("/home/u/proj$(echo INJECTED)", "/home/u/a`echo BT`b", "/home/u/my$HOME", '/home/u/a"b',
                       "C:\\Users\\me\\$work"):
            with self.subTest(folder=folder):
                command = save_command(folder)
                self.assertIn(" --project '", command)      # one literal word in bash and in PowerShell
                self.assertNotIn('--project "', command)
        self.assertIn("--project '/home/u/proj$(echo INJECTED)'", save_command("/home/u/proj$(echo INJECTED)"))
        self.assertIn("--project .", save_command("/home/u/it's"))
        self.assertIn("--project .", save_command("/home/u/a\nb"))


class RuleHintTests(unittest.TestCase):
    def test_the_prompt_hook_points_out_a_stated_rule_even_without_a_skill_hint(self):
        out = hook_output(json.dumps({"prompt": RULE, "cwd": "C:/proj"}))
        context = out["hookSpecificOutput"]["additionalContext"]
        self.assertIn("state a rule", context)
        self.assertIn("--project 'C:/proj'", context)

    def test_an_ordinary_prompt_gets_no_rule_reminder(self):
        out = hook_output(json.dumps({"prompt": "thanks!", "cwd": "C:/proj"}))
        self.assertEqual(out, {})


if __name__ == "__main__":
    unittest.main()
