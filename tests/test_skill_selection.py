import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

from bossku.cli import main
from bossku.index import index_is_stale, write_index
from bossku.install import update_user
from bossku.init_project import init_project
from bossku.memory import save_user_config
from bossku.skills import _profile_skills, find_skill, select_skill_stack, write_routing_cache


ROOT = Path(__file__).resolve().parents[1]


class SkillSelectionTests(unittest.TestCase):
    def select(self, prompt, **kwargs):
        return select_skill_stack(prompt, ROOT, **kwargs)

    def ids(self, result):
        return [row['skill_id'] for row in result['selected']]

    def test_explicit_alias_and_complements_are_honored(self):
        result = self.select('use bosskuai-caveman and python-testing for this task')
        self.assertEqual(self.ids(result), ['bosskuai-token-saver', 'python-testing'])
        self.assertTrue(all(row['reason'] == 'explicit skill request' for row in result['selected']))

    def test_incompatible_explicit_directions_are_explained(self):
        result = self.select('use taste-skill and hallmark to build this landing page')
        self.assertIn('taste-skill', self.ids(result))
        self.assertNotIn('hallmark', self.ids(result))
        self.assertTrue(any(row['skill_id'] == 'hallmark' and 'alternative' in row['reason']
                            for row in result['deferred']))

    def test_debugging_alternatives_do_not_duplicate_work(self):
        result = self.select('debug this crash and investigate its root cause')
        self.assertLessEqual(len(set(self.ids(result)) &
                                 {'bosskuai-diagnose-loop', 'systematic-debugging'}), 1)

    def test_multi_domain_complements_cover_distinct_concerns(self):
        result = self.select('write pytest fixtures and run Google Ads for our app', limit=8)
        self.assertIn('python-testing', self.ids(result))
        self.assertIn('ads', self.ids(result))
        self.assertTrue(all(row['reason'] and row['description'] for row in result['selected']))

    def test_optional_hindsight_does_not_hijack_ordinary_reflection(self):
        for prompt in ('reflect on our architecture decisions', 'recall our previous design decisions',
                       'retain our source references for this review'):
            with self.subTest(prompt=prompt):
                self.assertNotIn('bosskuai-hindsight-memory', self.ids(self.select(prompt)))
        self.assertIn('bosskuai-hindsight-memory', self.ids(self.select('connect Hindsight memory to this project')))

    def test_negated_skill_is_not_loaded(self):
        result = self.select("write pytest fixtures, do not use Hindsight")
        self.assertIn('python-testing', self.ids(result))
        self.assertNotIn('bosskuai-hindsight-memory', self.ids(result))

    def test_negated_alias_is_not_loaded(self):
        result = self.select('do not use bosskuai-caveman; write pytest fixtures')
        self.assertNotIn('bosskuai-token-saver', self.ids(result))
        self.assertIn('python-testing', self.ids(result))

    def test_negated_invocation_markers_are_not_loaded(self):
        for prompt, excluded in (
            ('do not use /ads, use pricing', 'ads'),
            ('do not use $python-testing, use python-patterns', 'python-testing'),
            ('do not run /ads; use pricing', 'ads'),
            ('do not invoke $python-testing; use python-patterns', 'python-testing'),
        ):
            with self.subTest(prompt=prompt):
                self.assertNotIn(excluded, self.ids(self.select(prompt)))

    def test_excluded_cofounder_is_not_reintroduced_as_fallback(self):
        result = self.select('do not use cofounder')
        self.assertNotIn('cofounder', self.ids(result))
        self.assertIsNone(result['primary'])

    def test_common_domain_word_is_not_an_explicit_skill_request(self):
        result = self.select('review the Python API schema and add tests')
        self.assertNotIn('schema', self.ids(result))
        explicit = self.select('use /schema for structured data markup')
        self.assertIn('schema', self.ids(explicit))

    def test_unknown_named_skill_is_reported(self):
        result = self.select('use bosskuai-nonexistent-skill')
        self.assertIn('bosskuai-nonexistent-skill', result['unavailable_requested'])

    def test_user_only_command_is_deferred(self):
        result = self.select('use /prototype for this feature')
        self.assertNotIn('prototype', self.ids(result))
        self.assertTrue(any(row['skill_id'] == 'prototype' and 'user invocation' in row['reason']
                            for row in result['deferred']))

    def test_noninstalled_skills_never_load(self):
        result = self.select('use x402 to pay for browser automation')
        self.assertNotIn('x402', self.ids(result))
        self.assertTrue(any(row['skill_id'] == 'x402' and 'not installed' in row['reason']
                            for row in result['deferred']))

    def test_availability_filter_reports_missing_requested_skill(self):
        available = set(_profile_skills('core', ROOT))
        result = self.select('use python-testing to write pytest fixtures', available=available)
        self.assertTrue(set(self.ids(result)) <= available)
        self.assertIn('python-testing', result['unavailable_requested'])

    def test_unknown_input_is_an_explicit_low_confidence_fallback(self):
        result = self.select('zzzz qqqq vvvv')
        self.assertEqual(result['primary'], 'cofounder')
        self.assertFalse(result['confident'])
        self.assertEqual(result['selected'][0]['score'], 0.0)

    def test_limit_and_determinism(self):
        prompt = 'write pytest fixtures and run Google Ads and audit keyboard focus'
        self.assertEqual(self.select(prompt), self.select(prompt))
        self.assertLessEqual(len(self.select(prompt, limit=2)['selected']), 2)
        self.assertEqual(self.select(prompt, limit=0)['selected'], [])

    def test_cli_includes_selection_and_profile(self):
        output = io.StringIO()
        with redirect_stdout(output):
            status = main(['skills', 'find', 'use python-testing', '--profile', 'core', '--root', str(ROOT)])
        self.assertEqual(status, 0)
        result = json.loads(output.getvalue())
        self.assertIn('selection', result)
        self.assertIn('python-testing', result['selection']['unavailable_requested'])
        self.assertNotEqual(result['skill_id'], 'python-testing')


class RoutingInventoryTests(unittest.TestCase):
    def test_update_uses_configured_source_unless_explicitly_overridden(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            source = home / 'source'
            save_user_config({'installed_from': str(source), 'profile': 'core', 'obsidian_vault': 'vault'}, home)
            with mock.patch('bossku.install.install_user', return_value={}) as install:
                update_user(home=home)
                install.assert_called_once_with(root=source, home=home, profile='core', vault='vault')
            with mock.patch('bossku.install.install_user', return_value={}) as install:
                update_user(root=ROOT, home=home)
                install.assert_called_once_with(root=ROOT, home=home, profile='core', vault='vault')

    def test_cache_uses_actual_inventory_and_preserves_invocation_flags(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'routing.json'
            write_routing_cache(path, ROOT, available={'cofounder', 'prototype', 'x402'})
            data = json.loads(path.read_text(encoding='utf-8'))
            rows = {row['id']: row for row in data['skills']}
            self.assertEqual(set(rows), {'cofounder', 'prototype'})
            self.assertTrue(rows['prototype']['user_invoked'])
            self.assertIn('alternative_groups', data['selection_policy'])
            self.assertTrue(all(target in rows for target in data['aliases'].values()))

    def test_portable_install_keeps_shared_skill_sidecars(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            project = home / 'project'
            init_project(project, root=ROOT, home=home, portable=True, profile='core')
            support = project / '.bossku'
            self.assertEqual((support / 'docs' / 'memory.md').read_bytes(),
                             (ROOT / 'docs' / 'memory.md').read_bytes())
            self.assertTrue((support / 'references' / 'checklists' / 'skill-health-checklist.md').is_file())

    def test_stale_description_is_rebuilt_without_modifying_saved_index(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill = root / 'skills' / 'bosskuai-sample' / 'SKILL.md'
            skill.parent.mkdir(parents=True)
            skill.write_text('---\nname: bosskuai-sample\ndescription: Use when inspecting apples.\n---\n', encoding='utf-8')
            saved = write_index(root)
            original = saved.read_bytes()
            skill.write_text('---\nname: bosskuai-sample\ndescription: Use when inspecting bananas.\n---\n', encoding='utf-8')
            self.assertTrue(index_is_stale(root))
            self.assertEqual(find_skill('inspecting bananas', root)[0], 'bosskuai-sample')
            self.assertEqual(saved.read_bytes(), original)


if __name__ == '__main__':
    unittest.main()
