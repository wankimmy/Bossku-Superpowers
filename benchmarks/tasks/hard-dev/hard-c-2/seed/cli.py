"""CLI: rank a list of passwords by strength.

Handy for auditing a batch of passwords pulled from somewhere else (an old
export, a list of defaults, whatever) without writing a one-off script
each time.
"""

import sys

import checker
import report


def main(argv):
    """Entry point: `argv` is the list of passwords to rank, taken
    straight from the command line. Prints a one-line headline naming the
    strongest password, followed by a full report of every password."""
    passwords = list(argv)
    if not passwords:
        print("no passwords given")
        return
    ranked = report.rank_by_strength(passwords)
    strongest = ranked[0]
    strongest_score, _ = checker.check_strength(strongest)
    print(f"strongest: {strongest} ({strongest_score}/5)")
    print(report.summarize_many(ranked))


if __name__ == "__main__":
    main(sys.argv[1:])
