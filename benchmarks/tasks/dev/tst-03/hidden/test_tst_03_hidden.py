import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ORIGINAL_MODULE = ROOT / "original" / "calc.py"
MUTANTS_DIR = ROOT / "mutants"
AGENT_TEST_FILE = ROOT / "test_calc.py"
MODULE_NAME = "calc"
TEST_MODULE_NAME = "test_calc"
SUBPROCESS_TIMEOUT = 15


def _run_against(module_source):
    tmp = Path(tempfile.mkdtemp(prefix="calc_mut_"))
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
        self.assertEqual(rc, 0, f"test_calc.py did not pass against the correct module:\n{output}")
        count = _test_count(output)
        self.assertGreaterEqual(
            count, 5, f"expected at least 5 test methods in test_calc.py, found {count}:\n{output}"
        )

    def _assert_catches(self, mutant_filename):
        rc, output = _run_against(MUTANTS_DIR / mutant_filename)
        self.assertNotEqual(rc, 0, f"test_calc.py did not catch the bug in {mutant_filename}:\n{output}")

    def test_catches_subtraction_direction_bug(self):
        self._assert_catches("m1_calc.py")

    def test_catches_division_truncation_bug(self):
        self._assert_catches("m2_calc.py")

    def test_catches_weakened_division_by_zero_check(self):
        self._assert_catches("m3_calc.py")

    def test_catches_missing_unary_minus(self):
        self._assert_catches("m4_calc.py")

    def test_catches_missing_paren_balance_check(self):
        self._assert_catches("m5_calc.py")

    def test_catches_missing_decimal_support(self):
        self._assert_catches("m6_calc.py")

    def test_catches_missing_trailing_token_check(self):
        self._assert_catches("m7_calc.py")

    def test_catches_swapped_mul_div(self):
        self._assert_catches("m8_calc.py")


if __name__ == "__main__":
    unittest.main()
