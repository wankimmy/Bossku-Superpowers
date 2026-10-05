import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from scripts.benchmark_rules import kept_messages, prepare, score, wilson


class RuleBenchmarkTests(unittest.TestCase):
    def folder(self, tmp: str) -> Path:
        d = Path(tmp)
        (d / 'pos-a.json').write_text(json.dumps(['From now on always use tabs. Fix the header.', 'Plain request one']), encoding='utf-8')
        (d / 'pos-b.json').write_text(json.dumps(['We never use eval in this repo. Fix the parser.']), encoding='utf-8')
        (d / 'neg-a.json').write_text(json.dumps(['Why does parse_line return None?', 'Thanks!']), encoding='utf-8')
        (d / 'neg-b.json').write_text(json.dumps(['Add a retry wrapper to the client.']), encoding='utf-8')
        return d

    def test_prepare_hides_the_intended_label_from_the_labellers(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = self.folder(tmp)
            self.assertEqual(prepare(d), 6)
            audit = json.loads((d / 'audit-0.json').read_text(encoding='utf-8')) + json.loads((d / 'audit-1.json').read_text(encoding='utf-8'))
            self.assertEqual(len(audit), 6)
            self.assertTrue(all(set(item) == {'id', 'text'} for item in audit))

    def test_only_messages_where_labeller_and_writer_agree_are_scored(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = self.folder(tmp)
            prepare(d)
            key = json.loads((d / 'key.json').read_text(encoding='utf-8'))
            labels = {str(n): r['label'] for n, r in enumerate(key)}
            labels[str(next(n for n, r in enumerate(key) if r['text'] == 'Plain request one'))] = 0   # the labeller disagrees
            (d / 'labels-0.json').write_text(json.dumps(labels), encoding='utf-8')
            agreed, total = kept_messages(d)
            self.assertEqual((len(agreed), total), (5, 6))
            with contextlib.redirect_stdout(io.StringIO()):
                result = score(d)
            self.assertEqual((result['rules'], result['caught'], result['non_rules'], result['flagged']), (2, 2, 3, 0))

    def test_the_interval_is_wide_for_few_messages(self):
        lo, hi = wilson(3, 10)
        self.assertLess(lo, 0.3)
        self.assertGreater(hi, 0.3)


if __name__ == '__main__':
    unittest.main()
