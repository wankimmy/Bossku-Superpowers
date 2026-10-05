import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from unittest import mock

from types import SimpleNamespace

from scripts.benchmark_agent import (
    Arm, agent_command, build_report, checked_after_last_edit, child_env, diff_stats, is_infrastructure_failure,
    materialize_humaneval, parse_arm, parse_stream, parse_unittest, summarize_arm, total_input, wilson, write_shim,
)


def stream(*events):
    return '\n'.join(json.dumps(event) for event in events) + '\n'


class GradingTests(unittest.TestCase):
    def test_unittest_summary_counts_failures_and_errors(self):
        ok = parse_unittest('Ran 14 tests in 0.002s\n\nOK\n', 0)
        self.assertEqual((ok['passed'], ok['tests_total'], ok['tests_passed']), (True, 14, 14))
        bad = parse_unittest('Ran 12 tests in 0.1s\n\nFAILED (failures=2, errors=1)\n', 1)
        self.assertEqual((bad['passed'], bad['tests_total'], bad['tests_passed']), (False, 12, 9))

    def test_missing_module_is_a_failure_not_a_pass(self):
        out = parse_unittest('Ran 1 test in 0.000s\n\nFAILED (errors=1)\n', 1)
        self.assertFalse(out['passed'])
        self.assertEqual(out['tests_passed'], 0)

    def test_no_tests_run_never_counts_as_passing(self):
        self.assertFalse(parse_unittest('', 0)['passed'])

    def test_wilson_interval_is_sane(self):
        self.assertEqual(wilson(0, 0), (0.0, 0.0))
        low, high = wilson(10, 10)
        self.assertGreater(low, 0.7)
        self.assertAlmostEqual(high, 1.0, places=6)
        low, high = wilson(5, 10)
        self.assertLess(low, 0.5)
        self.assertGreater(high, 0.5)
        self.assertAlmostEqual((low + high) / 2, 0.5, delta=0.02)


class TranscriptTests(unittest.TestCase):
    def parse(self, text):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 't.jsonl'
            path.write_text(text, encoding='utf-8-sig')
            return parse_stream(path)

    def test_counts_tools_skills_and_bossku_calls_and_tokens(self):
        text = stream(
            {'type': 'system', 'subtype': 'init', 'skills': ['a', 'b', 'c'], 'tools': ['x'], 'claude_code_version': '9'},
            {'type': 'assistant', 'message': {'id': 'm1', 'content': [
                {'type': 'tool_use', 'name': 'Skill', 'input': {'skill': 'bosskuai-tdd-loop'}},
                {'type': 'tool_use', 'name': 'Bash', 'input': {'command': 'bossku skills find "x"'}},
                {'type': 'tool_use', 'name': 'Bash', 'input': {'command': 'python -m unittest'}},
                {'type': 'tool_use', 'name': 'Read', 'input': {'file_path': '/p/.claude/skills/foo/SKILL.md'}},
            ], 'usage': {'input_tokens': 1}}, 'parent_tool_use_id': None},
            {'type': 'assistant', 'message': {'id': 'm2', 'content': [{'type': 'text', 'text': 'done'}]},
             'parent_tool_use_id': None},
            {'type': 'result', 'num_turns': 2, 'total_cost_usd': 0.5, 'is_error': False, 'subtype': 'success',
             'usage': {'input_tokens': 10, 'cache_creation_input_tokens': 20, 'cache_read_input_tokens': 30,
                       'output_tokens': 5}},
        )
        parsed = self.parse(text)
        self.assertEqual(parsed['skills_invoked'], ['bosskuai-tdd-loop'])
        self.assertEqual(len(parsed['skill_files_read']), 1)
        self.assertEqual(parsed['bossku_calls'], ['bossku skills find "x"'])
        self.assertEqual(parsed['bash_calls'], 2)
        self.assertEqual(parsed['init']['skills'], 3)
        self.assertEqual(parsed['final_text'], 'done')
        self.assertEqual(total_input(parsed['tokens']), 60)
        self.assertEqual(parsed['turns'], 2)

    def test_commands_run_through_powershell_are_counted_too(self):
        text = stream({'type': 'assistant', 'message': {'id': 'm1', 'content': [
            {'type': 'tool_use', 'name': 'PowerShell', 'input': {'command': 'bossku remember --kind learning "x"'}}]}})
        parsed = self.parse(text)
        self.assertEqual(parsed['bash_calls'], 1)
        self.assertEqual(len(parsed['bossku_calls']), 1)

    def test_a_bom_and_garbage_lines_do_not_break_parsing(self):
        parsed = self.parse('﻿not json\n' + stream({'type': 'result', 'usage': {'output_tokens': 3}}))
        self.assertTrue(parsed['has_result'])
        self.assertEqual(parsed['tokens']['output'], 3)

    def test_usage_is_rebuilt_from_messages_when_the_run_never_finished(self):
        text = stream({'type': 'assistant', 'message': {'id': 'm1', 'content': [], 'usage': {
            'input_tokens': 7, 'output_tokens': 9, 'cache_read_input_tokens': 100}}})
        parsed = self.parse(text)
        self.assertFalse(parsed['has_result'])
        self.assertEqual(parsed['tokens']['output'], 9)
        self.assertEqual(parsed['tokens']['cache_read'], 100)

    def test_infrastructure_failures_are_told_apart_from_coding_failures(self):
        base = {'has_result': True, 'is_error': False, 'subtype': 'success', 'tokens': {'output': 50}}
        self.assertFalse(is_infrastructure_failure(base))
        self.assertTrue(is_infrastructure_failure({**base, 'has_result': False}))
        self.assertTrue(is_infrastructure_failure({**base, 'is_error': True, 'tokens': {'output': 0}}))
        self.assertFalse(is_infrastructure_failure(
            {**base, 'is_error': True, 'subtype': 'error_max_budget_usd', 'tokens': {'output': 0}}))
        self.assertFalse(is_infrastructure_failure({**base, 'is_error': True}))

    def test_a_rate_limit_that_cuts_a_run_short_is_not_a_coding_failure(self):
        base = {'has_result': True, 'is_error': True, 'subtype': 'success', 'tokens': {'output': 900}}
        self.assertTrue(is_infrastructure_failure({**base, 'terminal_reason': 'api_error'}))
        self.assertFalse(is_infrastructure_failure({**base, 'is_error': False, 'terminal_reason': 'completed'}))


class CheckedAfterEditTests(unittest.TestCase):
    def test_running_anything_after_the_last_code_edit_counts_as_checking(self):
        edit = ('Edit', {'file_path': 'app.py'})
        run = ('Bash', {'command': 'cd /p && python -m unittest'})
        self.assertEqual(checked_after_last_edit([edit, run]), {'edited_code': True, 'ran_after_last_edit': True})
        self.assertEqual(checked_after_last_edit([run, edit]), {'edited_code': True, 'ran_after_last_edit': False})
        self.assertEqual(checked_after_last_edit([edit, run, edit]), {'edited_code': True, 'ran_after_last_edit': False})

    def test_reading_or_listing_is_not_checking_and_docs_are_not_code(self):
        edit = ('Write', {'file_path': 'app.py'})
        self.assertFalse(checked_after_last_edit([edit, ('Bash', {'command': 'ls -la && cat app.py'})])['ran_after_last_edit'])
        self.assertFalse(checked_after_last_edit([edit, ('Read', {'file_path': 'app.py'})])['ran_after_last_edit'])
        self.assertFalse(checked_after_last_edit([('Edit', {'file_path': 'README.md'})])['edited_code'])
        self.assertFalse(checked_after_last_edit([])['edited_code'])

    def test_the_row_carries_the_verdict_and_the_summary_counts_unchecked_finishes(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 't.jsonl'
            path.write_text(stream({'type': 'assistant', 'parent_tool_use_id': None, 'message': {'id': 'm', 'content': [
                {'type': 'tool_use', 'name': 'Write', 'input': {'file_path': 'a.py'}}]}}), encoding='utf-8')
            parsed = parse_stream(path)
        self.assertEqual((parsed['edited_code'], parsed['ran_after_last_edit']), (True, False))
        row = {**parsed, 'passed': False, 'cost_usd': None, 'turns': 1, 'wall_s': 1, 'timed_out': False, 'lines_added': 1}
        summary = summarize_arm([row, {**row, 'ran_after_last_edit': True}])
        self.assertEqual((summary['edited_runs'], summary['unchecked_finishes'], summary['unchecked_rate']), (2, 1, 0.5))


class BudgetTests(unittest.TestCase):
    def command(self, provider, budget=None):
        args = SimpleNamespace(provider=provider, budget=budget, effort=None)
        return agent_command('claude', 'm', args, None)

    def test_claude_runs_are_capped_but_other_models_are_not(self):
        # Claude Code prices other models with a made-up rate; a cap there cut off half the runs of the arm that used more tokens.
        self.assertEqual(self.command('anthropic')[self.command('anthropic').index('--max-budget-usd') + 1], '1.0')
        self.assertNotIn('--max-budget-usd', self.command('ollama'))

    def test_an_explicit_budget_always_applies(self):
        command = self.command('ollama', 5.0)
        self.assertEqual(command[command.index('--max-budget-usd') + 1], '5.0')


class HarnessSetupTests(unittest.TestCase):
    def test_arm_specs(self):
        self.assertIsNone(parse_arm('baseline').root)
        arm = parse_arm('v2=/tmp/bossku@core')
        self.assertEqual((arm.name, arm.profile), ('v2', 'core'))
        self.assertEqual(parse_arm('v2=/tmp/bossku').profile, 'full')

    def test_child_processes_see_a_throwaway_home_and_none_of_the_launching_session(self):
        with mock.patch.dict('os.environ', {'CLAUDE_CODE_MESSAGING_TOKEN': 'secret', 'CLAUDE_CODE_SESSION_ID': 'abc'}):
            env = child_env(Path('shim'), {'ANTHROPIC_AUTH_TOKEN': 't'}, Path('throwaway'))
        self.assertEqual((env['HOME'], env['USERPROFILE']), ('throwaway', 'throwaway'))
        self.assertNotIn('CLAUDE_CODE_MESSAGING_TOKEN', env)
        self.assertNotIn('CLAUDE_CODE_SESSION_ID', env)
        self.assertTrue(env['PATH'].startswith('shim'))

    def test_the_anthropic_provider_keeps_the_real_login_but_not_the_real_home(self):
        with mock.patch.dict('os.environ', {'CLAUDE_CONFIG_DIR': ''}, clear=False):
            env = child_env(Path('shim'), {}, Path('throwaway'))
        self.assertTrue(env['CLAUDE_CONFIG_DIR'].endswith('.claude'))
        self.assertEqual(env['HOME'], 'throwaway')

    def test_baseline_shim_pretends_bossku_is_not_installed(self):
        with tempfile.TemporaryDirectory() as tmp:
            shim = Path(tmp) / 'shim'
            write_shim(shim, Arm('baseline', None), Path(tmp) / 'home')
            self.assertIn('command not found', (shim / 'bossku').read_text(encoding='utf-8'))
            write_shim(shim, Arm('v2', Path(tmp) / 'root'), Path(tmp) / 'home')
            text = (shim / 'bossku').read_text(encoding='utf-8')
            self.assertIn('-m bossku --home', text)
            self.assertIn('PYTHONPATH', text)

    def test_humaneval_tasks_are_hidden_test_stubs(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = materialize_humaneval(Path(tmp) / 'he', 3)
            tasks = sorted(dest.glob('*/task.json'))
            self.assertEqual(len(tasks), 3)
            task = json.loads(tasks[0].read_text(encoding='utf-8'))
            base = tasks[0].parent
            self.assertTrue((base / 'seed' / 'solution.py').read_text(encoding='utf-8').rstrip().endswith('pass'))
            self.assertIn('check(solution.', (base / 'hidden' / 'test_humaneval_hidden.py').read_text(encoding='utf-8'))
            self.assertNotIn('hidden', task['prompt'].lower())

    def test_humaneval_sample_is_reproducible(self):
        with tempfile.TemporaryDirectory() as tmp:
            first = sorted(p.name for p in materialize_humaneval(Path(tmp) / 'a', 5).iterdir())
            second = sorted(p.name for p in materialize_humaneval(Path(tmp) / 'b', 5).iterdir())
            self.assertEqual(first, second)


class DiffTests(unittest.TestCase):
    def test_changes_are_measured_against_the_seed_even_if_the_agent_commits(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            run = lambda *args: subprocess.run(['git', *args], cwd=repo, check=True, capture_output=True)  # noqa: E731
            run('init', '-q')
            run('config', 'user.email', 'a@b.c')
            run('config', 'user.name', 'n')
            (repo / 'a.py').write_text('one\n', encoding='utf-8')
            (repo / '.claude').mkdir()
            (repo / '.claude' / 'x.md').write_text('scaffold\n', encoding='utf-8')
            run('add', '-A')
            run('commit', '-q', '-m', 'seed')
            seed = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=repo, capture_output=True, text=True,
                                  check=True).stdout.strip()
            (repo / 'a.py').write_text('one\ntwo\nthree\n', encoding='utf-8')
            (repo / '.claude' / 'x.md').write_text('changed\n', encoding='utf-8')
            run('add', '-A')
            run('commit', '-q', '-m', 'agent commit')
            stats = diff_stats(repo, seed)
            self.assertEqual(stats, {'files_changed': 1, 'lines_added': 2, 'lines_removed': 0})


class ReportTests(unittest.TestCase):
    def row(self, arm, task, passed, cost, out=100):
        return {'arm': arm, 'task': task, 'model': 'm', 'passed': passed, 'cost_usd': cost, 'wall_s': 10.0,
                'turns': 3, 'timed_out': False, 'category': 'feature', 'skills_invoked': [], 'skill_files_read': [],
                'bossku_calls': [], 'lines_added': 4, 'lines_removed': 1,
                'tokens': {'input_uncached': 10, 'cache_write': 20, 'cache_read': 70, 'output': out}}

    def test_cost_is_absent_not_zero_for_providers_without_per_token_billing(self):
        summary = summarize_arm([self.row('a', 't', True, None), self.row('a', 'u', False, None)])
        self.assertIsNone(summary['cost_mean'])
        self.assertEqual(summary['pass_rate'], 0.5)

    def test_paired_report_compares_arms_on_the_same_tasks(self):
        rows = [self.row('baseline', 't1', False, 1.0), self.row('baseline', 't2', True, 1.0),
                self.row('v2', 't1', True, 0.5), self.row('v2', 't2', True, 1.5)]
        report = build_report(rows, 'baseline')
        paired = report['models']['m']['paired']['v2']
        self.assertEqual(paired['passed']['tasks'], 2)
        self.assertAlmostEqual(paired['passed']['mean_diff'], 0.5)
        self.assertAlmostEqual(paired['cost']['mean_diff'], 0.0)


class ScrubTests(unittest.TestCase):
    """Saved rows must not carry the account or folder names of whoever ran the benchmark."""

    def test_home_folders_in_windows_and_unix_styles_are_replaced(self):
        from scripts.benchmark_agent import scrub
        cases = {
            'cd "C:\\Users\\jo\\AppData\\Local\\Temp\\bf\\r\\1" && bossku memory-path': 'cd "<home>\\AppData\\Local\\Temp\\bf\\r\\1" && bossku memory-path',
            'cd "C:/Users/jo/AppData/Local/Temp/bf/r/1"': 'cd "<home>/AppData/Local/Temp/bf/r/1"',
            'ls /c/Users/jo/work and /home/ann/project': 'ls <home>/work and <home>/project',
        }
        for text, expected in cases.items():
            with self.subTest(text=text):
                self.assertEqual(scrub(text), expected)

    def test_the_notes_folder_under_documents_and_the_account_name_are_replaced(self):
        from scripts.benchmark_agent import scrub
        text = 'C:\\Users\\jo\\OneDrive\\Documents\\some-owner\\BosskuAI\\proj'
        self.assertEqual(scrub(text), '<home>\\OneDrive\\Documents\\<folder>\\BosskuAI\\proj')
        with mock.patch('pathlib.Path.home', return_value=Path('/somewhere/jorge')):
            self.assertEqual(scrub('written by jorge, not jorgeous'), 'written by <user>, not jorgeous')

    def test_compact_scrubs_every_field_of_a_row_not_only_the_free_text(self):
        from scripts.benchmark_agent import cmd_compact
        row = {'kind': 'task', 'arm': 'after', 'final_text': 'done', 'bossku_calls': [],
               'skill_files_read': ['C:/Users/jo/AppData/Local/Temp/x/.claude/skills/s/SKILL.md']}
        with tempfile.TemporaryDirectory() as tmp:
            source, target = Path(tmp) / 'runs.jsonl', Path(tmp) / 'out.jsonl'
            source.write_text(json.dumps(row) + '\n', encoding='utf-8')
            with mock.patch('pathlib.Path.home', return_value=Path('/somewhere/jo')):
                cmd_compact(SimpleNamespace(runs=[str(source)], out=str(target), kind=None, arm=None))
            saved = json.loads(target.read_text(encoding='utf-8'))
        self.assertEqual(saved['skill_files_read'], ['<home>/AppData/Local/Temp/x/.claude/skills/s/SKILL.md'])

    def test_compact_keeps_one_row_per_finished_run_and_keeps_the_excluded_tries(self):
        from scripts.benchmark_agent import cmd_compact
        done = {'kind': 'task', 'arm': 'after', 'run_id': 'task.after.m.t.t1', 'passed': True}
        rows = [dict(done, infrastructure_failure=True, passed=False), done, dict(done, passed=False)]
        with tempfile.TemporaryDirectory() as tmp:
            source, target = Path(tmp) / 'runs.jsonl', Path(tmp) / 'out.jsonl'
            source.write_text(''.join(json.dumps(r) + '\n' for r in rows), encoding='utf-8')
            cmd_compact(SimpleNamespace(runs=[str(source)], out=str(target), kind=None, arm=None))
            saved = [json.loads(line) for line in target.read_text(encoding='utf-8').splitlines()]
        self.assertEqual([r.get('infrastructure_failure', False) for r in saved], [True, False])
        self.assertTrue(saved[1]['passed'])

    def test_ordinary_text_is_left_alone(self):
        from scripts.benchmark_agent import scrub
        text = 'Ran 3 tests in 0.01s; see src/app/main.py and /tmp/x'
        self.assertEqual(scrub(text), text)


class FindClaudeTests(unittest.TestCase):
    def locate(self, *relative):
        from scripts.benchmark_agent import find_claude
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp) / 'Claude' / 'claude-code'
            for rel in relative:
                (base / rel).parent.mkdir(parents=True)
                (base / rel).write_text('')
            with mock.patch.dict('os.environ', {'APPDATA': tmp}), mock.patch('shutil.which', return_value=None):
                return Path(find_claude(None)).relative_to(base).as_posix()

    def test_the_newest_version_wins_in_both_folder_layouts(self):
        self.assertEqual(self.locate('2.1.9/claude.exe', '2.1.10/claude.exe'), '2.1.10/claude.exe')
        self.assertEqual(self.locate('2.1.284/aaa/claude.exe', '2.1.286/bbb/claude.exe'), '2.1.286/bbb/claude.exe')

    def test_an_explicit_path_is_used_as_given(self):
        from scripts.benchmark_agent import find_claude
        self.assertEqual(find_claude('C:/tools/claude.exe'), 'C:/tools/claude.exe')


class SessionKeepingTests(unittest.TestCase):
    """The stop gate reads the session transcript, so a run that does not keep its session has no gate."""

    def test_no_provider_asks_claude_code_to_skip_saving_the_session(self):
        for provider in ('anthropic', 'ollama'):
            args = SimpleNamespace(provider=provider, budget=None, effort=None)
            self.assertNotIn('--no-session-persistence', agent_command('claude', 'm', args, None))

    def test_the_session_folder_is_named_after_the_work_folder(self):
        from scripts.benchmark_agent import claude_session_dir
        with tempfile.TemporaryDirectory() as tmp, mock.patch.dict('os.environ', {'CLAUDE_CONFIG_DIR': tmp}):
            work = Path(tmp) / 'a b' / 'r' / 'abc123'
            work.mkdir(parents=True)
            folder = claude_session_dir(work)
            self.assertEqual(folder.parent, Path(tmp) / 'projects')
            self.assertTrue(folder.name.endswith('-a-b-r-abc123'), folder.name)
            self.assertNotRegex(folder.name, r'[^A-Za-z0-9-]')


if __name__ == '__main__':
    unittest.main()


class RoutingProbeTests(unittest.TestCase):
    def assistant(self, *blocks):
        return {'type': 'assistant', 'parent_tool_use_id': None, 'message': {'content': list(blocks)}}

    def use(self, name, **args):
        return {'type': 'tool_use', 'name': name, 'input': args}

    def test_skills_are_detected_however_the_agent_opens_them(self):
        from scripts.benchmark_agent import skills_loaded
        events = [self.assistant(
            self.use('Skill', skill='bosskuai-tdd-loop'),
            self.use('Read', file_path='C:/Users/x/.claude/skills/seo-audit/SKILL.md'),
            self.use('Bash', command='bossku --home /tmp/h skills show taste-skill'),
            self.use('Skill', skill='bossku-ai:cofounder'),
            self.use('Bash', command='bossku skills find "x"'),
            self.use('Read', file_path='README.md'),
        )]
        self.assertEqual(skills_loaded(events), ['bosskuai-tdd-loop', 'seo-audit', 'taste-skill', 'cofounder'])

    def test_subagent_activity_is_not_counted_as_the_agents_own_choice(self):
        from scripts.benchmark_agent import skills_loaded
        sub = self.assistant(self.use('Skill', skill='inner'))
        sub['parent_tool_use_id'] = 'toolu_1'
        self.assertEqual(skills_loaded([sub]), [])

    def test_a_probe_stops_a_few_steps_after_the_first_skill_or_after_ten_steps(self):
        from scripts.benchmark_agent import routing_stop
        other = self.use('Read', file_path='a.py')
        self.assertFalse(routing_stop([self.assistant(other, other)]))
        opened = [self.assistant(self.use('Skill', skill='x'), other, other)]
        self.assertFalse(routing_stop(opened))
        self.assertTrue(routing_stop(opened + [self.assistant(other)]))
        self.assertTrue(routing_stop([self.assistant(*[other] * 10)]))
        self.assertTrue(routing_stop([{'type': 'result'}]))

    def test_prompts_split_into_two_stable_halves(self):
        from scripts.benchmark_agent import routing_split
        ids = [f'h-{i:03d}' for i in range(1, 161)]
        halves = {routing_split(i) for i in ids}
        self.assertEqual(halves, {'dev', 'test'})
        self.assertEqual([routing_split(i) for i in ids], [routing_split(i) for i in ids])
