import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from static_files import read_file


class StaticFilesHappyPathTests(unittest.TestCase):
    def test_reads_top_level_and_nested_files(self):
        with tempfile.TemporaryDirectory() as root:
            with open(os.path.join(root, "notes.txt"), "wb") as fh:
                fh.write(b"hello world")
            os.makedirs(os.path.join(root, "sub"))
            with open(os.path.join(root, "sub", "inner.txt"), "wb") as fh:
                fh.write(b"nested content")

            self.assertEqual(read_file(root, "notes.txt"), b"hello world")
            self.assertEqual(
                read_file(root, "sub/inner.txt"), b"nested content"
            )


if __name__ == "__main__":
    unittest.main()
