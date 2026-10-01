"""Tiny CLI that replays a saved chat log.

Log file format: one message per line, "HH:MM|author|text". This is a
deliberately narrow format - no dates, no multi-line messages, no escaping
of "|" in the text - good enough for quickly eyeballing a conversation
that was dumped out of some other system.
"""

import sys
from datetime import datetime

import render


def _parse_line(line):
    """Parse one "HH:MM|author|text" log line into its three parts."""
    hhmm, author, text = line.rstrip("\n").split("|", 2)
    timestamp = datetime.strptime(hhmm, "%H:%M")
    return author, text, timestamp


def main(argv):
    """Entry point: `argv` is `[logfile]`. Reads the whole log up front,
    then prints one rendered line per message, in file order."""
    if not argv:
        print("usage: cli.py <logfile>")
        return
    with open(argv[0], encoding="utf-8") as handle:
        entries = [_parse_line(line) for line in handle if line.strip()]
    for author, text, timestamp in entries:
        # Narrower than the default width, since terminal logs tend to get
        # piped through other tools that wrap long lines badly anyway.
        print(render.render_message(author, text, timestamp, 40))


if __name__ == "__main__":
    main(sys.argv[1:])
