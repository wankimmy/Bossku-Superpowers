import datetime
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PANTRY_JSON = ROOT / "pantry.json"
TODAY = datetime.date.today()


def _iso(days_from_today):
    return (TODAY + datetime.timedelta(days=days_from_today)).isoformat()


def run_cli(*args):
    return subprocess.run(
        [sys.executable, "pantry.py", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=20,
    )


def seed_pantry(items):
    PANTRY_JSON.write_text(json.dumps(items), encoding="utf-8")


class PantryTestCase(unittest.TestCase):
    def setUp(self):
        if PANTRY_JSON.exists():
            PANTRY_JSON.unlink()

    def tearDown(self):
        if PANTRY_JSON.exists():
            PANTRY_JSON.unlink()


class AddFunctionalTests(PantryTestCase):
    def test_add_creates_pantry_json_with_record(self):
        result = run_cli("add", "--name", "Milk", "--expires", _iso(5))
        self.assertEqual(result.returncode, 0)
        data = json.loads(PANTRY_JSON.read_text(encoding="utf-8"))
        self.assertEqual(data, [{"name": "Milk", "expires": _iso(5)}])

    def test_add_appends_multiple_items(self):
        run_cli("add", "--name", "Milk", "--expires", _iso(5))
        run_cli("add", "--name", "Eggs", "--expires", _iso(10))
        data = json.loads(PANTRY_JSON.read_text(encoding="utf-8"))
        self.assertEqual(len(data), 2)
        names = {item["name"] for item in data}
        self.assertEqual(names, {"Milk", "Eggs"})

    def test_add_prints_simple_confirmation(self):
        result = run_cli("add", "--name", "Yogurt", "--expires", _iso(3))
        self.assertIn("Yogurt", result.stdout)
        # add is a one-line confirmation, not a list -- it should not need
        # to be valid single-line JSON.
        self.assertEqual(len([l for l in result.stdout.splitlines() if l.strip()]), 1)


class ExpiringFunctionalTests(PantryTestCase):
    def setUp(self):
        super().setUp()
        seed_pantry([
            {"name": "Soon", "expires": _iso(1)},
            {"name": "Edge", "expires": _iso(5)},
            {"name": "TooLate", "expires": _iso(6)},
            {"name": "Already", "expires": _iso(-1)},
        ])

    def test_text_mode_includes_items_in_range(self):
        result = run_cli("expiring", "--within-days", "5")
        self.assertEqual(result.returncode, 0)
        self.assertIn("Soon", result.stdout)
        self.assertIn("Edge", result.stdout)

    def test_text_mode_excludes_items_out_of_range(self):
        result = run_cli("expiring", "--within-days", "5")
        self.assertNotIn("TooLate", result.stdout)
        self.assertNotIn("Already", result.stdout)

    def test_boundary_is_inclusive(self):
        result = run_cli("expiring", "--within-days", "5")
        self.assertIn("Edge", result.stdout)
        self.assertNotIn("TooLate", result.stdout)

    def test_no_matches_does_not_crash(self):
        seed_pantry([{"name": "Far", "expires": _iso(100)}])
        result = run_cli("expiring", "--within-days", "1")
        self.assertEqual(result.returncode, 0)


class JsonFlagRuleTests(PantryTestCase):
    """Project rule: list-printing subcommands support --json, printing one
    line of JSON with alphabetically-ordered object keys."""

    def setUp(self):
        super().setUp()
        seed_pantry([
            {"name": "Soon", "expires": _iso(1)},
            {"name": "Edge", "expires": _iso(5)},
            {"name": "TooLate", "expires": _iso(6)},
        ])

    def test_json_flag_is_accepted(self):
        result = run_cli("expiring", "--within-days", "5", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_json_output_is_single_line(self):
        result = run_cli("expiring", "--within-days", "5", "--json")
        lines = [l for l in result.stdout.splitlines() if l.strip()]
        self.assertEqual(len(lines), 1, f"expected exactly one output line, got {lines!r}")

    def test_json_output_parses_as_array(self):
        result = run_cli("expiring", "--within-days", "5", "--json")
        parsed = json.loads(result.stdout.strip())
        self.assertIsInstance(parsed, list)

    def test_json_objects_have_alphabetical_keys(self):
        result = run_cli("expiring", "--within-days", "5", "--json")
        line = result.stdout.strip()
        objects = json.loads(line, object_pairs_hook=lambda pairs: pairs)
        self.assertTrue(objects, "expected at least one matching item")
        for obj in objects:
            keys = [k for k, _ in obj]
            self.assertEqual(
                keys, sorted(keys),
                f"object keys {keys} are not in alphabetical order",
            )

    def test_json_objects_have_exactly_expected_keys(self):
        result = run_cli("expiring", "--within-days", "5", "--json")
        parsed = json.loads(result.stdout.strip())
        for obj in parsed:
            self.assertEqual(set(obj.keys()), {"name", "expires"})

    def test_json_output_sorted_soonest_first(self):
        result = run_cli("expiring", "--within-days", "5", "--json")
        parsed = json.loads(result.stdout.strip())
        names_in_order = [obj["name"] for obj in parsed]
        self.assertEqual(names_in_order, ["Soon", "Edge"])

    def test_json_empty_result_prints_empty_array_on_one_line(self):
        seed_pantry([{"name": "Far", "expires": _iso(100)}])
        result = run_cli("expiring", "--within-days", "1", "--json")
        lines = [l for l in result.stdout.splitlines() if l.strip()]
        self.assertEqual(lines, ["[]"])


if __name__ == "__main__":
    unittest.main()
