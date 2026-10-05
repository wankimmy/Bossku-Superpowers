import gzip
import json
import tempfile
import unittest
from pathlib import Path

from bossku import skills
from bossku.hint import MIN_TOP_SCORE, build_hint
from bossku.index import QUERY_SOURCE, _query_terms
from bossku.skills import _request_fit, rank_skills

ROOT = Path(__file__).resolve().parents[1]


def entries(**texts):
    return {sid: {"qterms": text} for sid, text in texts.items()}


class RequestFitTests(unittest.TestCase):
    def test_the_best_fitting_skill_scores_one_and_the_rest_less(self):
        index = entries(a="jest:4 hang:3 finish:2", b="invoice:5 pdf:2", c="test:2 hang:1")
        fit = _request_fit("why does jest hang after the tests finish", index, "")
        self.assertEqual(max(fit.values()), 1.0)
        self.assertEqual(max(fit, key=fit.get), "a")
        self.assertNotIn("b", fit)

    def test_a_request_that_fits_nothing_pushes_nothing(self):
        self.assertEqual(_request_fit("qwerty zxcvb", entries(a="jest:4 hang:3"), ""), {})

    def test_an_index_without_request_words_is_still_usable(self):
        self.assertEqual(_request_fit("anything at all", {"a": {}, "b": {"qterms": ""}}, ""), {})

    def test_the_words_people_use_find_a_skill_that_never_says_them(self):
        top = lambda q: [sid for sid, _ in rank_skills(q, ROOT, limit=3)]
        self.assertIn("aso", top("app barely gets downloads on Play Store, why?"))
        self.assertTrue({"systematic-debugging", "bosskuai-diagnose-loop"} & set(top("why is jest hanging after tests finish")))
        self.assertIn("graft", top("where is the auth middleware called from?"))

    def test_hyphenated_trigger_phrases_count_as_phrases(self):
        self.assertEqual(rank_skills("micro-interactions for the settings page", ROOT, limit=1)[0][0], "animate")


class QueryTermTests(unittest.TestCase):
    def test_words_found_in_most_skills_are_dropped_and_the_distinctive_ones_kept(self):
        data = {f"s{i}": [f"please help with thing{i} thing{i}", "please help with the usual"] for i in range(10)}
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / QUERY_SOURCE
            target.parent.mkdir(parents=True)
            target.write_bytes(gzip.compress(json.dumps(data).encode()))
            terms = _query_terms(Path(tmp))
        self.assertEqual(set(terms), set(data))
        self.assertIn("thing3:2", terms["s3"].split())
        self.assertNotIn("please", terms["s3"])      # in every skill: says nothing about any
        self.assertNotIn("help:", terms["s3"])

    def test_a_missing_or_broken_file_gives_no_terms(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(_query_terms(Path(tmp)), {})
            target = Path(tmp) / QUERY_SOURCE
            target.parent.mkdir(parents=True)
            target.write_bytes(b"not gzip")
            self.assertEqual(_query_terms(Path(tmp)), {})


class HintConfidenceTests(unittest.TestCase):
    def test_a_weak_match_gets_no_hint(self):
        weak = "Implement count_inversions(nums) in inversions.py and make it fast for large lists of numbers please"
        self.assertLess(rank_skills(weak, ROOT, limit=1)[0][1], MIN_TOP_SCORE)
        self.assertIsNone(build_hint(weak, root=ROOT, home=ROOT))


if __name__ == "__main__":
    unittest.main()
