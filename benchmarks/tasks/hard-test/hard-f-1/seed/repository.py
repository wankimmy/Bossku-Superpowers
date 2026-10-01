"""The issue repository: the only place that reads/writes issues.json.

``list_issues()`` currently returns every issue, ordered by ``id``
ascending (which is also creation order, since ids are assigned in
increasing order and never reused - see ``storage.py``). It is read-only:
it never calls ``save``. Every dict ``list_issues()``/``get``/``add``/
``close`` hand back is a fresh copy (via ``Issue.to_dict()``), so mutating
a returned dict - or its ``tags`` list - can never corrupt the
repository's own state.
"""
import datetime
import time

from errors import NotFoundError
from models import Issue
from storage import load, save


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

    def list_issues(self):
        return [self._issues[i].to_dict() for i in sorted(self._issues)]

    def summary(self):
        counts = {status: 0 for status in ("open", "in_progress", "closed")}
        for issue in self._issues.values():
            counts[issue.status] += 1
        counts["total"] = len(self._issues)
        return counts


def _iso(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc).isoformat()
