"""Extract tar archives uploaded by users into a scratch workspace."""
import os
import tarfile


class ArchiveSecurityError(Exception):
    """Raised when a tar archive contains unsafe content and must be rejected."""


def extract_archive(archive_path, dest_dir):
    """Extract every member of the tar archive at archive_path into dest_dir.

    Returns the sorted list of relative paths that were written.
    """
    os.makedirs(dest_dir, exist_ok=True)
    with tarfile.open(archive_path) as tar:
        tar.extractall(dest_dir)
    written = []
    for root, _dirs, files in os.walk(dest_dir):
        for fname in files:
            full = os.path.join(root, fname)
            written.append(os.path.relpath(full, dest_dir).replace(os.sep, "/"))
    return sorted(written)
