import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from threading import Barrier
from unittest import mock

from bossku.cli import main
from bossku.hooks import run_sync_hook
from bossku.init_project import init_project
from bossku.install import install_auto_memory_instructions
from bossku.memory import (
    init_memory_templates,
    load_user_config,
    memory_directory,
    remember,
    save_user_config,
    sync_project,
)


class VaultMemoryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.home = Path(self.tmp.name)
        self.project = self.home / 'repo'
        self.project.mkdir()
        self.vault = self.home / 'vault'
        self.vault.mkdir()
        save_user_config({'obsidian_vault': str(self.vault), 'memory_storage': 'obsidian'}, self.home)

    def test_remember_writes_only_to_vault_and_preserves_vault_edits(self):
        target = self.vault / 'BosskuAI' / 'repo' / 'decisions.md'
        target.parent.mkdir(parents=True)
        target.write_text('# Decisions\n\nEdited in Obsidian.\n', encoding='utf-8')
        result = remember(self.project, 'decision', 'Keep this choice.', home=self.home)
        self.assertEqual(Path(result['file']), target)
        self.assertEqual(result['vault']['status'], 'ok')
        self.assertIn('Edited in Obsidian.', target.read_text(encoding='utf-8'))
        self.assertIn('Keep this choice.', target.read_text(encoding='utf-8'))
        self.assertFalse((self.project / '.bossku').exists())

    def test_redaction_runs_before_vault_write(self):
        result = remember(self.project, 'learning', 'api_key=supersecret123', home=self.home)
        content = Path(result['file']).read_text(encoding='utf-8')
        self.assertNotIn('supersecret123', content)
        self.assertIn('[REDACTED]', content)

    def test_offline_vault_does_not_fall_back_to_repo(self):
        self.vault.rmdir()
        with self.assertRaisesRegex(ValueError, 'unavailable'):
            remember(self.project, 'decision', 'Keep this choice.', home=self.home)
        self.assertFalse((self.project / '.bossku').exists())
        self.assertEqual(sync_project(self.project, home=self.home)['status'], 'pending')

    def test_no_vault_does_not_fall_back_to_repo(self):
        save_user_config({'memory_storage': 'obsidian'}, self.home)
        with self.assertRaisesRegex(ValueError, 'configured'):
            remember(self.project, 'decision', 'Keep this choice.', home=self.home)
        self.assertFalse((self.project / '.bossku').exists())

    def test_sync_does_not_overwrite_vault_with_legacy_repo_notes(self):
        legacy = self.project / '.bossku' / 'memory'
        legacy.mkdir(parents=True)
        (legacy / 'decisions.md').write_text('Stale repo copy', encoding='utf-8')
        target = self.vault / 'BosskuAI' / 'repo' / 'decisions.md'
        target.parent.mkdir(parents=True)
        target.write_text('Current Obsidian copy', encoding='utf-8')
        self.assertEqual(sync_project(self.project, home=self.home)['status'], 'ok')
        self.assertEqual(target.read_text(encoding='utf-8'), 'Current Obsidian copy')
        self.assertFalse((legacy / 'sync-state.json').exists())

    def test_session_hook_never_creates_repo_memory(self):
        with mock.patch('sys.stdin', io.StringIO(json.dumps({'cwd': str(self.project)}))):
            result = run_sync_hook(home=self.home)
        self.assertEqual(result['status'], 'ok')
        self.assertFalse((self.project / '.bossku').exists())

    def test_init_templates_go_to_vault(self):
        result = init_project(self.project, home=self.home)
        self.assertEqual(Path(result['memory']), self.vault / 'BosskuAI' / 'repo')
        self.assertTrue((Path(result['memory']) / 'handoff.md').is_file())
        self.assertFalse((self.project / '.bossku' / 'memory').exists())
        self.assertIn('Automatically save', (self.project / 'AGENTS.md').read_text(encoding='utf-8'))

    def test_cli_memory_path_resolves_vault(self):
        output = io.StringIO()
        with redirect_stdout(output):
            status = main(['memory-path', '--home', str(self.home), '--project', str(self.project)])
        self.assertEqual(status, 0)
        self.assertEqual(Path(json.loads(output.getvalue())['memory_dir']), self.vault / 'BosskuAI' / 'repo')

    def test_vault_inside_code_repo_is_rejected(self):
        vault = self.project / 'vault'
        vault.mkdir()
        save_user_config({'memory_storage': 'obsidian', 'obsidian_vault': str(vault)}, self.home)
        with self.assertRaisesRegex(ValueError, 'outside the code repository'):
            remember(self.project, 'decision', 'Keep this choice.', home=self.home)
        self.assertFalse((self.project / '.bossku').exists())

    def test_auto_instructions_preserve_user_rules_and_are_idempotent(self):
        path = self.home / '.codex' / 'AGENTS.md'
        path.parent.mkdir()
        path.write_text('Keep my rules.\n', encoding='utf-8')
        install_auto_memory_instructions(self.home)
        first = path.read_text(encoding='utf-8')
        install_auto_memory_instructions(self.home)
        self.assertEqual(first, path.read_text(encoding='utf-8'))
        self.assertIn('Keep my rules.', first)
        self.assertIn('Automatically save', first)
        self.assertIn('memory-path', first)
        self.assertFalse((self.home / '.claude').exists())

    def test_configured_workspace_root_groups_subrepo_memory(self):
        child = self.project / 'tenant-frontend'
        child.mkdir()
        save_user_config({'memory_storage': 'obsidian', 'obsidian_vault': str(self.vault),
                          'memory_project_roots': [str(self.project)]}, self.home)
        result = remember(child, 'decision', 'Shared workspace decision.', home=self.home)
        self.assertEqual(Path(result['file']), self.vault / 'BosskuAI' / 'repo' / 'decisions.md')
        self.assertFalse((child / '.bossku').exists())
        parent_result = remember(self.project, 'decision', 'Parent uses the same memory.', home=self.home)
        self.assertEqual(parent_result['file'], result['file'])

    def other_project(self, name='repo'):
        project = self.home / 'other' / name
        project.mkdir(parents=True)
        return project

    def snapshot(self):
        return {str(path.relative_to(self.home)): path.read_bytes()
                for path in self.home.rglob('*') if path.is_file()}

    def test_unrelated_same_name_cannot_read_or_append_claimed_memory(self):
        other = self.other_project()
        original = remember(self.project, 'decision', 'Only the original project.', home=self.home)
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, 'already belongs'):
            memory_directory(other, home=self.home)
        with self.assertRaisesRegex(ValueError, 'already belongs'):
            remember(other, 'decision', 'Do not mix this project.', home=self.home)
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(Path(original['file']).parent, self.vault / 'BosskuAI' / 'repo')
        self.assertFalse((other / '.bossku').exists())

    def test_init_templates_claim_folder_before_another_project_writes(self):
        other = self.other_project()
        target = init_memory_templates(self.project, home=self.home)
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, 'already belongs'):
            init_memory_templates(other, home=self.home)
        self.assertEqual(target, self.vault / 'BosskuAI' / 'repo')
        self.assertEqual(self.snapshot(), before)

    def test_sanitized_project_names_cannot_share_claimed_memory(self):
        first = self.home / 'billing.accounts'
        first.mkdir()
        second = self.other_project('billing-accounts')
        result = remember(first, 'decision', 'Billing evidence.', home=self.home)
        self.assertEqual(Path(result['file']).parent.name, 'billing-accounts')
        with self.assertRaisesRegex(ValueError, 'already belongs'):
            remember(second, 'decision', 'Unrelated evidence.', home=self.home)

    def test_namespaces_separate_duplicates_without_moving_existing_notes(self):
        other = self.other_project()
        first = remember(self.project, 'decision', 'Existing canonical note.', home=self.home)
        original = Path(first['file']).read_bytes()
        cfg = load_user_config(self.home)
        cfg['memory_project_namespaces'] = {str(other): 'other-repo'}
        save_user_config(cfg, self.home)
        second = remember(other, 'decision', 'Separate canonical note.', home=self.home)
        self.assertEqual(Path(second['file']).parent, self.vault / 'BosskuAI' / 'other-repo')
        self.assertEqual(Path(first['file']).read_bytes(), original)
        self.assertEqual(memory_directory(self.project, home=self.home), Path(first['file']).parent)

    def test_separate_vaults_can_use_the_same_project_folder_name(self):
        other = self.other_project()
        first = remember(self.project, 'decision', 'First vault.', home=self.home)
        original = Path(first['file']).read_bytes()
        second_vault = self.home / 'another-vault'
        second_vault.mkdir()
        cfg = load_user_config(self.home)
        cfg['obsidian_vault'] = str(second_vault)
        save_user_config(cfg, self.home)
        second = remember(other, 'decision', 'Second vault.', home=self.home)
        self.assertEqual(Path(second['file']).parent, second_vault / 'BosskuAI' / 'repo')
        self.assertEqual(Path(first['file']).read_bytes(), original)

    def test_memory_path_and_sync_check_do_not_claim_or_create_folders(self):
        before = self.snapshot()
        output = io.StringIO()
        with redirect_stdout(output):
            status = main(['memory-path', '--home', str(self.home), '--project', str(self.project)])
        self.assertEqual(status, 0)
        self.assertEqual(memory_directory(self.project, home=self.home), self.vault / 'BosskuAI' / 'repo')
        self.assertEqual(sync_project(self.project, home=self.home)['status'], 'ok')
        self.assertEqual(self.snapshot(), before)
        self.assertFalse((self.home / '.bosskuai' / 'memory-project-registry').exists())
        self.assertFalse((self.vault / 'BosskuAI').exists())

    def test_malformed_ownership_claim_blocks_reads_and_writes(self):
        result = remember(self.project, 'decision', 'Keep the valid note.', home=self.home)
        claim = next((self.home / '.bosskuai' / 'memory-project-registry').glob('*.json'))
        valid_claim = claim.read_bytes()
        original = Path(result['file']).read_bytes()
        invalid_claims = (
            'not JSON', '[]', '{}', '{"project_root": 7, "memory_dir": "wrong"}',
            json.dumps({'project_root': str(self.project), 'memory_dir': str(self.vault / 'other')}),
            json.dumps({'project_root': 'relative', 'memory_dir': str(Path(result['file']).parent)}),
        )
        for invalid in invalid_claims:
            with self.subTest(invalid=invalid):
                claim.write_text(invalid, encoding='utf-8')
                with self.assertRaisesRegex(ValueError, 'ownership claim'):
                    memory_directory(self.project, home=self.home)
                with self.assertRaisesRegex(ValueError, 'ownership claim'):
                    remember(self.project, 'decision', 'Must not append.', home=self.home)
                self.assertEqual(Path(result['file']).read_bytes(), original)
        claim.write_bytes(valid_claim)
        self.assertEqual(memory_directory(self.project, home=self.home), Path(result['file']).parent)

    def test_invalid_namespace_configuration_fails_before_writing(self):
        for mapping in ([], {str(self.project): ''}, {str(self.project): 4}):
            with self.subTest(mapping=mapping):
                cfg = load_user_config(self.home)
                cfg['memory_project_namespaces'] = mapping
                save_user_config(cfg, self.home)
                before = self.snapshot()
                with self.assertRaisesRegex(ValueError, 'memory_project_namespaces'):
                    remember(self.project, 'decision', 'Must not write.', home=self.home)
                self.assertEqual(self.snapshot(), before)

    def test_racing_projects_cannot_both_claim_the_same_folder(self):
        other = self.other_project()
        barrier = Barrier(2)

        def write(project, note):
            barrier.wait(timeout=5)
            try:
                result = remember(project, 'decision', note, home=self.home)
                return result, note
            except ValueError:
                return None, note

        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(lambda args: write(*args),
                                    [(self.project, 'Original project note.'),
                                     (other, 'Other project note.')]))
        saved = [(result, note) for result, note in results if result is not None]
        self.assertEqual(len(saved), 1)
        content = Path(saved[0][0]['file']).read_text(encoding='utf-8')
        self.assertIn(saved[0][1], content)
        self.assertTrue(all(note not in content for result, note in results if result is None))

    def test_legacy_storage_still_saves_without_a_vault(self):
        save_user_config({}, self.home)
        result = remember(self.project, 'decision', 'Legacy workflow.', home=self.home)
        self.assertEqual(Path(result['file']), self.project / '.bossku' / 'memory' / 'decisions.md')
        self.assertEqual(result['vault']['status'], 'skipped')

    def test_unknown_storage_cannot_fall_back_during_sync(self):
        save_user_config({'memory_storage': 'invalid', 'obsidian_vault': str(self.vault)}, self.home)
        with self.assertRaisesRegex(ValueError, 'unknown memory_storage'):
            sync_project(self.project, home=self.home)
        self.assertFalse((self.project / '.bossku').exists())
