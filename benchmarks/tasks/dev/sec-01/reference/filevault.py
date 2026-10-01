"""Serve files from a shared upload folder, by path, without leaking anything outside it."""
from pathlib import Path


class FileVault:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir).resolve()

    def _resolve(self, relative_path):
        if not relative_path or Path(relative_path).is_absolute():
            raise PermissionError(f"unsafe path: {relative_path!r}")
        candidate = (self.base_dir / relative_path).resolve()
        try:
            candidate.relative_to(self.base_dir)
        except ValueError:
            raise PermissionError(f"unsafe path: {relative_path!r}") from None
        return candidate

    def read(self, relative_path):
        path = self._resolve(relative_path)
        if not path.exists():
            raise FileNotFoundError(relative_path)
        if path.is_dir():
            raise IsADirectoryError(relative_path)
        return path.read_text(encoding="utf-8")
