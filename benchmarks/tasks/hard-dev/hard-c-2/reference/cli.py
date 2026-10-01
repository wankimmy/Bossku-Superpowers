"""CLI: rank a list of passwords by strength."""

import sys

import checker
import report


def main(argv):
    passwords = list(argv)
    if not passwords:
        print("no passwords given")
        return
    ranked = report.rank_by_strength(passwords)
    strongest = ranked[0]
    strongest_score = checker.evaluate_password(strongest).score
    print(f"strongest: {strongest} ({strongest_score}/5)")
    print(report.summarize_many(ranked))


if __name__ == "__main__":
    main(sys.argv[1:])
