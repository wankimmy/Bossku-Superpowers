"""Concrete prompt regressions from the Claude skill-hint investigation."""
import json
import unittest
from pathlib import Path

from bossku.hint import hook_output, pick_skills
from bossku.index import load_index, normalize_task
from bossku.skills import select_skill_stack

ROOT = Path(__file__).resolve().parents[1]
DEBUG = {'bosskuai-diagnose-loop', 'systematic-debugging'}


class RoutingCoverageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = load_index(ROOT)

    def select(self, prompt):
        return {r['skill_id'] for r in select_skill_stack(prompt, ROOT, data=self.data)['selected']}

    def hints(self, prompt):
        return {r['skill_id'] for r in pick_skills(prompt, root=ROOT, data=self.data)}

    def test_short_and_concrete_tasks_are_hinted(self):
        cases = (
            ('audit SEO', {'seo-audit'}),
            ('run the tests', {'verification-before-completion'}),
            ('Implement a function that adds two numbers and returns the result',
             {'bosskuai-coding-best-practices'}),
            ('Write pytest tests covering malformed JSON, timeouts, and retry exhaustion', {'python-testing'}),
            ('Implement count_inversions(nums) in inversions.py and make it fast for large lists of numbers please',
             {'python-patterns'}),
            ('Fix the typo in README.md and audit SEO', {'seo-audit'}),
            ('Explain this React hook in one sentence', {'bosskuai-react-development'}),
            ('What is causing this Python error? Explain in one line', {'python-patterns'}),
            ('Build a responsive landing page for my SaaS with a pricing section and signup form',
             {'bosskuai-taste', 'signup'}),
        )
        for prompt, expected in cases:
            with self.subTest(prompt=prompt):
                self.assertTrue(expected <= self.hints(prompt))

    def test_crash_prompts_select_debugging_and_python_when_named(self):
        cases = (
            'fix this bug',
            'Fix a Python parser that crashes with ValueError when reading an empty CSV field',
            'Tolong check kenapa app saya crash bila user tekan button login',
            'same issue still happens after your fix',
        )
        for prompt in cases:
            with self.subTest(prompt=prompt):
                self.assertTrue(self.select(prompt) & DEBUG)
                self.assertTrue(self.hints(prompt) & DEBUG)
        self.assertIn('python-patterns', self.select(cases[1]))

    def test_router_diagnosis_does_not_load_framework_or_config_skills(self):
        prompt = ('check sometimes when prompt to claude code, it didnt use any skills, '
                  'is it expected or the bossku auto route skills is failed ?')
        self.assertEqual(self.hints(prompt), {'bosskuai-diagnose-loop', 'bosskuai-claude-code-setup'})

    def test_bm_rojak_and_equivalent_requests(self):
        for prompt, expected in (
            ('Tolong audit SEO website saya, check title tags dan meta descriptions yang missing', {'seo-audit'}),
            ('Buat landing page untuk bisnes saya, kena cantik dan senang guna kat phone', {'bosskuai-taste'}),
            ('Baiki fungsi Python yang rosak dan tulis ujian pytest', {'python-patterns', 'python-testing'}),
        ):
            with self.subTest(prompt=prompt):
                self.assertTrue(expected <= self.select(prompt))
                self.assertTrue(expected <= self.hints(prompt))

    def test_explicit_short_requests_and_aliases_work(self):
        for prompt, expected in (
            ('use bosskuai-diagnose-loop', {'bosskuai-diagnose-loop'}),
            ('use python-testing and ads', {'python-testing', 'ads'}),
            ('pakai bosskuai-caveman', {'bosskuai-token-saver'}),
        ):
            with self.subTest(prompt=prompt):
                self.assertTrue(expected <= self.hints(prompt))

    def test_mixed_jobs_keep_distinct_specialists(self):
        prompt = 'Fix the Python API timeout bug and write marketing copy for the launch announcement'
        selected = self.select(prompt)
        self.assertTrue(selected & DEBUG)
        self.assertIn('copywriting', selected)
        hinted = self.hints(prompt)
        self.assertTrue(hinted & DEBUG)
        self.assertIn('copywriting', hinted)
        prompt = 'write pytest fixtures and run Google Ads and audit keyboard focus'
        self.assertEqual(self.hints(prompt), {'python-testing', 'ads', 'accessibility'})

    def test_unrelated_complements_are_not_added(self):
        prompt = 'Please audit my website for SEO issues such as missing title tags and meta descriptions'
        self.assertNotIn('ads', self.select(prompt))
        self.assertNotIn('ads', self.hints(prompt))
        self.assertEqual(self.select('Thanks, now audit SEO'), {'seo-audit'})
        self.assertEqual(self.hints('Thanks, now audit SEO'), {'seo-audit'})
        self.assertNotIn('error-handling', self.hints(
            'Implement a function that adds two numbers and returns the result'))
        self.assertNotIn('emil-design-eng', self.hints(
            'Buat landing page untuk bisnes saya, kena cantik dan senang guna kat phone'))

    def test_noise_exclusions_and_invocation_restrictions(self):
        for prompt in ('hi', 'thanks', 'ok thanks a lot', 'What changed in the last update?',
                       'yes do that', 'zzzz qqqq vvvv', '/prototype compare layouts', '!echo hi',
                       'Review my lunch plan', 'Explain the error in this sentence',
                       'check the code and keep going', 'Translate good morning into Malay and Tamil'):
            self.assertEqual(self.hints(prompt), set(), prompt)
        for prompt, blocked in (
            ('audit SEO but do not use ads', {'ads'}),
            ('tulis ujian pytest tapi jangan pakai Hindsight', {'bosskuai-hindsight-memory'}),
            ('use /prototype for this feature', {'prototype'}),
            ('use x402 to pay for browser automation', {'x402'}),
        ):
            self.assertFalse(self.hints(prompt) & blocked)

    def test_actual_hook_delivers_short_and_combined_requests(self):
        for prompt, expected in (
            ('audit SEO', {'seo-audit'}),
            ('use python-testing and ads', {'python-testing', 'ads'}),
        ):
            out = hook_output(json.dumps({'prompt': prompt, 'cwd': str(ROOT)}), root=ROOT)
            text = out.get('hookSpecificOutput', {}).get('additionalContext', '')
            for sid in expected:
                self.assertIn(sid, text)

    def test_normalization_preserves_identifiers_and_bm_negation(self):
        text = 'Review buat.py, `rosak.json`, ujian.py and C:/src/fungsi.py'
        self.assertEqual(normalize_task(text), text.lower())
        self.assertIn('do not use', normalize_task('jangan pakai /ads'))
        self.assertNotIn('ads', self.select('jangan pakai /ads; audit SEO'))

    def test_other_task_domains_retain_hints(self):
        for prompt, expected in (
            ('Convert this PDF to Markdown', 'markitdown'),
            ('Find qualified prospects for my B2B SaaS', 'prospecting'),
            ('Animate this component with an entrance animation', 'animate'),
            ('Animate this React component', 'animate'),
            ('Extract tables from this scanned PDF', 'odl-pdf'),
            ('Summarize this report with source citations', 'bosskuai-grounding'),
            ('Recommend a pricing strategy for our SaaS', 'pricing'),
        ):
            with self.subTest(prompt=prompt):
                self.assertIn(expected, self.hints(prompt))
        self.assertNotIn('animate-expo', self.hints('Animate this React component'))
        self.assertNotIn('loop-triage', self.hints('Summarize this report'))
        self.assertNotIn('loop-triage', self.hints('Please read this report'))
        self.assertIn('animate-expo', self.hints('use animate-expo'))
