"""Evidence-based hint coverage and quiet-prompt safeguards.

Both modes use task evidence instead of the old score/word-count gates.
Concrete short tasks and repeated defects can receive hints. Generic follow-ups and trivia stay quiet.
The hook builds the idf table once per prompt and skips empty concern clauses.

Nothing here reads the test half of prompts.json, fresh.json or trivial.json for its answers: those are decision data.
The quiet prompts below were written for this file. Nothing touches the real home: every home is a temp folder.
"""

import contextlib
import gc
import json
import os
import shutil
import sys
import tempfile
import unittest
import weakref
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import bossku.index as bossku_index  # noqa: E402
import bossku.skills as skills  # noqa: E402
from bossku import hint  # noqa: E402
from bossku.hint import hook_output, pick_skills  # noqa: E402
from bossku.index import load_index  # noqa: E402
from bossku.memory import save_user_config  # noqa: E402
from scripts import benchmark_routing_heldout as heldout  # noqa: E402

PROMPTS = ROOT / "benchmarks" / "routing-heldout" / "prompts.json"

# Follow-ups, trivia, chit-chat and short pings. Hand-written for this file; none comes from the decision sets.
FOLLOW_UPS = [
    "yes go ahead and do that please", "ok that looks good, thanks for the quick turnaround",
    "can you explain what that last change does exactly", "no, I meant the other file, not this one",
    "try again but keep the same format as before", "why did you pick that approach instead of the simpler one",
    "great, now do the same for the other two files", "what does that error message actually mean in plain words",
    "show me the diff again so I can read it slowly", "undo the last edit and put it back how it was",
    "sounds good, go for it and tell me when it is done", "wait, can you make that shorter and a bit friendlier",
    "thanks, that fixed it, you can stop there",
    "ok continue with the next step whenever you are ready", "can you run it one more time and show me the output",
    "yes please, and keep the names the way they are now", "not quite, the second part is still wrong",
    "that is fine, just leave the rest as it is", "good, now rename it to something clearer",
    "boleh tolong terangkan sikit lagi pasal tu", "ok cantik, teruskan macam tu je",
    "lepas ni apa pula yang kita kena buat", "betul tu, tapi tukar warna dia sikit",
    "ya boleh, buat yang kedua pula", "takpe, biar je macam tu dulu",
    "ok lah, tolong ringkaskan balik apa yang awak buat tadi", "eh tunggu, yang tadi tu salah la sebenarnya",
    "yeah that works, now add a short comment above it", "also, can you double check the last paragraph for typos",
    "and what about the other case we talked about earlier", "ok so what should I do first, then",
    "right, so that means we keep it as is, correct", "perfect, send me the final version when you can",
    "one more thing, make the title a little bit bigger", "can you summarise what we decided so far in two lines",
    "do you think that is enough or should we change more", "great work, let me look at it and come back to you",
    "ok but why is it slower than before then", "fine, use your best judgement on the rest",
    "that last output you gave me looks good but can you also explain why you chose a dictionary there instead of a list",
    "ok I read through what you wrote and it makes sense, so please go ahead and apply the same idea to the remaining two sections",
    "thanks for the explanation, I think I understand now, but could you give me one more example using a different kind of input",
    "yes that is what I meant, please carry on with the rest of the list and let me know if anything looks odd to you",
    "sorry for the confusion earlier, I actually wanted the shorter version you gave me first, the one before the long explanation",
    "boleh tak awak sambung balik apa yang kita bincang tadi, saya rasa kita dah sampai separuh jalan tapi saya lupa bahagian akhir",
    "okay so after thinking about it more I want to keep the first option you suggested, so please drop the other two from the list",
    "I just want to double check that I understood your last message correctly, you said the second one is the safer choice, right",
    "that works for me, please keep the same tone and length as the previous answer and just change the example at the end",
    "good job on the last step, now let us pause here for today and pick this up again tomorrow morning when I am back at my desk",
    "please remind me what we agreed on in the earlier part of this conversation, I want to be sure before I move on to the next part",
    "interesting, I did not know that, is it also true for the other cases we looked at before or only for the first one",
    "no worries about that, it was a small thing and I can fix it myself later, let us just move on to whatever comes next",
    "right, that all sounds reasonable to me, so unless you see a problem I would say we are done with this part for now",
    "that was a very helpful answer overall, thank you, I will read it again slowly and come back if I have more questions later",
]
TRIVIAL = [
    "what is the capital city of Australia", "how many days are there until the end of the year",
    "what does HTTP stand for in simple terms", "tell me a short joke about cats and dogs",
    "convert 70 kilometres per hour into miles per hour", "who wrote the novel Pride and Prejudice",
    "give me a synonym for the word happy", "how do you say thank you in Malay", "what is seventeen times twenty three",
    "is a tomato a fruit or a vegetable", "what is the difference between affect and effect",
    "berapa lama nak drive dari KL ke Penang", "apa maksud idempotent dalam bahasa mudah",
    "what year did the second world war end", "spell the word necessary for me slowly",
    "which planet is the biggest in our solar system", "what time is it in Tokyo when it is noon in London",
    "good morning, hope you are doing well today", "hello there, are you available to help me",
    "what is the longest river in the world", "what is a haiku and how many syllables does it have",
    "what is the tallest building in the world right now", "describe the taste of durian to someone who never had it",
    "tell me a fun fact about the number seven", "lol that is funny, tell me another one",
    "translate good morning into Malay and Tamil", "kenapa langit warna biru pada waktu siang",
    "how do people usually decide between renting and buying a home when they are in their early thirties and have some savings",
    "what do you think is the most important thing to remember when learning to cook for the first time on your own at home",
    "can you recommend a good hawker stall near Petaling Jaya for dinner tonight, somewhere that is also fine for kids and older parents",
    "I was reading about how volcanoes form and got curious, how long does it usually take for a new island to appear above the water",
    "tell me a bedtime story about a small turtle who is afraid of the dark and learns to love the night sky",
    "kalau saya nak belajar bahasa Jepun dari awal, apa langkah pertama yang paling mudah dan tak membosankan untuk orang yang sibuk",
]
SHORT_PINGS = [
    "thanks a lot", "ok sounds good", "looks good to me", "what time is it", "do it again",
    "yes please do", "go ahead then", "terima kasih banyak", "hello how are you", "show me again", "fix this please",
    "what is next", "try it again", "undo that change", "commit it now", "push the changes", "make it two lines",
    "explain that again", "who are you", "thanks, that works", "ok do that", "good evening to you", "ya betul tu",
    "run it again", "what happened there", "continue please", "keep going", "show the diff", "revert that",
    "capital of Peru", "tell me a riddle", "nice one", "same again please", "check the logs",
    "restart the server", "why did that fail", "list the files", "open the readme",
]


@contextlib.contextmanager
def clean_env():
    with mock.patch.dict(os.environ):
        for name in ("CLAUDE_PROJECT_DIR", hint.NONCE_ENV):
            os.environ.pop(name, None)
        yield


class ConstantsTests(unittest.TestCase):
    def test_both_modes_keep_the_bounded_hint_contract(self):
        self.assertEqual(hint.MAX_HINTS, 3)
        self.assertEqual(hint.MODES, ('v1', 'v2'))
        self.assertEqual(hint.HINT_CHARS, 800)


class QuietPromptTests(unittest.TestCase):
    """Chit-chat, trivia, follow-ups and short pings get no hint, in either mode."""

    @classmethod
    def setUpClass(cls):
        cls.data = load_index(ROOT)

    def test_every_quiet_prompt_stays_silent(self):
        loud = {}
        for prompt in [*FOLLOW_UPS, *TRIVIAL, *SHORT_PINGS]:
            for mode in ("v1", "v2"):
                picks = pick_skills(prompt, root=ROOT, mode=mode, data=self.data)
                if picks:
                    loud[(mode, prompt)] = [item["skill_id"] for item in picks]
        self.assertEqual(loud, {})

    def test_short_work_and_repeated_defects_are_tasks_not_quiet_pings(self):
        for prompt, expected in (
            ('run the tests', {'verification-before-completion'}),
            ('add more tests', {'bosskuai-tdd-loop', 'test-driven-development'}),
            ('hmm that did not work, I still get the same error', {'bosskuai-diagnose-loop', 'systematic-debugging'}),
        ):
            for mode in ('v1', 'v2'):
                ids = {r['skill_id'] for r in pick_skills(prompt, root=ROOT, mode=mode, data=self.data)}
                self.assertTrue(ids & expected, (prompt, mode, ids))

    def test_the_quiet_set_is_not_a_copy_of_the_decision_sets(self):
        decision = set()
        for name in ("fresh", "trivial"):
            decision |= {item["prompt"] for item in json.loads(
                (ROOT / "benchmarks" / "routing-heldout" / f"{name}.json").read_text(encoding="utf-8"))}
        held_out = json.loads(PROMPTS.read_text(encoding="utf-8"))
        decision |= {item["prompt"] for item in held_out if heldout.split_of(item["id"]) == "test"}
        self.assertEqual(decision & {*FOLLOW_UPS, *TRIVIAL, *SHORT_PINGS}, set())


class EverydayRequestTests(unittest.TestCase):
    """Requests worded as a need, a question or a soft verb still route; one shared word adds no skill.

    Written for this file from prompts typed in a Claude Code session, not taken from the decision sets.
    """

    @classmethod
    def setUpClass(cls):
        cls.data = load_index(ROOT)

    def ids(self, prompt):
        return [r["skill_id"] for r in pick_skills(prompt, root=ROOT, data=self.data)]

    def test_soft_wording_with_two_subject_words_routes(self):
        for prompt, expected in (
            ("add stripe subscription billing", "bosskuai-saas-billing-ops"),
            ("make the dashboard responsive on mobile", "bosskuai-ui-ux-design-to-code"),
        ):
            with self.subTest(prompt=prompt):
                self.assertIn(expected, self.ids(prompt))

    def test_one_shared_word_does_not_add_a_second_skill(self):
        self.assertNotIn("bosskuai-software-architecture", self.ids("write unit tests for the cart service"))
        self.assertEqual(self.ids("fix the login bug, users get 500 after submit"), ["bosskuai-diagnose-loop"])

    def test_plain_react_is_not_an_expo_task(self):
        self.assertNotIn("bosskuai-expo-react-native", self.ids("why my react state not updating"))

    def test_a_skill_named_with_spaces_is_an_explicit_request_only_when_asked_for(self):
        self.assertEqual(self.ids("use the mysql patterns skill to check replica lag"), ["mysql-patterns"])
        self.assertEqual(self.ids("I love the pricing skill you showed"), [])

    def test_an_app_notification_is_not_a_prompt(self):
        note = ("<task-notification>\n<task-id>b8p8o68cc</task-id>\n<status>completed</status>\n"
                "<summary>Background command \"Baseline routing tests in clean worktree\" completed</summary>\n"
                "</task-notification>")
        self.assertEqual(self.ids(note), [])
        self.assertEqual(self.ids("[SYSTEM NOTIFICATION - NOT USER INPUT]\n" + note), [])
        handback = ('<agent-message from="a8379bf8bda661d9d">\n[Subagent hand-back] Task B is done: the ticket '
                    'schema went into bosskuai-planning-execution and the CLI contract checks into polyglot.\n'
                    '</agent-message>')
        self.assertEqual(self.ids(handback), [])


class MultiConcernTests(unittest.TestCase):
    """The prompts of tests/test_skill_selection.py that ask for several things get one skill for each."""

    TWO = "write pytest fixtures and run Google Ads for our app"
    THREE = "write pytest fixtures and run Google Ads and audit keyboard focus"

    @classmethod
    def setUpClass(cls):
        cls.data = load_index(ROOT)

    def picks(self, prompt):
        return pick_skills(prompt, root=ROOT, mode="v2", data=self.data)

    def test_the_prompts_are_the_ones_the_selection_tests_use(self):
        source = (ROOT / "tests" / "test_skill_selection.py").read_text(encoding="utf-8")
        self.assertIn(self.TWO, source)
        self.assertIn(self.THREE, source)

    def test_two_concerns_get_two_skills_and_three_concerns_get_three(self):
        two = [item["skill_id"] for item in self.picks(self.TWO)]
        three = [item["skill_id"] for item in self.picks(self.THREE)]
        self.assertEqual(sorted(two), ["ads", "python-testing"])
        self.assertEqual(sorted(three), ["accessibility", "ads", "python-testing"])
        self.assertEqual(self.picks(self.THREE)[0]["skill_id"], "ads")

    def test_the_skills_cover_distinct_concerns(self):
        for prompt in (self.TWO, self.THREE):
            with self.subTest(prompt=prompt):
                picks = self.picks(prompt)
                self.assertTrue(2 <= len(picks) <= hint.MAX_HINTS)
                ids = [item["skill_id"] for item in picks]
                for group in skills.ALTERNATIVE_SKILLS:       # never two alternatives for the same job
                    self.assertLessEqual(len(group & set(ids)), 1)
                seen = set()
                for item in picks:                            # every pick brings a word the earlier ones did not match
                    self.assertTrue(set(item["matched_terms"]) - seen, item["skill_id"])
                    seen |= set(item["matched_terms"])

    def test_the_hook_prints_one_line_per_concern_in_v2_and_nothing_for_a_follow_up(self):
        with tempfile.TemporaryDirectory() as tmp, clean_env():
            home = Path(tmp)
            save_user_config({"hint_mode": "v2"}, home)
            for sid in ("ads", "python-testing", "accessibility"):    # listed by the host: "(Skill tool)", so the lines stay short
                (home / ".claude" / "skills" / sid).mkdir(parents=True)
                shutil.copyfile(ROOT / "skills" / sid / "SKILL.md", home / ".claude" / "skills" / sid / "SKILL.md")
            out = hook_output(json.dumps({"prompt": self.THREE, "cwd": tmp}), root=ROOT, home=home)
            text = out["hookSpecificOutput"]["additionalContext"]
            self.assertEqual(sum(line.startswith("- ") for line in text.splitlines()), 3)
            self.assertLessEqual(len(text), hint.HINT_CHARS)
            for sample in FOLLOW_UPS[:10]:
                self.assertEqual(hook_output(json.dumps({"prompt": sample, "cwd": tmp}), root=ROOT, home=home), {}, sample)


class BlankPieceTests(unittest.TestCase):
    """select_skill_stack ranks the pieces of a multi-part prompt, but not the blank gap between two separators."""

    PROMPT = "fix the login bug and pricing, then ship"      # pieces: "fix the login bug", "pricing", blank, "ship"

    @classmethod
    def setUpClass(cls):
        cls.data = load_index(ROOT)

    def test_a_blank_piece_is_never_ranked(self):
        with mock.patch.object(skills, "rank_skills", wraps=skills.rank_skills) as ranked:
            skills.select_skill_stack(self.PROMPT, ROOT, limit=3, data=self.data)
        pieces = [call.args[0].strip() for call in ranked.call_args_list if call.kwargs.get("limit") == 1]
        self.assertEqual(pieces, ["fix the login bug", "pricing", "ship"])

    def test_skipping_it_loses_nothing_because_a_blank_piece_scores_under_the_nomination_bar(self):
        for blank in ("", " ", "  " + chr(10)):
            for _, score in skills.rank_skills(blank, ROOT, limit=1, data=self.data):
                self.assertLess(score, skills.CONCERN_WINNER_MIN, repr(blank))


class Entries(list):
    """A list that can be weakly referenced, standing in for the entries of an index."""


class HookIdfTests(unittest.TestCase):
    """The hook builds the idf table once per prompt, not once per ranking, and puts the original function back."""

    def test_one_build_for_a_prompt_that_ranks_its_pieces_and_the_function_is_restored_after(self):
        prompt = MultiConcernTests.THREE
        with tempfile.TemporaryDirectory() as tmp, clean_env(), \
                mock.patch.object(bossku_index, "compute_idf", wraps=bossku_index.compute_idf) as built:
            watched = bossku_index.compute_idf
            plain = hook_output(json.dumps({"prompt": prompt, "cwd": tmp}), root=ROOT, home=Path(tmp))
            self.assertEqual(built.call_count, 1)
            self.assertIs(bossku_index.compute_idf, watched)
        with tempfile.TemporaryDirectory() as tmp, clean_env():
            self.assertEqual(hook_output(json.dumps({"prompt": prompt, "cwd": tmp}), root=ROOT, home=Path(tmp)), plain)
        self.assertIn("ads", plain["hookSpecificOutput"]["additionalContext"])

    def test_without_the_cache_the_table_is_built_for_every_ranking(self):
        with mock.patch.object(bossku_index, "compute_idf", wraps=bossku_index.compute_idf) as built:
            skills.select_skill_stack(MultiConcernTests.THREE, ROOT, limit=3, data=load_index(ROOT))
        self.assertGreater(built.call_count, 3)

    def test_a_cached_table_keeps_its_entries_alive_so_a_reused_id_cannot_return_another_table(self):
        seen = {}

        def build(prompt, **kwargs):    # stands in for build_hint: two tables, the first from short-lived entries
            first = Entries(["a"])
            seen["ref"] = weakref.ref(first)
            seen["first"] = bossku_index.compute_idf(first)
            del first
            gc.collect()
            seen["alive"] = seen["ref"]() is not None
            seen["second"] = bossku_index.compute_idf(Entries(["a", "b"]))

        # new=len, not a Mock: a Mock keeps its arguments alive and the check would pass for any cache
        with tempfile.TemporaryDirectory() as tmp, clean_env(), \
                mock.patch.object(bossku_index, "compute_idf", new=len), \
                mock.patch("bossku.hint.build_hint", side_effect=build):
            hook_output(json.dumps({"prompt": "nothing to suggest here", "cwd": tmp}), root=ROOT, home=Path(tmp))
        self.assertEqual((seen["first"], seen["second"]), (1, 2))
        self.assertTrue(seen["alive"])


if __name__ == "__main__":
    unittest.main()
