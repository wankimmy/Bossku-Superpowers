"""The contact repository: the only place that reads/writes contacts.json.

``list_contacts()`` searches, filters, sorts, and (optionally)
paginates, always in that order: `q`/`tags`/`company` narrow the set
first, the *narrowed* result is sorted, and pagination slices the
sorted result last. ``total`` and ``pages`` in its return value always
describe the narrowed set as a whole - every page of the same
search/filter reports the same ``total``/``pages`` - never just the
items on the current page.

Passing ``page=None`` means "no pagination": every matching contact
comes back as a single page (``page=1``, ``page_size=total``,
``pages=1``, or ``pages=0`` when nothing matches).

``q`` is a case-insensitive substring search that matches if it is
found in `full_name` OR `email` OR `company` (never `phone`) - it is an
OR across those three fields, but an AND with every other filter
(`tags`, `company`) given alongside it.

Sorting: the default sort key is ``id`` ascending, which is also
creation order (ids are never reused - see ``storage.py``). For any
other sort key, ties are always broken by ``id`` ascending, in *both*
``asc`` and ``desc`` order - ``order`` only flips the primary key, never
the tie-break. ``name`` sorts by the *last whitespace-separated token*
of ``full_name``, lowercased (e.g. "Ada Lovelace" sorts under
"lovelace") - not by the full name. ``company`` sorts case-insensitively
by `company`, treating a contact with no company as if its company
were ``""`` (so it sorts before any named company in ascending order).

This method is read-only: it never calls ``save``. Every dict it,
``get``, ``add``, or ``tag`` hand back is a fresh copy, so mutating a
returned dict - or its ``tags`` list - can never corrupt the
repository's own state.
"""
import datetime
import math
import time

from errors import NotFoundError, ValidationError
from models import Contact
from storage import load, save

NO_FILTER = object()


class ContactRepository:
    def __init__(self, path, clock=time.time):
        self.path = path
        self.clock = clock
        data = load(path)
        self._next_id = data["next_id"]
        self._contacts = {}
        for raw in data["contacts"]:
            contact = Contact.from_dict(raw)
            self._contacts[contact.id] = contact

    def _save(self):
        ordered = [self._contacts[i].to_dict() for i in sorted(self._contacts)]
        save(self.path, self._next_id, ordered)

    def add(self, full_name, email=None, phone=None, company=None, tags=None):
        contact = Contact(
            id=self._next_id,
            full_name=full_name,
            created_at=_iso(self.clock()),
            email=email,
            phone=phone,
            company=company,
            tags=tags,
        )
        self._contacts[contact.id] = contact
        self._next_id += 1
        self._save()
        return contact.to_dict()

    def get(self, contact_id):
        contact = self._contacts.get(contact_id)
        if contact is None:
            raise NotFoundError(f"no contact with id {contact_id}")
        return contact.to_dict()

    def delete(self, contact_id):
        if contact_id not in self._contacts:
            raise NotFoundError(f"no contact with id {contact_id}")
        del self._contacts[contact_id]
        self._save()

    def tag(self, contact_id, tag_name):
        contact = self._contacts.get(contact_id)
        if contact is None:
            raise NotFoundError(f"no contact with id {contact_id}")
        tag_name = str(tag_name).strip()
        if not tag_name:
            raise ValidationError("tag must not be empty")
        if tag_name not in contact.tags:
            contact.tags.append(tag_name)
            self._save()
        return contact.to_dict()

    def count(self):
        return {"count": len(self._contacts)}

    def list_contacts(self, q=None, tags=(), company=NO_FILTER, sort_by="id",
                       order="asc", page=None, page_size=None):
        items = [self._contacts[i] for i in sorted(self._contacts)]

        if q:
            needle = q.lower()
            items = [c for c in items if _matches_search(c, needle)]
        for tag in tags:
            items = [c for c in items if tag in c.tags]
        if company is not NO_FILTER:
            target = (company or "").lower()
            items = [c for c in items if (c.company or "").lower() == target]

        # ``items`` is already id-ascending from the initial ``sorted()``
        # above; a single stable sort (with ``reverse`` only flipping the
        # primary key) is what keeps ties in id order in both directions.
        items.sort(key=_sort_key(sort_by), reverse=(order == "desc"))

        dicts = [c.to_dict() for c in items]
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


def _matches_search(contact, needle):
    for field in (contact.full_name, contact.email, contact.company):
        if field and needle in field.lower():
            return True
    return False


def _sort_key(sort_by):
    if sort_by == "name":
        return lambda c: c.full_name.strip().split()[-1].lower() if c.full_name.strip() else ""
    if sort_by == "company":
        return lambda c: (c.company or "").lower()
    return lambda c: getattr(c, sort_by)


def _iso(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc).isoformat()
