"""CLI for toggling and listing feature flags.

A thin wrapper around `flags.py`/`reporting.py` for ops/on-call use: flip
a flag during an incident, or check what's currently on, without needing
a Python shell.
"""

import sys

import flags
import reporting


def main(argv):
    """Entry point: `argv[0]` is one of "enable"/"disable"/"list", and for
    the first two, `argv[1]` is the flag name to act on."""
    if not argv:
        print("usage: cli.py <enable|disable|list> [flag_name]")
        return
    command = argv[0]
    if command == "enable":
        flags.enable(argv[1])
        print(f"enabled {argv[1]}")
    elif command == "disable":
        flags.disable(argv[1])
        print(f"disabled {argv[1]}")
    elif command == "list":
        print(reporting.build_report())
    else:
        print(f"unknown command: {command}")


if __name__ == "__main__":
    main(sys.argv[1:])
