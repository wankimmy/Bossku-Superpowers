"""The contact repository: the only place that reads/writes contacts.json.

``list_contacts()`` currently returns every contact, ordered by ``id``
ascending (which is also creation order, since ids are assigned in
increasing order and never reused - see ``storage.py``). It is
read-only: it never calls ``save``. Every dict ``list_contacts()``/
``get``/``add``/``tag`` hand back is a fresh copy (via
``Contact.to_dict()``), so mutating a returned dict - or its ``tags``
list - can never corrupt the repository's own state.

``tag()`` is idempotent: adding a tag a contact already has is a no-op
(no duplicate, no error) - calling it twice in a row with the same
arguments leaves the contact exactly as the first call did.
"""
import datetime
import time

from errors import NotFoundError, ValidationError
from models import Contact
from storage import load, save


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

    def list_contacts(self):
        return [self._contacts[i].to_dict() for i in sorted(self._contacts)]


def _iso(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc).isoformat()
