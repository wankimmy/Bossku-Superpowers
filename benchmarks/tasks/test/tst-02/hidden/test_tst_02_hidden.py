import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ORIGINAL_MODULE = ROOT / "original" / "ledger.py"
MUTANTS_DIR = ROOT / "mutants"
AGENT_TEST_FILE = ROOT / "test_ledger.py"
MODULE_NAME = "ledger"
TEST_MODULE_NAME = "test_ledger"
SUBPROCESS_TIMEOUT = 15


def _run_against(module_source):
    tmp = Path(tempfile.mkdtemp(prefix="ledger_mut_"))
    try:
        shutil.copyfile(module_source, tmp / f"{MODULE_NAME}.py")
        shutil.copyfile(AGENT_TEST_FILE, tmp / f"{TEST_MODULE_NAME}.py")
        try:
            proc = subprocess.run(
                [sys.executable, "-m", "unittest", "-v", TEST_MODULE_NAME],
                cwd=str(tmp),
                capture_output=True,
                text=True,
                timeout=SUBPROCESS_TIMEOUT,
            )
            return proc.returncode, proc.stdout + "\n" + proc.stderr
        except subprocess.TimeoutExpired as exc:
            out = (exc.stdout or "") + "\n" + (exc.stderr or "")
            return 1, out + "\n[subprocess timed out]"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def _test_count(output):
    m = re.search(r"Ran (\d+) tests?", output)
    return int(m.group(1)) if m else 0


class AgentTestSuiteQualityTests(unittest.TestCase):
    def test_passes_on_correct_module_with_enough_tests(self):
        rc, output = _run_against(ORIGINAL_MODULE)
        self.assertEqual(rc, 0, f"test_ledger.py did not pass against the correct module:\n{output}")
        count = _test_count(output)
        self.assertGreaterEqual(
            count, 5, f"expected at least 5 test methods in test_ledger.py, found {count}:\n{output}"
        )

    def _assert_catches(self, mutant_filename):
        rc, output = _run_against(MUTANTS_DIR / mutant_filename)
        self.assertNotEqual(rc, 0, f"test_ledger.py did not catch the bug in {mutant_filename}:\n{output}")

    def test_catches_withdraw_boundary_bug(self):
        self._assert_catches("m1_ledger.py")

    def test_catches_zero_amount_validation_bug(self):
        self._assert_catches("m2_ledger.py")

    def test_catches_void_last_inverted_restore(self):
        self._assert_catches("m3_ledger.py")

    def test_catches_totals_swapped(self):
        self._assert_catches("m4_ledger.py")

    def test_catches_largest_transaction_uses_min(self):
        self._assert_catches("m5_ledger.py")

    def test_catches_interest_percentage_bug(self):
        self._assert_catches("m6_ledger.py")

    def test_catches_transfer_order_bug(self):
        self._assert_catches("m7_ledger.py")

    def test_catches_history_not_copied(self):
        self._assert_catches("m8_ledger.py")


if __name__ == "__main__":
    unittest.main()
