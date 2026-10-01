"""CLI for toggling and listing feature flags."""

import sys

import flags
import reporting


def main(argv, registry=None):
    reg = registry if registry is not None else flags.default_registry
    if not argv:
        print("usage: cli.py <enable|disable|list> [flag_name]")
        return
    command = argv[0]
    if command == "enable":
        reg.enable(argv[1])
        print(f"enabled {argv[1]}")
    elif command == "disable":
        reg.disable(argv[1])
        print(f"disabled {argv[1]}")
    elif command == "list":
        print(reporting.build_report(reg))
    else:
        print(f"unknown command: {command}")


if __name__ == "__main__":
    main(sys.argv[1:])
