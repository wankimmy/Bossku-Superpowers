"""Serve files from a fixed content root for internal tooling."""
import os


class PathSecurityError(Exception):
    """Raised when a requested path is unsafe or cannot be safely served."""


def read_file(root_dir, requested_path):
    """Read and return the bytes of a file under root_dir."""
    full_path = os.path.join(root_dir, requested_path)
    with open(full_path, "rb") as fh:
        return fh.read()
