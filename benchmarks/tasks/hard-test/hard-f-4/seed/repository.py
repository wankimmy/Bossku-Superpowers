"""The bookmark repository: the only place that reads/writes bookmarks.json.

``list_bookmarks()`` currently returns every bookmark, ordered by ``id``
ascending (which is also creation order, since ids are assigned in
increasing order and never reused - see ``storage.py``). It is
read-only: it never calls ``save``. Every dict ``list_bookmarks()``/
``get``/``add``/``visit`` hand back is a fresh copy (via
``Bookmark.to_dict()``), so mutating a returned dict - or its ``tags``
list - can never corrupt the repository's own state.

``add()`` is idempotent on ``url`` (exact, case-sensitive match - no
trailing-slash or scheme normalization): adding a url that's already
stored never creates a duplicate. Instead it *merges* into the existing
bookmark - any newly given tags are unioned in (appending only the
genuinely new ones, keeping their order), and the title is replaced
only if a non-empty title was explicitly given this call (an omitted or
empty title leaves the existing title untouched) - and leaves ``id``,
``added_at``, and ``visits`` exactly as they were. Calling ``add()``
twice in a row with identical arguments always leaves the bookmark in
the same state the first call did.

``visit()`` is the opposite: it is *not* idempotent - every call
increments ``visits`` by one more, on purpose, since each call
represents one more real visit.
"""
import time

from errors import NotFoundError
from models import Bookmark, normalize_tags
from storage import load, save


class BookmarkRepository:
    def __init__(self, path, clock=time.time):
        self.path = path
        self.clock = clock
        data = load(path)
        self._next_id = data["next_id"]
        self._bookmarks = {}
        for raw in data["bookmarks"]:
            bookmark = Bookmark.from_dict(raw)
            self._bookmarks[bookmark.id] = bookmark

    def _save(self):
        ordered = [self._bookmarks[i].to_dict() for i in sorted(self._bookmarks)]
        save(self.path, self._next_id, ordered)

    def _find_by_url(self, url):
        for bookmark in self._bookmarks.values():
            if bookmark.url == url:
                return bookmark
        return None

    def add(self, url, title=None, tags=None):
        existing = self._find_by_url(str(url).strip())
        if existing is not None:
            changed = False
            if title is not None and str(title).strip():
                existing.title = str(title).strip()
                changed = True
            for tag in normalize_tags(tags):
                if tag not in existing.tags:
                    existing.tags.append(tag)
                    changed = True
            if changed:
                self._save()
            return existing.to_dict()

        bookmark = Bookmark(id=self._next_id, url=url, added_at=_iso(self.clock()),
                             title=title, tags=tags)
        self._bookmarks[bookmark.id] = bookmark
        self._next_id += 1
        self._save()
        return bookmark.to_dict()

    def get(self, bookmark_id):
        bookmark = self._bookmarks.get(bookmark_id)
        if bookmark is None:
            raise NotFoundError(f"no bookmark with id {bookmark_id}")
        return bookmark.to_dict()

    def visit(self, bookmark_id):
        bookmark = self._bookmarks.get(bookmark_id)
        if bookmark is None:
            raise NotFoundError(f"no bookmark with id {bookmark_id}")
        bookmark.visits += 1
        self._save()
        return bookmark.to_dict()

    def delete(self, bookmark_id):
        if bookmark_id not in self._bookmarks:
            raise NotFoundError(f"no bookmark with id {bookmark_id}")
        del self._bookmarks[bookmark_id]
        self._save()

    def stats(self):
        return {
            "bookmarks": len(self._bookmarks),
            "total_visits": sum(b.visits for b in self._bookmarks.values()),
        }

    def list_bookmarks(self):
        return [self._bookmarks[i].to_dict() for i in sorted(self._bookmarks)]


def _iso(timestamp):
    import datetime

    return datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc).isoformat()
