import os
import tempfile
import unittest

from static_files import PathSecurityError, read_file

MAX_DEPTH = 6


class StaticFilesHiddenTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = self._tmp.name

        self._write("notes.txt", b"top level")
        self._write("notes..bak", b"dotdot substring")
        self._write("caf\u00e9_\u00e9toile.txt", b"unicode name")
        self._write("%2e%2e_report.txt", b"percent literal")
        self._write("my notes.txt", b"has a space")
        self._write("a/b/c.txt", b"nested normal")
        os.makedirs(os.path.join(self.root, "sub"), exist_ok=True)
        self._write("sub/inner.txt", b"inside sub")

        at_limit = "/".join(f"d{i}" for i in range(MAX_DEPTH)) + "/deep.txt"
        self._write(at_limit, b"at the depth limit")
        self.at_limit_path = at_limit

        over_limit = "/".join(f"d{i}" for i in range(MAX_DEPTH + 1)) + "/deep.txt"
        self._write(over_limit, b"over the depth limit")
        self.over_limit_path = over_limit

    def _write(self, relpath, data):
        full = os.path.join(self.root, *relpath.split("/"))
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "wb") as fh:
            fh.write(data)

    # ---- traversal / absolute path ----

    def test_rejects_dotdot_leading(self):
        with self.assertRaises(PathSecurityError):
            read_file(self.root, "../secret.txt")

    def test_rejects_dotdot_buried(self):
        with self.assertRaises(PathSecurityError):
            read_file(self.root, "a/b/../../../secret.txt")

    def test_rejects_dotdot_that_would_cancel_out(self):
        # Mathematically resolves back inside root, but the policy is to
        # refuse any ".." segment outright.
        with self.assertRaises(PathSecurityError):
            read_file(self.root, "sub/../notes.txt")

    def test_rejects_leading_slash(self):
        with self.assertRaises(PathSecurityError):
            read_file(self.root, "/etc/passwd")

    def test_rejects_leading_backslash(self):
        with self.assertRaises(PathSecurityError):
            read_file(self.root, "\\windows\\win.ini")

    def test_rejects_drive_letter(self):
        with self.assertRaises(PathSecurityError):
            read_file(self.root, "C:\\secret.txt")

    def test_rejects_mixed_separator_traversal(self):
        with self.assertRaises(PathSecurityError):
            read_file(self.root, "sub\\..\\..\\secret.txt")

    # ---- malformed / control characters ----

    def test_rejects_nul_byte(self):
        with self.assertRaises(PathSecurityError):
            read_file(self.root, "notes.txt\x00.png")

    def test_rejects_control_char(self):
        with self.assertRaises(PathSecurityError):
            read_file(self.root, "\x07bell.txt")

    # ---- depth limit ----

    def test_rejects_too_deep(self):
        with self.assertRaises(PathSecurityError):
            read_file(self.root, self.over_limit_path)

    def test_allows_exactly_max_depth(self):
        self.assertEqual(
            read_file(self.root, self.at_limit_path), b"at the depth limit"
        )

    # ---- not-a-readable-file cases ----

    def test_rejects_path_is_directory(self):
        with self.assertRaises(PathSecurityError):
            read_file(self.root, "sub")

    def test_rejects_path_missing(self):
        with self.assertRaises(PathSecurityError):
            read_file(self.root, "does_not_exist.txt")

    def test_rejects_empty_path(self):
        with self.assertRaises(PathSecurityError):
            read_file(self.root, "")

    # ---- normal use must still work ----

    def test_allows_dotdot_substring_filename(self):
        self.assertEqual(read_file(self.root, "notes..bak"), b"dotdot substring")

    def test_allows_unicode_filename(self):
        self.assertEqual(
            read_file(self.root, "caf\u00e9_\u00e9toile.txt"), b"unicode name"
        )

    def test_allows_percent_literal_filename(self):
        self.assertEqual(
            read_file(self.root, "%2e%2e_report.txt"), b"percent literal"
        )

    def test_allows_spaces_filename(self):
        self.assertEqual(read_file(self.root, "my notes.txt"), b"has a space")

    def test_allows_nested_normal(self):
        self.assertEqual(read_file(self.root, "a/b/c.txt"), b"nested normal")


if __name__ == "__main__":
    unittest.main()
