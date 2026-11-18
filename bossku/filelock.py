"""One writer at a time for a file that several processes append to: the notes files and the learn ledger.

On Windows an append is "seek to the end, then write". Two processes can pick the same end, and one entry then
overwrites the other. `locked` makes the writers that use it take turns.

The lock is on the file itself, so two writers meet the same lock whatever path each used to reach the file. No
lock file is left in the folder, which may be an Obsidian vault or OneDrive, and the OS drops the lock when the
process dies. A program that does not use `locked` is not held back: it can still read and write the file.

The lock works between processes of one operating system. A Windows program and a WSL program do not see each
other's lock, and neither do two computers that sync one folder: those can still write at the same moment.
"""

from __future__ import annotations

import os
import time
from contextlib import contextmanager, suppress
from pathlib import Path

LOCK_WAIT = 10.0   # seconds a writer waits for its turn; one append takes a few milliseconds
# A Windows lock also stops other processes reading the locked bytes, so the locked byte is far past the end of
# the file. Readers, editors and sync tools never touch it.
_LOCK_BYTE = 1 << 30


def _lock(fd: int, take: bool) -> None:
    """Take or drop the lock without waiting. A lock held elsewhere raises BlockingIOError or PermissionError."""
    if os.name == "nt":
        import msvcrt
        os.lseek(fd, _LOCK_BYTE, os.SEEK_SET)
        msvcrt.locking(fd, msvcrt.LK_NBLCK if take else msvcrt.LK_UNLCK, 1)
    else:
        import fcntl
        fcntl.flock(fd, (fcntl.LOCK_EX | fcntl.LOCK_NB) if take else fcntl.LOCK_UN)


@contextmanager
def locked(path: Path):
    """Run the block while holding the write lock of `path`. The file is created when it is missing.

    A writer that does not get its turn within LOCK_WAIT seconds raises TimeoutError, and the block does not run.
    On a file system that has no locks the block runs without one, as it did before this lock existed: refusing
    every write there would lose more notes than the race does.
    """
    fd = os.open(path, os.O_WRONLY | os.O_CREAT, 0o666)
    try:
        held, deadline = False, time.monotonic() + LOCK_WAIT
        while not held:
            try:
                _lock(fd, True)
                held = True
            except (BlockingIOError, PermissionError):
                if time.monotonic() >= deadline:
                    raise TimeoutError(f"{path} is still locked by another writer after {LOCK_WAIT:g} seconds; "
                                       "nothing was written to it, try again") from None
                time.sleep(0.02)
            except OSError:
                break
        try:
            yield
        finally:
            if held:
                with suppress(OSError):   # closing the file drops the lock as well
                    _lock(fd, False)
    finally:
        os.close(fd)
