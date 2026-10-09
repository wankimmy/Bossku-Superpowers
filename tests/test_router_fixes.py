import io
import json
import math
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest import mock

from bossku import hint, index, skills
from bossku.index import load_index, singular, tokenize, write_index
from bossku.skills import _request_fit, find_skill, rank_skills, resolve_skill_id, select_skill_stack

ROOT = Path(__file__).resolve().parents[1]

FIVE_CLAUSES = ("add a login page with remember me, then write tests first, and also review the diff before i merge, "
                "and speed up the docker build; design the database table")
STRONG = "Please audit my website for SEO issues such as missing title tags and meta descriptions"
WEAK = "Implement count_inversions(nums) in inversions.py and make it fast for large lists of numbers please"


def counting_fingerprint():
    calls = []
    real = index.skills_fingerprint

    def wrapper(root=None):
        calls.append(root)
        return real(root)

    return calls, mock.patch("bossku.index.skills_fingerprint", side_effect=wrapper)


class OneFingerprintPerLookupTests(unittest.TestCase):
    """Hashing every SKILL.md costs ~60 ms; a lookup must pay for it once, not once per clause and per call."""

    def test_selecting_a_five_clause_prompt_hashes_the_skills_once(self):
        calls, patched = counting_fingerprint()
        with patched:
            select_skill_stack(FIVE_CLAUSES, ROOT)
        self.assertEqual(len(calls), 1)

    def test_ranking_and_finding_hash_the_skills_once(self):
        for lookup in (lambda: rank_skills(FIVE_CLAUSES, ROOT), lambda: find_skill(FIVE_CLAUSES, ROOT)):
            calls, patched = counting_fingerprint()
            with patched:
                lookup()
            self.assertEqual(len(calls), 1)

    def test_a_caller_that_holds_the_index_never_hashes(self):
        data = load_index(ROOT)
        calls, patched = counting_fingerprint()
        with patched:
            rank_skills(STRONG, ROOT, data=data)
            find_skill(STRONG, ROOT, data=data)
            select_skill_stack(STRONG, ROOT, data=data)
        self.assertEqual(calls, [])

    def test_a_hint_hashes_the_skills_once(self):
        calls, patched = counting_fingerprint()
        with patched:
            self.assertIsNotNone(hint.build_hint(STRONG, root=ROOT, home=ROOT))
        self.assertEqual(len(calls), 1)

    def test_aliases_are_read_once_per_selection(self):
        data = load_index(ROOT)     # the fingerprint also lists skills through load_aliases; leave it out of the count
        with mock.patch("bossku.skills.load_aliases", wraps=skills.load_aliases) as load:
            select_skill_stack("use bosskuai-caveman and python-testing for this task", ROOT, data=data)
        self.assertEqual(load.call_count, 1)

    def test_resolving_with_a_given_alias_map_follows_chains_and_survives_cycles(self):
        self.assertEqual(resolve_skill_id("a", ROOT, {"a": "b", "b": "c"}), "c")
        self.assertIn(resolve_skill_id("a", ROOT, {"a": "b", "b": "a"}), {"a", "b"})
        self.assertEqual(resolve_skill_id("bosskuai-caveman", ROOT), "bosskuai-token-saver")


class HintGateTests(unittest.TestCase):
    def test_a_weak_prompt_stops_before_the_full_selection(self):
        with mock.patch("bossku.hint.select_skill_stack", side_effect=AssertionError("selection should not run")):
            self.assertIsNone(hint.build_hint(WEAK, root=ROOT, home=ROOT))

    def test_a_strong_prompt_still_gets_its_hint_through_the_gate(self):
        with mock.patch("bossku.hint.select_skill_stack", wraps=select_skill_stack) as select:
            text = hint.build_hint(STRONG, root=ROOT, home=ROOT)
        self.assertEqual(select.call_count, 1)
        self.assertIn("BosskuAI skill hint", text)


def old_request_fit(task, entries):
    """The request-fit model as it was parsed before the lookup rewrite: every posting turned into a dict up front."""
    counts = {sid: {w: int(c) for w, _, c in (item.partition(":") for item in entry["qterms"].split())}
              for sid, entry in entries.items() if entry.get("qterms")}
    lengths = {sid: sum(c.values()) for sid, c in counts.items()}
    average = sum(lengths.values()) / max(len(lengths), 1)
    df = {}
    for c in counts.values():
        for w in c:
            df[w] = df.get(w, 0) + 1
    idf = {w: math.log(1 + (len(counts) - f + 0.5) / (f + 0.5)) for w, f in df.items()}
    if not counts:
        return {}
    k1, b = skills._BM25_K1, skills._BM25_B
    words = list(dict.fromkeys(singular(t) for t in tokenize(task)))
    norm = sum(idf.get(w, 0.0) for w in words) * (k1 + 1) or 1.0
    fit = {}
    for sid, tf in counts.items():
        total = 0.0
        for w in words:
            f = tf.get(w)
            if f:
                total += idf[w] * f * (k1 + 1) / (f + k1 * (1 - b + b * lengths[sid] / average))
        if total:
            fit[sid] = total / norm
    best = max(fit.values(), default=0.0)
    return {sid: value / best for sid, value in fit.items()} if best else fit


class RequestFitLookupTests(unittest.TestCase):
    def test_scores_match_the_full_parse_exactly_on_the_shipped_index(self):
        entries = load_index(ROOT)["skills"]
        for prompt in (STRONG, WEAK, FIVE_CLAUSES, "why is jest hanging after tests finish",
                       "app barely gets downloads on Play Store, why?", "qwerty zxcvb", "tests tests testing"):
            with self.subTest(prompt=prompt):
                self.assertEqual(_request_fit(prompt, entries, ""), old_request_fit(prompt, entries))

    def test_a_word_only_counts_where_it_stands_alone(self):
        entries = {"a": {"qterms": "latest:3 testing:1"}, "b": {"qterms": "test:2 c++:4"}, "c": {"qterms": "x:1"}}
        for prompt in ("test", "the latest test of c++", "latest", "testing"):
            with self.subTest(prompt=prompt):
                self.assertEqual(_request_fit(prompt, entries, ""), old_request_fit(prompt, entries))
        self.assertEqual(set(_request_fit("test", entries, "")), {"b"})

    def test_a_request_looks_up_only_its_own_words(self):
        entries = load_index(ROOT)["skills"]
        skills._request_models.pop("lookup-test", None)
        try:
            _request_fit("why is jest hanging", entries, "lookup-test")
            *_, postings = skills._request_models["lookup-test"]
        finally:
            skills._request_models.pop("lookup-test", None)
        self.assertLessEqual(set(postings), set(tokenize("why is jest hanging")))
        self.assertGreater(len(entries), 100)


class StaleIndexNoticeTests(unittest.TestCase):
    def setUp(self):
        skills._stale_noted.clear()

    def _repo_with_stale_index(self, tmp):
        root = Path(tmp)
        skill = root / "skills" / "bosskuai-sample" / "SKILL.md"
        skill.parent.mkdir(parents=True)
        skill.write_text("---\nname: bosskuai-sample\ndescription: Use when inspecting apples.\n---\n", encoding="utf-8")
        write_index(root)
        skill.write_text("---\nname: bosskuai-sample\ndescription: Use when inspecting bananas.\n---\n", encoding="utf-8")
        return root

    def test_skills_find_says_once_that_it_routed_on_a_fresh_build(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._repo_with_stale_index(tmp)
            err = io.StringIO()
            with redirect_stderr(err):
                self.assertEqual(find_skill("inspecting bananas", root)[0], "bosskuai-sample")
                find_skill("inspecting bananas", root)
            lines = err.getvalue().splitlines()
        self.assertEqual(len(lines), 1)
        self.assertIn("skills/skill-index.json is stale", lines[0])
        self.assertIn("bossku skills index", lines[0])

    def test_a_fresh_or_missing_index_is_silent(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill = root / "skills" / "bosskuai-sample" / "SKILL.md"
            skill.parent.mkdir(parents=True)
            skill.write_text("---\nname: bosskuai-sample\ndescription: Use when inspecting apples.\n---\n", encoding="utf-8")
            err = io.StringIO()
            with redirect_stderr(err):
                find_skill("inspecting apples", root)     # no saved index yet
                write_index(root)
                find_skill("inspecting apples", root)
        self.assertEqual(err.getvalue(), "")

    def test_the_prompt_hook_keeps_reading_the_saved_index_and_stays_silent(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._repo_with_stale_index(tmp)
            err = io.StringIO()
            calls, patched = counting_fingerprint()
            with redirect_stderr(err), patched:
                hint.hook_output(json.dumps({"prompt": "please inspect the apples in the orchard today", "cwd": tmp}),
                                 root=root, home=root)
        self.assertEqual(err.getvalue(), "")
        self.assertEqual(calls, [])     # the hook never hashes the skills, so it cannot know the index is stale


class LazyImportTests(unittest.TestCase):
    def test_gzip_is_loaded_only_when_the_index_is_written(self):
        code = "import sys, bossku.hint; print('gzip' in sys.modules)"
        out = subprocess.run([sys.executable, "-c", code], cwd=ROOT, capture_output=True, text=True, check=True)
        self.assertEqual(out.stdout.strip(), "False")


if __name__ == "__main__":
    unittest.main()
