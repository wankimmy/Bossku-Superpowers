import tempfile
import unittest
from pathlib import Path

from filevault import FileVault


class FileVaultHiddenTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)
        self.vault_dir = self.root / "vault"
        (self.vault_dir / "reports").mkdir(parents=True)
        (self.vault_dir / "sub").mkdir(parents=True)
        (self.vault_dir / "reports" / "q1.txt").write_text("Q1 numbers", encoding="utf-8")
        (self.vault_dir / "sub" / "inner.txt").write_text("inner contents", encoding="utf-8")
        self.secret = self.root / "secret.txt"
        self.secret.write_text("top secret", encoding="utf-8")
        self.vault = FileVault(str(self.vault_dir))

    def test_read_file_in_base_dir(self):
        (self.vault_dir / "top.txt").write_text("hello", encoding="utf-8")
        self.assertEqual(self.vault.read("top.txt"), "hello")

    def test_read_nested_subdirectory_file(self):
        self.assertEqual(self.vault.read("reports/q1.txt"), "Q1 numbers")

    def test_leading_dot_slash_is_allowed(self):
        self.assertEqual(self.vault.read("./reports/q1.txt"), "Q1 numbers")

    def test_dotdot_that_stays_inside_vault_is_allowed(self):
        self.assertEqual(self.vault.read("sub/../reports/q1.txt"), "Q1 numbers")

    def test_missing_file_raises_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            self.vault.read("reports/nope.txt")

    def test_directory_raises_is_a_directory_error(self):
        with self.assertRaises(IsADirectoryError):
            self.vault.read("reports")

    def test_parent_traversal_escaping_vault_raises_permission_error(self):
        with self.assertRaises(PermissionError):
            self.vault.read("../secret.txt")

    def test_nested_parent_traversal_escaping_vault_raises_permission_error(self):
        with self.assertRaises(PermissionError):
            self.vault.read("sub/../../secret.txt")

    def test_absolute_path_raises_permission_error(self):
        with self.assertRaises(PermissionError):
            self.vault.read(self.secret.as_posix())

    def test_empty_relative_path_raises_permission_error(self):
        with self.assertRaises(PermissionError):
            self.vault.read("")

    def test_symlink_escaping_vault_raises_permission_error(self):
        link = self.vault_dir / "escape"
        try:
            link.symlink_to(self.secret)
        except (OSError, NotImplementedError):
            self.skipTest("symlinks are not supported in this environment")
        with self.assertRaises(PermissionError):
            self.vault.read("escape")

    def test_read_returns_exact_contents(self):
        (self.vault_dir / "exact.txt").write_text("line one\nline two", encoding="utf-8")
        self.assertEqual(self.vault.read("exact.txt"), "line one\nline two")

    def test_multiple_independent_reads(self):
        self.assertEqual(self.vault.read("reports/q1.txt"), "Q1 numbers")
        self.assertEqual(self.vault.read("sub/inner.txt"), "inner contents")


if __name__ == "__main__":
    unittest.main()
