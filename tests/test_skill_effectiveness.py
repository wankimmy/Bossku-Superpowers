import json
import tempfile
import unittest
from pathlib import Path

from scripts import skill_effectiveness as se

REPO = Path(__file__).resolve().parents[1]


def row(arm, task, passed, model='m1', loaded=(), tokens=100, cost=0.1, kind='task', **extra):
    return {'kind': kind, 'arm': arm, 'task': task, 'passed': passed, 'model': model, 'skills_loaded': list(loaded),
            'skills_invoked': [], 'tokens': {'input_uncached': tokens, 'cache_read': 0, 'cache_write': 0, 'output': 0},
            'cost_usd': cost, 'infrastructure_failure': False, **extra}


def cell(rows_base, rows_arm, **kw):
    rows = [row('base', t, p) for t, p in rows_base] + [row('with', t, p) for t, p in rows_arm]
    return se.compare(rows, 'base', 'with', **kw)[0]


class ActivationTests(unittest.TestCase):
    def test_hinted_opened_acceptable_and_outside_are_separate_counts(self):
        rows = [
            row('with', 't1', True, loaded=['a'], kind='routing', concerns=[['a', 'b']]),
            row('with', 't2', True, loaded=['z'], kind='routing', concerns=[['a']]),
            row('with', 't3', False, loaded=[], kind='routing', concerns=[['a']]),
        ]
        out = se.activation(rows)[0]
        self.assertEqual((out['runs'], out['opened_any'], out['acceptable_opened'], out['only_outside_acceptable']),
                         (3, 2, 1, 1))
        self.assertIsNone(out['hint_shown'])   # rows do not record it: never guessed

    def test_task_rows_have_no_acceptable_set(self):
        out = se.activation([row('with', 't1', True, loaded=['a'])])[0]
        self.assertEqual(out['opened_any'], 1)
        self.assertIsNone(out['acceptable_opened'])
        self.assertIsNone(out['only_outside_acceptable'])

    def test_hint_count_when_the_row_records_it(self):
        out = se.activation([row('with', 't1', True, hint_shown=True), row('with', 't2', True, hint_shown=False)])[0]
        self.assertEqual(out['hint_shown'], 1)

    def test_invoked_skills_count_as_opened_and_excluded_rows_are_dropped(self):
        bad = row('with', 't2', False)
        bad['infrastructure_failure'] = True
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / 'test-m1.jsonl'
            invoked = row('with', 't1', True)
            invoked['skills_invoked'] = ['x']
            path.write_text('\n'.join(json.dumps(r) for r in (invoked, bad)), encoding='utf-8')
            out = se.activation(se.load_rows([path]))[0]
        self.assertEqual((out['runs'], out['opened_any']), (1, 1))


class CompareTests(unittest.TestCase):
    def test_paired_difference_rates_and_overhead(self):
        tasks = [f't{i}' for i in range(12)]
        rows = [row('base', t, i < 6, tokens=100, cost=0.1) for i, t in enumerate(tasks)]
        rows += [row('with', t, i < 12, tokens=150, cost=0.2) for i, t in enumerate(tasks)]
        c = se.compare(rows, 'base', 'with')[0]
        self.assertEqual(c['paired_tasks'], 12)
        self.assertEqual((c['baseline']['pass_rate'], c['arm']['pass_rate']), (0.5, 1.0))
        self.assertAlmostEqual(c['paired_difference'], 0.5)
        self.assertGreater(c['confidence_interval'][0], 0)
        self.assertAlmostEqual(c['token_overhead'], 0.5)
        self.assertAlmostEqual(c['arm']['cost_per_passed'], 0.2)
        self.assertEqual(c['sign_test_p'], 2 * 0.5 ** 6)

    def test_different_task_sets_are_refused_unless_allowed(self):
        rows = [row('base', 't1', True), row('base', 't2', True), row('with', 't1', True)]
        with self.assertRaises(ValueError):
            se.compare(rows, 'base', 'with')
        c = se.compare(rows, 'base', 'with', allow_unpaired=True)[0]
        self.assertTrue(c['unpaired'])
        self.assertEqual(c['paired_tasks'], 1)
        self.assertEqual(c['tasks_only_in_baseline'], ['t2'])

    def test_unmeasured_cost_is_null_not_zero(self):
        rows = [row('base', 't1', True, cost=None), row('with', 't1', True, cost=None)]
        c = se.compare(rows, 'base', 'with')[0]
        self.assertIsNone(c['arm']['cost_per_passed'])
        self.assertIsNone(c['arm']['cost_mean'])

    def test_days_each_arm_ran_are_reported(self):
        rows = [row('base', 't1', True, timestamp='2026-10-01T00:00:00+00:00'),
                row('with', 't1', True, timestamp='2026-10-08T00:00:00+00:00')]
        c = se.compare(rows, 'base', 'with')[0]
        self.assertEqual((c['baseline']['days'], c['arm']['days']), (['2026-10-01'], ['2026-10-08']))

    def test_record_never_takes_unpaired_cells(self):
        with self.assertRaises(SystemExit):
            se.build_parser().parse_args(['record', '--skill', 'x', '--date', 'd', '--allow-unpaired'])

    def test_missing_arm_gives_no_cell(self):
        self.assertEqual(se.compare([row('base', 't1', True)], 'base', 'with'), [])

    def test_models_and_suites_are_kept_apart(self):
        rows = [row('base', 't1', True, model='a'), row('with', 't1', True, model='a'),
                row('base', 't1', False, model='b'), row('with', 't1', True, model='b')]
        self.assertEqual([c['model'] for c in se.compare(rows, 'base', 'with')], ['a', 'b'])


class ClassifyTests(unittest.TestCase):
    N = se.MIN_PAIRED_TASKS

    def tasks(self, n):
        return [f't{i}' for i in range(n)]

    def test_minimum_is_ten(self):
        self.assertEqual(se.MIN_PAIRED_TASKS, 10)

    def test_demonstrated_improvement(self):
        t = self.tasks(self.N)
        self.assertEqual(se.classify(cell([(x, False) for x in t], [(x, True) for x in t])), 'demonstrated_improvement')

    def test_demonstrated_regression(self):
        t = self.tasks(self.N)
        self.assertEqual(se.classify(cell([(x, True) for x in t], [(x, False) for x in t])), 'demonstrated_regression')

    def test_too_few_tasks_cannot_be_demonstrated(self):
        t = self.tasks(self.N - 1)
        self.assertEqual(se.classify(cell([(x, False) for x in t], [(x, True) for x in t])),
                         'promising_insufficient_evidence')
        self.assertEqual(se.classify(cell([(x, True) for x in t], [(x, False) for x in t])),
                         'neutral_or_inconclusive')

    def test_positive_point_with_interval_across_zero_is_promising(self):
        t = self.tasks(20)
        base = [(x, i % 2 == 0) for i, x in enumerate(t)]
        arm = base[:]
        arm[1] = (t[1], True)   # one task better, nothing worse
        c = cell(base, arm)
        self.assertLessEqual(c['confidence_interval'][0], 0)
        self.assertEqual(se.classify(c), 'promising_insufficient_evidence')

    def test_ceiling_is_inconclusive_never_no_difference(self):
        t = self.tasks(20)
        label = se.classify(cell([(x, True) for x in t], [(x, True) for x in t]))
        self.assertEqual(label, 'neutral_or_inconclusive')
        self.assertNotIn('no_difference', label)

    def test_four_wins_in_twelve_is_not_demonstrated(self):
        t = self.tasks(12)
        base = [(x, False) for x in t]
        arm = [(x, i < 4) for i, x in enumerate(t)]
        c = cell(base, arm)
        self.assertGreater(c['confidence_interval'][0], 0)
        self.assertGreater(c['sign_test_p'], 0.05)
        self.assertEqual(se.classify(c), 'promising_insufficient_evidence')
        self.assertEqual(se.classify(cell(arm, base)), 'neutral_or_inconclusive')

    def test_not_tested_without_rows(self):
        self.assertEqual(se.classify(None), 'not_tested')


class RecordTests(unittest.TestCase):
    def test_measured_record_has_computed_fields_and_no_clock(self):
        t = [f't{i}' for i in range(12)]
        c = cell([(x, False) for x in t], [(x, True) for x in t])
        rec = se.make_record(c, skill_id='pack:bossku', skill_version=None, baseline_arm='base', arm='with',
                             date='2026-01-02', source_rows=['a.jsonl'], required=False)
        se.validate_record(rec)
        self.assertEqual(rec['evaluation_status'], 'demonstrated_improvement')
        self.assertEqual(rec['last_evaluated'], '2026-01-02')
        self.assertEqual(rec['sample_size'], 12)
        self.assertEqual(rec['cost_per_success'], c['arm']['cost_per_passed'])

    def test_required_flag_sets_required_safety_control(self):
        t = [f't{i}' for i in range(12)]
        rec = se.make_record(cell([(x, True) for x in t], [(x, True) for x in t]), skill_id='pack:bossku',
                             skill_version=None, baseline_arm='base', arm='with', date='d', source_rows=[],
                             required=True)
        self.assertEqual(rec['evaluation_status'], 'required_safety_control')

    def test_not_tested_record_is_all_null(self):
        rec = se.not_tested_record('minimal-fix', 'abc', '2026-01-02')
        se.validate_record(rec)
        self.assertEqual(rec['evaluation_status'], 'not_tested')
        for key in ('model', 'suite', 'sample_size', 'baseline_pass_rate', 'skill_pass_rate', 'paired_difference',
                    'confidence_interval', 'token_overhead', 'cost_per_success'):
            self.assertIsNone(rec[key], key)

    def test_validate_rejects_bad_status_and_missing_field(self):
        rec = se.not_tested_record('x', None, 'd')
        with self.assertRaises(ValueError):
            se.validate_record({**rec, 'evaluation_status': 'no_difference'})
        rec.pop('host')
        with self.assertRaises(ValueError):
            se.validate_record(rec)

    def test_skill_version_is_the_git_blob_hash(self):
        self.assertEqual(len(se.skill_blob_hash('minimal-fix')), 40)
        with self.assertRaises(ValueError):
            se.skill_blob_hash('../README')

    def test_record_path_keeps_every_part_inside_the_folder(self):
        rec = se.not_tested_record('pack:bossku', None, 'd') | {'model': '../../x/y', 'suite': 's/t', 'arm': 'with'}
        path = se.record_path(rec, Path('out'))
        self.assertEqual(path.parent, Path('out'))
        self.assertNotIn('/', path.name)
        self.assertNotIn('..' + '/', path.name)

    def test_committed_records_validate(self):
        files = sorted((REPO / 'benchmarks' / 'skill-effectiveness' / 'records').glob('*.json'))
        self.assertTrue(files)
        for path in files:
            with self.subTest(path.name):
                se.validate_record(json.loads(path.read_text(encoding='utf-8')))


class CommandLineTests(unittest.TestCase):
    def run_main(self, *argv):
        import contextlib
        import io
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = se.main(list(argv))
        return code, out.getvalue(), err.getvalue()

    def write_rows(self, d, rows, name='test-m1.jsonl'):
        (Path(d) / 'raw').mkdir(exist_ok=True)
        path = Path(d) / 'raw' / name
        path.write_text('\n'.join(json.dumps(r) for r in rows), encoding='utf-8')
        return str(path)

    def paired(self, model='m1', n=12):
        t = [f't{i}' for i in range(n)]
        return [row('base', x, False, model=model) for x in t] + [row('with', x, True, model=model) for x in t]

    def test_required_without_rows_writes_required_safety_control(self):
        with tempfile.TemporaryDirectory() as d:
            code, _, _ = self.run_main('record', '--date', '2026-11-17', '--skill', 'pack:bossku', '--required',
                                       '--out', d)
            rec = json.loads(next(Path(d).glob('*.json')).read_text(encoding='utf-8'))
        self.assertEqual(code, 0)
        self.assertEqual(rec['evaluation_status'], 'required_safety_control')
        se.validate_record(rec)

    def test_record_without_rows_writes_not_tested(self):
        with tempfile.TemporaryDirectory() as d:
            code, _, _ = self.run_main('record', '--date', '2026-11-17', '--skill', 'pack:bossku', '--out', d)
            rec = json.loads(next(Path(d).glob('*.json')).read_text(encoding='utf-8'))
        self.assertEqual((code, rec['evaluation_status']), (0, 'not_tested'))

    def test_record_with_rows_writes_a_valid_named_file(self):
        with tempfile.TemporaryDirectory() as d:
            rows = self.write_rows(d, self.paired())
            out = Path(d) / 'records'
            code, _, _ = self.run_main('record', '--date', '2026-11-17', '--skill', 'pack:bossku', '--baseline',
                                       'base', '--arm', 'with', '--out', str(out), rows)
            files = list(out.glob('*.json'))
            self.assertEqual((code, [f.name for f in files]), (0, ['pack-bossku--m1--test--with.json']))
            rec = json.loads(files[0].read_text(encoding='utf-8'))
        se.validate_record(rec)
        self.assertEqual(rec['evaluation_status'], 'demonstrated_improvement')

    def test_record_with_a_slash_in_the_model_stays_in_the_folder(self):
        with tempfile.TemporaryDirectory() as d:
            rows = self.write_rows(d, self.paired(model='open/x'), name='test-open-x.jsonl')
            out = Path(d) / 'records'
            code, _, _ = self.run_main('record', '--date', 'd', '--skill', 'pack:bossku', '--baseline', 'base',
                                       '--arm', 'with', '--out', str(out), rows)
            self.assertEqual((code, len(list(out.glob('*.json')))), (0, 1))

    def test_record_skips_unpaired_cells_and_still_writes_the_rest(self):
        rows = self.paired('m1') + [row('base', 'a', True, model='m2'), row('with', 'b', True, model='m2')]
        with tempfile.TemporaryDirectory() as d:
            path = self.write_rows(d, rows)
            out = Path(d) / 'records'
            code, _, err = self.run_main('record', '--date', 'd', '--skill', 'pack:bossku', '--baseline', 'base',
                                         '--arm', 'with', '--out', str(out), path)
            names = [f.name for f in out.glob('*.json')]
        self.assertEqual((code, len(names)), (0, 1))
        self.assertIn('m2', err)

    def test_compare_refuses_different_task_sets_unless_allowed(self):
        rows = [row('base', 't1', True), row('base', 't2', True), row('with', 't1', True)]
        with tempfile.TemporaryDirectory() as d:
            path = self.write_rows(d, rows)
            args = ('compare', '--baseline', 'base', '--arm', 'with', path)
            self.assertEqual(self.run_main(*args)[0], 1)
            code, out, _ = self.run_main(*args, '--allow-unpaired')
        self.assertEqual(code, 0)
        self.assertTrue(json.loads(out)[0]['unpaired'])


if __name__ == '__main__':
    unittest.main()
