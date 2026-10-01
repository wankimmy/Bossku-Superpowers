import tempfile
import unittest
from pathlib import Path

from scripts.benchmark_routing import (
    baseline_documents, baseline_rank, comparable, load_corpus, selection_outcome, summarize,
)


class RoutingBenchmarkTests(unittest.TestCase):
    def test_duplicate_prompts_union_defensible_answers_and_provenance(self):
        with tempfile.TemporaryDirectory() as tmp:
            corpus = Path(tmp) / 'routing.py'
            corpus.write_text(
                "ROUTING_CASES = [('same prompt', {'alpha'})]\n"
                "REVIEW_ROUTING_CASES = [('same prompt', {'beta'}), ('other', {'gamma'})]\n"
                "raise AssertionError('the benchmark must not execute the test module')\n",
                encoding='utf-8',
            )
            cases = load_corpus(corpus)
        self.assertEqual(len(cases), 2)
        self.assertEqual(cases[0]['expected'], ['alpha', 'beta'])
        self.assertEqual(cases[0]['sources'], ['ROUTING_CASES', 'REVIEW_ROUTING_CASES'])

    def test_baseline_ignores_triggers_exclusions_and_body_keywords(self):
        entries = {
            'alpha': {
                'description': 'Useful for invoices',
                'triggers': ['zebra'],
                'keywords': ['zebra'],
                'exclusions': ['invoice'],
            },
            'beta': {'description': 'Useful for zebra research'},
            'x402': {'description': 'zebra'},
        }
        documents, weights = baseline_documents(entries)
        self.assertNotIn('x402', documents)
        self.assertNotIn('zebra', documents['alpha'])
        self.assertEqual(baseline_rank('zebra', documents, weights)[0][0], 'beta')
        self.assertEqual(baseline_rank('invoices', documents, weights)[0][0], 'alpha')

    def test_ties_are_stable_and_skill_ids_are_baseline_terms(self):
        entries = {'beta': {'description': 'same topic'}, 'alpha': {'description': 'same topic'}}
        documents, weights = baseline_documents(entries)
        self.assertEqual([sid for sid, _ in baseline_rank('topic', documents, weights)], ['alpha', 'beta'])
        self.assertEqual(baseline_rank('beta', documents, weights)[0][0], 'beta')

    def test_metrics_do_not_confuse_top_three_with_primary_accuracy(self):
        rows = [
            {'method': {'top1_hit': True, 'top3_hit': True}},
            {'method': {'top1_hit': False, 'top3_hit': True}},
            {'method': {'top1_hit': False, 'top3_hit': False}},
        ]
        result = summarize(rows, 'method')
        self.assertEqual(result['cases'], 3)
        self.assertEqual(result['top1_hits'], 1)
        self.assertEqual(result['top3_hits'], 2)
        self.assertEqual(result['top1_percent'], 33.33)
        self.assertEqual(result['top3_percent'], 66.67)

    def test_snapshot_check_ignores_commit_metadata_but_not_changed_routing_inputs(self):
        first = {'source': {'git_revision': 'old', 'routing_inputs_sha256': 'same'}, 'python_version': '3.11'}
        second = {'source': {'git_revision': 'new', 'routing_inputs_sha256': 'same'}, 'python_version': '3.12'}
        self.assertEqual(comparable(first), comparable(second))
        second['source']['routing_inputs_sha256'] = 'changed'
        self.assertNotEqual(comparable(first), comparable(second))

    def test_user_only_route_requires_deferral_and_cannot_count_automatic_loading(self):
        entries = {'command': {'user_invoked': True}, 'cofounder': {}}
        selection = {'primary': 'cofounder', 'selected': [{'skill_id': 'cofounder'}],
                     'deferred': [{'skill_id': 'command', 'reason': 'requires user invocation'}]}
        self.assertTrue(selection_outcome(selection, ['command'], entries)['hit'])
        selection['selected'].append({'skill_id': 'command'})
        self.assertFalse(selection_outcome(selection, ['command'], entries)['hit'])
        selection['selected'].pop()
        selection['deferred'][0]['reason'] = 'weak match'
        self.assertFalse(selection_outcome(selection, ['command'], entries)['hit'])

    def test_model_primary_is_scored_without_accepting_an_alternative_deferral(self):
        entries = {'model': {}, 'command': {'user_invoked': True}, 'other': {}}
        selection = {'primary': 'other', 'selected': [{'skill_id': 'other'}],
                     'deferred': [{'skill_id': 'command', 'reason': 'requires user invocation'}]}
        self.assertFalse(selection_outcome(selection, ['command', 'model'], entries)['hit'])
        selection['primary'] = 'model'
        selection['selected'] = [{'skill_id': 'model'}]
        self.assertTrue(selection_outcome(selection, ['command', 'model'], entries)['hit'])


if __name__ == '__main__':
    unittest.main()
