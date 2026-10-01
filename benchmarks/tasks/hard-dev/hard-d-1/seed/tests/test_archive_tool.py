import io
import os
import sys
import tarfile
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from archive_tool import extract_archive


def _make_tar(path, entries):
    """entries: list of (name, bytes) for regular files."""
    with tarfile.open(path, "w") as tar:
        for name, data in entries:
            info = tarfile.TarInfo(name=name)
            info.size = len(data)
            tar.addfile(info, io.BytesIO(data))


class ArchiveToolHappyPathTests(unittest.TestCase):
    def test_extracts_regular_files_and_nested_dirs(self):
        with tempfile.TemporaryDirectory() as tmp:
            archive_path = os.path.join(tmp, "bundle.tar")
            _make_tar(archive_path, [
                ("readme.txt", b"hello"),
                ("src/main.py", b"print('hi')\n"),
            ])
            dest = os.path.join(tmp, "dest")
            written = extract_archive(archive_path, dest)
            self.assertEqual(written, ["readme.txt", "src/main.py"])
            with open(os.path.join(dest, "readme.txt"), "rb") as fh:
                self.assertEqual(fh.read(), b"hello")
            with open(os.path.join(dest, "src", "main.py"), "rb") as fh:
                self.assertEqual(fh.read(), b"print('hi')\n")


if __name__ == "__main__":
    unittest.main()
