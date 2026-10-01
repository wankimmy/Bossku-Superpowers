"""CLI: redact a file and print the result plus match counts.

Files ending in ".bin" are read and redacted as raw bytes; anything else is
read and redacted as text.
"""

import sys

from redactor import redact


def main(argv):
    if not argv:
        print("usage: cli.py <file>")
        return
    path = argv[0]
    if path.endswith(".bin"):
        with open(path, "rb") as handle:
            content = handle.read()
    else:
        with open(path, "r", encoding="utf-8") as handle:
            content = handle.read()
    result, counts = redact(content)
    if isinstance(result, bytes):
        result = result.decode("utf-8")
    print(f"redacted: {result}")
    for name in sorted(counts):
        print(f"{name}: {counts[name]}")


if __name__ == "__main__":
    main(sys.argv[1:])
