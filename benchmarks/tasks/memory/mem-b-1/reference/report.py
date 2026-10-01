"""Structured event reporting for the order importer.

This service runs under a log shipper that only understands single-line
JSON on stdout. Never call print() or the logging module directly from
anywhere else in this codebase -- route everything through report() so
every line written to stdout stays valid JSON.
"""

import json


def report(event, **fields):
    """Emit one JSON line to stdout describing `event` and return it."""
    payload = {"event": event}
    payload.update(fields)
    print(json.dumps(payload, sort_keys=True))
    return payload
