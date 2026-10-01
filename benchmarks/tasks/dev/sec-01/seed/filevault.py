"""Serve files from a shared upload folder, by path."""
from pathlib import Path


class FileVault:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)

    def read(self, relative_path):
        path = self.base_dir / relative_path
        if not path.exists():
            raise FileNotFoundError(relative_path)
        if path.is_dir():
            raise IsADirectoryError(relative_path)
        return path.read_text(encoding="utf-8")
