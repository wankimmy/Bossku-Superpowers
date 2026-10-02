import json
import unittest

from bossku.gate import decide
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
        self.assertIn('--project "C:/work/proj"', command)
        self.assertIn("bossku remember", command)
        self.assertIn("call the Bash tool now", stop_reminder("."))


class RuleGateTests(unittest.TestCase):
    def test_a_stated_rule_that_was_not_saved_gets_one_reminder_with_the_command(self):
        lines = [user(RULE), call("Write", file_path="tickets.py"), call("Bash", command="python -m unittest")]
        kind, reason = decide(lines, "C:/proj")
        self.assertEqual(kind, "rule")
        self.assertIn('bossku remember --project "C:/proj"', reason)
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


class RuleHintTests(unittest.TestCase):
    def test_the_prompt_hook_points_out_a_stated_rule_even_without_a_skill_hint(self):
        out = hook_output(json.dumps({"prompt": RULE, "cwd": "C:/proj"}))
        context = out["hookSpecificOutput"]["additionalContext"]
        self.assertIn("state a rule", context)
        self.assertIn('--project "C:/proj"', context)

    def test_an_ordinary_prompt_gets_no_rule_reminder(self):
        out = hook_output(json.dumps({"prompt": "thanks!", "cwd": "C:/proj"}))
        self.assertEqual(out, {})


if __name__ == "__main__":
    unittest.main()
