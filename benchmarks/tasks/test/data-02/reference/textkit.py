"""A tiny multi-command text utility."""

USAGE = "usage: textkit <wordcount|filter|sort> [options]\n"
_COMMANDS = ("wordcount", "filter", "sort")


def main(argv, stdin, stdout):
    if not argv or argv[0] in ("-h", "--help"):
        stdout.write(USAGE)
        return 0

    command, rest = argv[0], argv[1:]
    if command not in _COMMANDS:
        stdout.write(f"unknown command: {command}\n")
        return 2

    if command == "wordcount":
        if rest:
            stdout.write("wordcount takes no arguments\n")
            return 2
        text = stdin.read()
        lines = len(text.splitlines())
        words = len(text.split())
        chars = len(text)
        stdout.write(f"{lines} lines, {words} words, {chars} chars\n")
        return 0

    if command == "filter":
        if len(rest) != 1:
            stdout.write("filter requires a substring argument\n")
            return 2
        substring = rest[0]
        for line in stdin.read().splitlines():
            if substring in line:
                stdout.write(line + "\n")
        return 0

    # sort
    if len(rest) > 1 or (rest and rest[0] != "-r"):
        bad = rest[0] if rest else ""
        stdout.write(f"sort: unknown option: {bad}\n")
        return 2
    reverse = bool(rest)
    for line in sorted(stdin.read().splitlines(), reverse=reverse):
        stdout.write(line + "\n")
    return 0
