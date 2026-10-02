"""Command-line tool for tracking pantry items and their expiry dates.

Project rule: any subcommand that prints a LIST of multiple items supports a
``--json`` flag. With ``--json`` it prints exactly one line of JSON (an
array of objects with alphabetically-ordered keys) instead of human text.
"""

import argparse
import datetime
import json
import os

PANTRY_FILE = "pantry.json"


def _load_items():
    if not os.path.exists(PANTRY_FILE):
        return []
    with open(PANTRY_FILE, "r", encoding="utf-8") as handle:
        return json.load(handle)


def _save_items(items):
    with open(PANTRY_FILE, "w", encoding="utf-8") as handle:
        json.dump(items, handle)


def cmd_add(args):
    items = _load_items()
    items.append({"name": args.name, "expires": args.expires})
    _save_items(items)
    print(f"Added {args.name}")


def cmd_expiring(args):
    today = datetime.date.today()
    items = _load_items()
    matches = []
    for item in items:
        expire_date = datetime.date.fromisoformat(item["expires"])
        days_until = (expire_date - today).days
        if 0 <= days_until <= args.within_days:
            matches.append(item)
    matches.sort(key=lambda item: item["expires"])

    if args.json:
        print(json.dumps(matches, sort_keys=True))
    else:
        for item in matches:
            print(f"{item['name']} expires {item['expires']}")


def build_parser():
    parser = argparse.ArgumentParser(prog="pantry")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("--name", required=True)
    add_parser.add_argument("--expires", required=True)
    add_parser.set_defaults(func=cmd_add)

    expiring_parser = subparsers.add_parser("expiring")
    expiring_parser.add_argument("--within-days", type=int, required=True)
    expiring_parser.add_argument("--json", action="store_true")
    expiring_parser.set_defaults(func=cmd_expiring)

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
