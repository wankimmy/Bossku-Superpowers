import io
import os
import tarfile
import tempfile
import unittest

from archive_tool import ArchiveSecurityError, extract_archive

MAX_MEMBERS = 50
MAX_SINGLE_FILE_BYTES = 2 * 1024 * 1024
MAX_TOTAL_BYTES = 6 * 1024 * 1024
MAX_DEPTH = 8


def _build_tar(path, members):
    """members: list of dicts describing tar entries to write.

    Keys: name, type ('file'|'dir'|'sym'|'hard'|'fifo'|'chr'),
    data (bytes, for 'file'), linkname (for 'sym'/'hard').
    """
    with tarfile.open(path, "w") as tar:
        for m in members:
            info = tarfile.TarInfo(name=m["name"])
            kind = m.get("type", "file")
            if kind == "file":
                data = m.get("data", b"")
                info.type = tarfile.REGTYPE
                info.size = len(data)
                tar.addfile(info, io.BytesIO(data))
            elif kind == "dir":
                info.type = tarfile.DIRTYPE
                tar.addfile(info)
            elif kind == "sym":
                info.type = tarfile.SYMTYPE
                info.linkname = m["linkname"]
                tar.addfile(info)
            elif kind == "hard":
                info.type = tarfile.LNKTYPE
                info.linkname = m["linkname"]
                tar.addfile(info)
            elif kind == "fifo":
                info.type = tarfile.FIFOTYPE
                tar.addfile(info)
            elif kind == "chr":
                info.type = tarfile.CHRTYPE
                tar.addfile(info)
            else:
                raise ValueError(f"unknown kind {kind!r}")


class ArchiveToolHiddenTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.archive_path = os.path.join(self._tmp.name, "bundle.tar")
        self.dest = os.path.join(self._tmp.name, "dest")

    def _tar(self, members):
        _build_tar(self.archive_path, members)
        return self.archive_path

    # ---- path traversal ----

    def test_rejects_leading_parent_traversal(self):
        self._tar([{"name": "../evil.txt", "data": b"x"}])
        with self.assertRaises(ArchiveSecurityError):
            extract_archive(self.archive_path, self.dest)

    def test_rejects_buried_parent_traversal(self):
        self._tar([{"name": "a/../../evil.txt", "data": b"x"}])
        with self.assertRaises(ArchiveSecurityError):
            extract_archive(self.archive_path, self.dest)

    def test_allows_internal_dotdot_that_stays_inside(self):
        self._tar([{"name": "a/../b.txt", "data": b"hi"}])
        written = extract_archive(self.archive_path, self.dest)
        self.assertEqual(written, ["b.txt"])
        with open(os.path.join(self.dest, "b.txt"), "rb") as fh:
            self.assertEqual(fh.read(), b"hi")

    def test_rejects_absolute_path(self):
        self._tar([{"name": "/etc/passwd", "data": b"x"}])
        with self.assertRaises(ArchiveSecurityError):
            extract_archive(self.archive_path, self.dest)

    def test_rejects_windows_drive_path(self):
        self._tar([{"name": "C:/windows/win.ini", "data": b"x"}])
        with self.assertRaises(ArchiveSecurityError):
            extract_archive(self.archive_path, self.dest)

    def test_rejects_backslash_traversal(self):
        self._tar([{"name": "..\\..\\evil.txt", "data": b"x"}])
        with self.assertRaises(ArchiveSecurityError):
            extract_archive(self.archive_path, self.dest)

    # ---- member types ----

    def test_rejects_symlink_member(self):
        self._tar([{"name": "link", "type": "sym", "linkname": "/etc/passwd"}])
        with self.assertRaises(ArchiveSecurityError):
            extract_archive(self.archive_path, self.dest)

    def test_rejects_hardlink_member(self):
        self._tar([
            {"name": "real.txt", "data": b"x"},
            {"name": "link", "type": "hard", "linkname": "real.txt"},
        ])
        with self.assertRaises(ArchiveSecurityError):
            extract_archive(self.archive_path, self.dest)

    def test_rejects_device_file_member(self):
        self._tar([{"name": "dev", "type": "chr"}])
        with self.assertRaises(ArchiveSecurityError):
            extract_archive(self.archive_path, self.dest)

    def test_rejects_fifo_member(self):
        self._tar([{"name": "pipe", "type": "fifo"}])
        with self.assertRaises(ArchiveSecurityError):
            extract_archive(self.archive_path, self.dest)

    # ---- resource limits ----

    def test_rejects_too_many_members(self):
        members = [{"name": f"f{i}.txt", "data": b"x"} for i in range(MAX_MEMBERS + 1)]
        self._tar(members)
        with self.assertRaises(ArchiveSecurityError):
            extract_archive(self.archive_path, self.dest)

    def test_allows_exactly_max_members(self):
        members = [{"name": f"f{i}.txt", "data": b"x"} for i in range(MAX_MEMBERS)]
        self._tar(members)
        written = extract_archive(self.archive_path, self.dest)
        self.assertEqual(len(written), MAX_MEMBERS)

    def test_rejects_oversized_single_file(self):
        self._tar([{"name": "big.bin", "data": b"x" * (MAX_SINGLE_FILE_BYTES + 1)}])
        with self.assertRaises(ArchiveSecurityError):
            extract_archive(self.archive_path, self.dest)

    def test_allows_single_file_at_exact_limit(self):
        self._tar([{"name": "big.bin", "data": b"x" * MAX_SINGLE_FILE_BYTES}])
        written = extract_archive(self.archive_path, self.dest)
        self.assertEqual(written, ["big.bin"])

    def test_rejects_total_size_over_limit(self):
        # Four files at exactly the per-file limit (8 MiB) exceed the 6 MiB total cap.
        members = [
            {"name": f"part{i}.bin", "data": b"y" * MAX_SINGLE_FILE_BYTES}
            for i in range(4)
        ]
        self._tar(members)
        with self.assertRaises(ArchiveSecurityError):
            extract_archive(self.archive_path, self.dest)

    def test_rejects_too_deep_path(self):
        name = "/".join(f"d{i}" for i in range(MAX_DEPTH + 1)) + "/file.txt"
        self._tar([{"name": name, "data": b"x"}])
        with self.assertRaises(ArchiveSecurityError):
            extract_archive(self.archive_path, self.dest)

    def test_allows_exactly_max_depth(self):
        name = "/".join(f"d{i}" for i in range(MAX_DEPTH)) + "/file.txt"
        self._tar([{"name": name, "data": b"ok"}])
        written = extract_archive(self.archive_path, self.dest)
        self.assertEqual(written, [name])

    # ---- atomicity ----

    def test_rejection_leaves_dest_empty(self):
        self._tar([
            {"name": "good.txt", "data": b"fine"},
            {"name": "../evil.txt", "data": b"bad"},
        ])
        with self.assertRaises(ArchiveSecurityError):
            extract_archive(self.archive_path, self.dest)
        if os.path.isdir(self.dest):
            self.assertEqual(os.listdir(self.dest), [])

    # ---- normal use must still work ----

    def test_allows_unicode_filename(self):
        name = "caf\u00e9/na\u00efve_\u6587\u4ef6.txt"
        self._tar([{"name": name, "data": b"unicode ok"}])
        written = extract_archive(self.archive_path, self.dest)
        self.assertEqual(written, [name])

    def test_allows_dotdot_substring_filename(self):
        self._tar([
            {"name": "..bashrc_backup", "data": b"a"},
            {"name": "version..2.txt", "data": b"b"},
        ])
        written = extract_archive(self.archive_path, self.dest)
        self.assertEqual(written, ["..bashrc_backup", "version..2.txt"])

    def test_allows_nested_normal_directories(self):
        self._tar([
            {"name": "a", "type": "dir"},
            {"name": "a/b", "type": "dir"},
            {"name": "a/b/c.txt", "data": b"deep"},
        ])
        written = extract_archive(self.archive_path, self.dest)
        self.assertEqual(written, ["a/b/c.txt"])
        with open(os.path.join(self.dest, "a", "b", "c.txt"), "rb") as fh:
            self.assertEqual(fh.read(), b"deep")

    def test_empty_archive_returns_empty_list(self):
        self._tar([])
        written = extract_archive(self.archive_path, self.dest)
        self.assertEqual(written, [])


if __name__ == "__main__":
    unittest.main()
