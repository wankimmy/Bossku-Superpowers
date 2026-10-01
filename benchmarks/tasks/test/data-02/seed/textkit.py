"""A tiny multi-command text utility."""
import sys

USAGE = "usage: textkit <wordcount|filter|sort> [options]\n"
_COMMANDS = ("wordcount", "filter", "sort")


def main(argv, stdin, stdout):
    if not argv or argv[0] in ("-h", "--help"):
        sys.stdout.write(USAGE)
        return 0

    command, rest = argv[0], argv[1:]
    if command not in _COMMANDS:
        stdout.write(f"unknown command: {command}\n")
        return 1

    if command == "wordcount":
        text = stdin.read()
        lines = len(text.splitlines())
        words = len(text.split())
        chars = sum(len(line) for line in text.splitlines())
        stdout.write(f"{lines} lines, {words} words, {chars} chars\n")
        return 0

    if command == "filter":
        if not rest:
            stdout.write("filter requires a substring argument\n")
            return 1
        substring = rest[0]
        for line in stdin.read().splitlines():
            if substring in line:
                stdout.write(line + "\n")
        return 0

    # sort
    for line in sorted(stdin.read().splitlines()):
        stdout.write(line + "\n")
    return 0
