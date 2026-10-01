"""Tiny CLI that replays a saved chat log.

Log file format: one message per line, "HH:MM|author|text".
"""

import sys
from datetime import datetime

import render


def _parse_line(line):
    hhmm, author, text = line.rstrip("\n").split("|", 2)
    timestamp = datetime.strptime(hhmm, "%H:%M")
    return author, text, timestamp


def main(argv):
    if not argv:
        print("usage: cli.py <logfile>")
        return
    with open(argv[0], encoding="utf-8") as handle:
        entries = [_parse_line(line) for line in handle if line.strip()]
    for author, text, timestamp in entries:
        print(render.render_message(author, text, timestamp, 40))


if __name__ == "__main__":
    main(sys.argv[1:])
