"""The ``Bookmark`` entity.

Fields:

- ``id``: positive ``int``, assigned by the repository and never reused
  (see ``storage.py``).
- ``url``: non-empty string that must start with ``http://`` or
  ``https://`` (case-insensitively).
- ``title``: non-empty string. If no title (or an empty/whitespace-only
  one) is given, it defaults to the bookmark's own ``url``.
- ``tags``: a list of non-empty strings. Each tag is stripped; empty
  tags are dropped; duplicates (exact, case-sensitive match) are
  dropped, keeping the first occurrence's position.
- ``added_at``: ISO 8601 timestamp string, set once when the bookmark
  is first created (see ``repository.add`` - re-adding the same url
  later never changes it).
- ``visits``: non-negative int, starts at ``0``.

``to_dict()`` always returns a *new* dict, with a *new* list for
``tags``, so callers can freely mutate what they get back without ever
corrupting the ``Bookmark``'s own state.
"""
from errors import ValidationError


def normalize_tags(tags):
    """Strip, drop-empty, and dedupe (first occurrence wins) a tag list.

    Shared by ``Bookmark.__init__`` and ``repository.add``'s merge-on-
    duplicate-url path, so both apply exactly the same tag rules.
    """
    seen = set()
    result = []
    for raw in tags or []:
        tag = str(raw).strip()
        if not tag or tag in seen:
            continue
        seen.add(tag)
        result.append(tag)
    return result


class Bookmark:
    __slots__ = ("id", "url", "title", "tags", "added_at", "visits")

    def __init__(self, id, url, added_at, title=None, tags=None, visits=0):
        url = str(url).strip()
        if not url:
            raise ValidationError("url is required")
        if not url.lower().startswith(("http://", "https://")):
            raise ValidationError(f"url must start with http:// or https://: {url!r}")

        title = str(title).strip() if title is not None else ""
        if not title:
            title = url

        self.id = id
        self.url = url
        self.title = title
        self.tags = normalize_tags(tags)
        self.added_at = added_at
        self.visits = int(visits)

    def to_dict(self):
        return {
            "id": self.id,
            "url": self.url,
            "title": self.title,
            "tags": list(self.tags),
            "added_at": self.added_at,
            "visits": self.visits,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            url=data["url"],
            added_at=data["added_at"],
            title=data.get("title"),
            tags=data.get("tags", []),
            visits=data.get("visits", 0),
        )
