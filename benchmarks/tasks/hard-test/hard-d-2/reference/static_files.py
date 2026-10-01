"""Serve files from a fixed content root for internal tooling."""
import os


class PathSecurityError(Exception):
    """Raised when a requested path is unsafe or cannot be safely served."""


MAX_DEPTH = 6


def _validate(requested_path):
    if any(ord(ch) < 0x20 for ch in requested_path):
        raise PathSecurityError(f"control character in path: {requested_path!r}")

    normalized = requested_path.replace("\\", "/")
    if normalized.startswith("/"):
        raise PathSecurityError(f"absolute path not allowed: {requested_path!r}")
    if len(normalized) > 1 and normalized[1] == ":":
        raise PathSecurityError(f"drive-letter path not allowed: {requested_path!r}")

    parts = [p for p in normalized.split("/") if p not in ("", ".")]
    if any(p == ".." for p in parts):
        raise PathSecurityError(f"'..' segment not allowed: {requested_path!r}")
    if not parts:
        raise PathSecurityError(
            f"path resolves to the content root: {requested_path!r}"
        )
    if len(parts) - 1 > MAX_DEPTH:
        raise PathSecurityError(f"path nested too deeply: {requested_path!r}")
    return parts


def read_file(root_dir, requested_path):
    """Read and return the bytes of a file under root_dir, safely."""
    parts = _validate(requested_path)

    root_abs = os.path.abspath(root_dir)
    full_abs = os.path.abspath(os.path.join(root_abs, *parts))
    if full_abs != root_abs and not full_abs.startswith(root_abs + os.sep):
        raise PathSecurityError(f"path escapes content root: {requested_path!r}")

    if os.path.isdir(full_abs):
        raise PathSecurityError(f"path is a directory: {requested_path!r}")
    if not os.path.isfile(full_abs):
        raise PathSecurityError(f"path does not exist: {requested_path!r}")

    with open(full_abs, "rb") as fh:
        return fh.read()
