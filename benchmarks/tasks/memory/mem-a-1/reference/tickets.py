"""Helpers for working with support ticket records."""

from typing import List, Optional


VALID_STATUSES = ("open", "pending", "resolved", "closed")

_STATUS_PRIORITY = {
    "open": "high",
    "pending": "medium",
    "resolved": "low",
    "closed": "low",
}

_OVERRIDE_PRIORITY = {
    1: "high",
    2: "medium",
    3: "low",
}


class Ticket:
    def __init__(self, id, subject, status):
        self.id = id
        self.subject = subject
        self.status = status


def load_tickets(records: List[dict]) -> List[Ticket]:
    tickets = []
    for record in records:
        tickets.append(Ticket(record["id"], record["subject"], record["status"]))
    return tickets


def count_by_status(tickets: List[Ticket]) -> dict:
    counts = dict((status, 0) for status in VALID_STATUSES)
    for ticket in tickets:
        counts[ticket.status] += 1
    return counts


def classify_priority(ticket: Ticket, override: Optional[int] = None) -> str:
    if override is not None:
        if override not in _OVERRIDE_PRIORITY:
            raise ValueError("override must be 1, 2, or 3")
        return _OVERRIDE_PRIORITY[override]
    if ticket.status not in _STATUS_PRIORITY:
        raise ValueError("unknown status: {!r}".format(ticket.status))
    return _STATUS_PRIORITY[ticket.status]
