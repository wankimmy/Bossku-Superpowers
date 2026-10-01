"""Shared constants.

``STATUSES`` / ``PRIORITIES`` are the only legal values for those two
``Issue`` fields (see ``models.py``). ``EXIT_CODES`` maps each error
category (see ``errors.py``) to the process exit code the CLI uses for it;
``SUCCESS`` is the exit code for every command that completes normally,
including a ``list`` whose filters happen to match nothing (an empty
result is not an error).

``PRIORITY_RANK`` is the severity order used to sort by ``priority``:
``low < medium < high``. It is *not* alphabetical order (alphabetically
``high < low < medium``).
"""

STATUSES = ("open", "in_progress", "closed")
PRIORITIES = ("low", "medium", "high")

DEFAULT_STATUS = "open"
DEFAULT_PRIORITY = "medium"

PRIORITY_RANK = {"low": 0, "medium": 1, "high": 2}

SUCCESS = 0
EXIT_CODES = {
    "validation": 2,
    "not_found": 3,
    "storage": 4,
}
