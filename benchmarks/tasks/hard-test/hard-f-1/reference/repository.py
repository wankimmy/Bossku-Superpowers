"""The issue repository: the only place that reads/writes issues.json.

``list_issues()`` filters, sorts, and (optionally) paginates, always in
that order: filters are applied first, the *filtered* result is sorted,
and pagination slices the sorted result last. ``total`` and ``pages`` in
its return value always describe the filtered set as a whole - every page
of the same filter reports the same ``total``/``pages`` - never just the
items on the current page.

Passing ``page=None`` means "no pagination": every matching issue comes
back as a single page (``page=1``, ``page_size=total``, ``pages=1``, or
``pages=0`` when nothing matches).

Sorting: the default sort key is ``id`` ascending, which is also creation
order (ids are never reused - see ``storage.py``). For any other sort key,
ties are always broken by ``id`` ascending, in *both* ``asc`` and ``desc``
order - ``order`` only flips the primary key, never the tie-break.
``priority`` sorts by severity (``constants.PRIORITY_RANK``:
``low < medium < high``), not alphabetically.

This method is read-only: it never calls ``save``. Every dict it, ``get``,
``add``, or ``close`` hand back is a fresh copy, so mutating a returned
dict - or its ``tags`` list - can never corrupt the repository's own
state.
"""
import datetime
import math
import time

from constants import PRIORITY_RANK
from errors import NotFoundError
from models import Issue
from storage import load, save

NO_FILTER = object()


class IssueRepository:
    def __init__(self, path, clock=time.time):
        self.path = path
        self.clock = clock
        data = load(path)
        self._next_id = data["next_id"]
        self._issues = {}
        for raw in data["issues"]:
            issue = Issue.from_dict(raw)
            self._issues[issue.id] = issue

    def _save(self):
        ordered = [self._issues[i].to_dict() for i in sorted(self._issues)]
        save(self.path, self._next_id, ordered)

    def add(self, title, priority=None, assignee=None, tags=None):
        kwargs = {}
        if priority is not None:
            kwargs["priority"] = priority
        issue = Issue(
            id=self._next_id,
            title=title,
            created_at=_iso(self.clock()),
            assignee=assignee,
            tags=tags,
            **kwargs,
        )
        self._issues[issue.id] = issue
        self._next_id += 1
        self._save()
        return issue.to_dict()

    def get(self, issue_id):
        issue = self._issues.get(issue_id)
        if issue is None:
            raise NotFoundError(f"no issue with id {issue_id}")
        return issue.to_dict()

    def close(self, issue_id):
        issue = self._issues.get(issue_id)
        if issue is None:
            raise NotFoundError(f"no issue with id {issue_id}")
        issue.status = "closed"
        self._save()
        return issue.to_dict()

    def delete(self, issue_id):
        if issue_id not in self._issues:
            raise NotFoundError(f"no issue with id {issue_id}")
        del self._issues[issue_id]
        self._save()

    def list_issues(self, status=None, priority=None, assignee=NO_FILTER,
                     tags=(), sort_by="id", order="asc", page=None, page_size=None):
        items = [self._issues[i] for i in sorted(self._issues)]

        if status is not None:
            items = [i for i in items if i.status == status]
        if priority is not None:
            items = [i for i in items if i.priority == priority]
        if assignee is not NO_FILTER:
            items = [i for i in items if i.assignee == assignee]
        for tag in tags:
            items = [i for i in items if tag in i.tags]

        # ``items`` is already id-ascending from the initial ``sorted()``
        # above; a single stable sort (with ``reverse`` only flipping the
        # primary key) is what keeps ties in id order in both directions.
        items.sort(key=_sort_key(sort_by), reverse=(order == "desc"))

        dicts = [i.to_dict() for i in items]
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

    def summary(self):
        counts = {status: 0 for status in ("open", "in_progress", "closed")}
        for issue in self._issues.values():
            counts[issue.status] += 1
        counts["total"] = len(self._issues)
        return counts


def _sort_key(sort_by):
    if sort_by == "priority":
        return lambda issue: PRIORITY_RANK[issue.priority]
    return lambda issue: getattr(issue, sort_by)


def _iso(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc).isoformat()
