"""Extract tar archives uploaded by users into a scratch workspace."""
import os
import tarfile


class ArchiveSecurityError(Exception):
    """Raised when a tar archive contains unsafe content and must be rejected."""


MAX_MEMBERS = 50
MAX_SINGLE_FILE_BYTES = 2 * 1024 * 1024
MAX_TOTAL_BYTES = 6 * 1024 * 1024
MAX_DEPTH = 8


def _safe_relative_parts(name):
    """Split a member name into safe path components, or raise.

    Rejects absolute paths (POSIX or a Windows drive letter) and any
    '..' component that would climb above the destination root, while
    treating '/' and '\\' as equivalent separators and ignoring '.'
    and empty components.
    """
    normalized = name.replace("\\", "/")
    if normalized.startswith("/"):
        raise ArchiveSecurityError(f"absolute path not allowed: {name!r}")
    if len(normalized) > 1 and normalized[1] == ":":
        raise ArchiveSecurityError(f"drive-letter path not allowed: {name!r}")
    parts = []
    for part in normalized.split("/"):
        if part in ("", "."):
            continue
        if part == "..":
            if not parts:
                raise ArchiveSecurityError(f"path escapes destination: {name!r}")
            parts.pop()
        else:
            parts.append(part)
    if not parts:
        raise ArchiveSecurityError(f"path resolves to the destination root: {name!r}")
    return parts


def extract_archive(archive_path, dest_dir):
    """Safely extract every member of a tar archive into dest_dir.

    Validates every member before writing anything; if any member is
    unsafe the whole archive is rejected (raising ArchiveSecurityError)
    and dest_dir is left without any of the archive's files.
    Returns the sorted list of relative paths that were written.
    """
    os.makedirs(dest_dir, exist_ok=True)
    dest_root = os.path.realpath(dest_dir)

    with tarfile.open(archive_path) as tar:
        members = tar.getmembers()
        if len(members) > MAX_MEMBERS:
            raise ArchiveSecurityError(
                f"archive has {len(members)} members, more than the "
                f"{MAX_MEMBERS} allowed"
            )

        plan = []
        total_size = 0
        for member in members:
            is_dir = member.isdir()
            is_file = member.isfile()
            if not (is_dir or is_file):
                raise ArchiveSecurityError(
                    f"member {member.name!r} has unsupported type {member.type!r}"
                )

            parts = _safe_relative_parts(member.name)
            depth = len(parts) - 1
            if depth > MAX_DEPTH:
                raise ArchiveSecurityError(
                    f"member {member.name!r} is nested more than "
                    f"{MAX_DEPTH} directories deep"
                )

            if is_file:
                if member.size > MAX_SINGLE_FILE_BYTES:
                    raise ArchiveSecurityError(
                        f"member {member.name!r} is {member.size} bytes, more "
                        f"than the {MAX_SINGLE_FILE_BYTES} allowed"
                    )
                total_size += member.size

            target = os.path.join(dest_root, *parts)
            target_real = os.path.realpath(target)
            if target_real != dest_root and not target_real.startswith(
                dest_root + os.sep
            ):
                raise ArchiveSecurityError(
                    f"member {member.name!r} escapes destination"
                )
            plan.append((member, parts, is_dir, target))

        if total_size > MAX_TOTAL_BYTES:
            raise ArchiveSecurityError(
                f"archive total size {total_size} exceeds the "
                f"{MAX_TOTAL_BYTES} allowed"
            )

        written = []
        for member, parts, is_dir, target in plan:
            if is_dir:
                os.makedirs(target, exist_ok=True)
            else:
                os.makedirs(os.path.dirname(target), exist_ok=True)
                fileobj = tar.extractfile(member)
                data = fileobj.read() if fileobj is not None else b""
                with open(target, "wb") as fh:
                    fh.write(data)
                written.append("/".join(parts))
    return sorted(written)
