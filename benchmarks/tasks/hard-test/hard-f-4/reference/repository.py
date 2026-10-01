"""The bookmark repository: the only place that reads/writes bookmarks.json.

``list_bookmarks()`` filters, sorts, and (optionally) paginates, always
in that order: filters are applied first, the *filtered* result is
sorted, and pagination slices the sorted result last. ``total`` and
``pages`` in its return value always describe the filtered set as a
whole - every page of the same filter reports the same ``total``/
``pages`` - never just the items on the current page.

Passing ``page=None`` means "no pagination": every matching bookmark
comes back as a single page (``page=1``, ``page_size=total``,
``pages=1``, or ``pages=0`` when nothing matches).

``tags`` + ``any_tag`` filter together: with ``any_tag=False`` (the
default), a bookmark must have **every** tag in ``tags`` (AND). With
``any_tag=True``, it only needs **at least one** of them (OR). With no
``tags`` at all, ``any_tag`` has nothing to flip and changes nothing.
``min_visits`` keeps only bookmarks with ``visits >= min_visits``.

Sorting: the default sort key is ``id`` ascending, which is also
creation order (ids are never reused - see ``storage.py``). For any
other sort key, ties are always broken by ``id`` ascending, in *both*
``asc`` and ``desc`` order - ``order`` only flips the primary key,
never the tie-break. ``title`` sorts case-insensitively.

This method is read-only: it never calls ``save``. Every dict it,
``get``, ``add``, or ``visit`` hand back is a fresh copy, so mutating a
returned dict - or its ``tags`` list - can never corrupt the
repository's own state.

``add()`` and ``visit()`` keep the same (pre-existing) behavior
documented in the module docstring below: ``add`` is idempotent and
merges on a duplicate url, ``visit`` is not idempotent and increments
every time.
"""
import math
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

    def list_bookmarks(self, tags=(), any_tag=False, min_visits=None,
                        sort_by="id", order="asc", page=None, page_size=None):
        items = [self._bookmarks[i] for i in sorted(self._bookmarks)]

        if tags:
            tag_set = set(tags)
            if any_tag:
                items = [b for b in items if tag_set & set(b.tags)]
            else:
                items = [b for b in items if tag_set.issubset(b.tags)]
        if min_visits is not None:
            items = [b for b in items if b.visits >= min_visits]

        # ``items`` is already id-ascending from the initial ``sorted()``
        # above; a single stable sort (with ``reverse`` only flipping the
        # primary key) is what keeps ties in id order in both directions.
        items.sort(key=_sort_key(sort_by), reverse=(order == "desc"))

        dicts = [b.to_dict() for b in items]
        total = len(dicts)

        if page is None:
            return {
                "items": dicts,
                "total": total,
                "page": 1,
                "page_size": total,
                "pages": 1 if total else 0,
            }

        pages = math.ceil(total / page_size) if total else 0
        start = (page - 1) * page_size
        page_items = dicts[start:start + page_size]
        return {
            "items": page_items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "pages": pages,
        }


def _sort_key(sort_by):
    if sort_by == "title":
        return lambda b: b.title.lower()
    return lambda b: getattr(b, sort_by)


def _iso(timestamp):
    import datetime

    return datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc).isoformat()
