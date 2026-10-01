"""The ``Contact`` entity.

Fields:

- ``id``: positive ``int``, assigned by the repository and never reused
  (see ``storage.py``).
- ``full_name``: non-empty string (leading/trailing whitespace stripped).
- ``email``: ``None``, or a non-empty string after stripping that
  contains exactly one ``@`` with a non-empty part on each side.
  Whitespace-only input is normalized to ``None``.
- ``phone``: ``None``, or a string normalized by removing spaces and
  dashes; what remains must be an optional leading ``+`` followed by one
  or more digits. Whitespace/dash-only input is normalized to ``None``.
- ``company``: a non-empty string, or ``None``. Whitespace-only input is
  normalized to ``None``.
- ``tags``: a list of non-empty strings. Each tag is stripped; empty
  tags are dropped; duplicates (exact, case-sensitive match) are
  dropped, keeping the first occurrence's position.
- ``created_at``: ISO 8601 timestamp string, set once at creation.

``to_dict()`` always returns a *new* dict, with a *new* list for
``tags``, so callers can freely mutate what they get back without ever
corrupting the ``Contact``'s own state.
"""
import re

from errors import ValidationError

_PHONE_RE = re.compile(r"^\+?\d+$")


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


def _normalize_email(email):
    if email is None:
        return None
    email = str(email).strip()
    if not email:
        return None
    parts = email.split("@")
    if len(parts) != 2 or not parts[0] or not parts[1]:
        raise ValidationError(f"invalid email: {email!r}")
    return email


def _normalize_phone(phone):
    if phone is None:
        return None
    stripped = str(phone).replace(" ", "").replace("-", "")
    if not stripped:
        return None
    if not _PHONE_RE.match(stripped):
        raise ValidationError(f"invalid phone: {phone!r}")
    return stripped


def _normalize_company(company):
    if company is None:
        return None
    company = str(company).strip()
    return company or None


class Contact:
    __slots__ = ("id", "full_name", "email", "phone", "company", "tags", "created_at")

    def __init__(self, id, full_name, created_at, email=None, phone=None,
                 company=None, tags=None):
        full_name = str(full_name).strip()
        if not full_name:
            raise ValidationError("full_name is required")

        self.id = id
        self.full_name = full_name
        self.email = _normalize_email(email)
        self.phone = _normalize_phone(phone)
        self.company = _normalize_company(company)
        self.tags = _normalize_tags(tags)
        self.created_at = created_at

    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "phone": self.phone,
            "company": self.company,
            "tags": list(self.tags),
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            full_name=data["full_name"],
            created_at=data["created_at"],
            email=data.get("email"),
            phone=data.get("phone"),
            company=data.get("company"),
            tags=data.get("tags", []),
        )
