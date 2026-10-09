import tempfile
import unittest
from pathlib import Path

from bossku.init_project import init_project
from bossku.install import install_auto_memory_instructions, install_user, uninstall_user
from bossku.skills import _profile_skills, is_managed_skill_name

ROOT = Path(__file__).resolve().parents[1]


class DefaultVoiceTests(unittest.TestCase):
    def test_voice_skill_is_available_in_every_profile(self):
        for profile in ('lean', 'core', 'full'):
            with self.subTest(profile=profile):
                self.assertIn('malaysia-localisation', _profile_skills(profile, ROOT))

    def test_install_preserves_custom_instructions_and_refreshes_voice_once(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            paths = (home / '.codex/AGENTS.md', home / '.claude/CLAUDE.md',
                     home / '.config/opencode/AGENTS.md')
            for path in paths:
                path.parent.mkdir(parents=True)
                path.write_text('# My instructions\nKeep my project glossary.\n', encoding='utf-8')
            install_auto_memory_instructions(home)
            first = [path.read_text(encoding='utf-8') for path in paths]
            install_auto_memory_instructions(home)
            for path, initial in zip(paths, first):
                text = path.read_text(encoding='utf-8')
                self.assertEqual(text, initial)
                self.assertIn('Keep my project glossary.', text)
                self.assertEqual(text.count('<!-- bosskuai:voice:start -->'), 1)
                self.assertIn('malaysia-localisation', text)
                self.assertIn('short, simple and easy to understand', text)
                self.assertIn('<!-- bosskuai:memory:start -->', text)
            self.assertFalse((home / '.cursor').exists())

    def test_project_init_installs_voice_and_keeps_host_imports(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            project = home / 'project'
            project.mkdir()
            (project / 'AGENTS.md').write_text('Keep this project rule.\n', encoding='utf-8')
            init_project(project, root=ROOT, home=home)
            init_project(project, root=ROOT, home=home)
            text = (project / 'AGENTS.md').read_text(encoding='utf-8')
            self.assertIn('Keep this project rule.', text)
            self.assertIn('malaysia-localisation', text)
            self.assertIn('short, simple and easy to understand', text)
            self.assertEqual(text.count('Default voice:'), 1)
            self.assertEqual((project / 'CLAUDE.md').read_text(encoding='utf-8'), '@AGENTS.md\n')
            self.assertEqual((project / '.omp/AGENTS.md').read_text(encoding='utf-8'), '@../AGENTS.md\n')

    def test_full_skill_resources_survive_install_and_uninstall(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            install_user(root=ROOT, home=home, profile='lean')
            for root in (home / '.agents/skills', home / '.claude/skills'):
                skill = root / 'malaysia-localisation'
                for relative in ('SKILL.md', 'references/particles.md', 'references/technical-language.md',
                                 'examples/rojak.jsonl', 'evals/register.jsonl', 'DATA_SOURCES.md', 'LICENSE'):
                    self.assertTrue((skill / relative).is_file(), relative)
                self.assertEqual((skill / 'references/particles.md').read_bytes(),
                                 (ROOT / 'skills/malaysia-localisation/references/particles.md').read_bytes())
                unrelated = root / 'my-custom-skill'
                unrelated.mkdir()
                (unrelated / 'SKILL.md').write_text('Keep my skill', encoding='utf-8')
            self.assertTrue(is_managed_skill_name('malaysia-localisation', ROOT))
            uninstall_user(root=ROOT, home=home)
            for root in (home / '.agents/skills', home / '.claude/skills'):
                self.assertFalse((root / 'malaysia-localisation').exists())
                self.assertTrue((root / 'my-custom-skill/SKILL.md').is_file())


if __name__ == '__main__':
    unittest.main()
