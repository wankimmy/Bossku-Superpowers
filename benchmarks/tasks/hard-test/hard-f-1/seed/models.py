"""The ``Issue`` entity.

Fields:

- ``id``: positive ``int``, assigned by the repository and never reused
  (see ``storage.py``).
- ``title``: non-empty string (leading/trailing whitespace stripped).
- ``status``: one of ``constants.STATUSES``. Defaults to ``"open"``.
- ``priority``: one of ``constants.PRIORITIES``. Defaults to ``"medium"``.
- ``assignee``: a non-empty string, or ``None`` if unassigned. An empty or
  whitespace-only string is normalized to ``None``.
- ``tags``: a list of non-empty strings. Each tag is stripped; empty tags
  are dropped; duplicates (exact, case-sensitive match) are dropped,
  keeping the first occurrence's position.
- ``created_at``: ISO 8601 timestamp string, set once at creation.

``to_dict()`` always returns a *new* dict, with a *new* list for ``tags``,
so callers can freely mutate what they get back without ever corrupting
the ``Issue``'s own state.
"""
from errors import ValidationError
from constants import STATUSES, PRIORITIES, DEFAULT_STATUS, DEFAULT_PRIORITY


def _normalize_tags(tags):
    seen = set()
    result = []
    for raw in tags or []:
        tag = str(raw).strip()
        if not tag or tag in seen:
            continue
        seen.add(tag)
        result.append(tag)
    return result


class Issue:
    __slots__ = ("id", "title", "status", "priority", "assignee", "tags", "created_at")

    def __init__(self, id, title, created_at, status=DEFAULT_STATUS,
                 priority=DEFAULT_PRIORITY, assignee=None, tags=None):
        title = str(title).strip()
        if not title:
            raise ValidationError("title is required")
        if status not in STATUSES:
            raise ValidationError(f"unknown status: {status!r}")
        if priority not in PRIORITIES:
            raise ValidationError(f"unknown priority: {priority!r}")

        self.id = id
        self.title = title
        self.status = status
        self.priority = priority
        self.assignee = (str(assignee).strip() or None) if assignee is not None else None
        self.tags = _normalize_tags(tags)
        self.created_at = created_at

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "status": self.status,
            "priority": self.priority,
            "assignee": self.assignee,
            "tags": list(self.tags),
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            title=data["title"],
            created_at=data["created_at"],
            status=data.get("status", DEFAULT_STATUS),
            priority=data.get("priority", DEFAULT_PRIORITY),
            assignee=data.get("assignee"),
            tags=data.get("tags", []),
        )
