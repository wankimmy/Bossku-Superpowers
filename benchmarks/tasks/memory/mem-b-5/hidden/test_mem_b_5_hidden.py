import ast
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HIDDEN_FILENAME = Path(__file__).name


def _project_py_files():
    files = []
    for path in sorted(ROOT.rglob("*.py")):
        if path.name == HIDDEN_FILENAME:
            continue
        if "tests" in path.relative_to(ROOT).parts[:-1]:
            continue
        files.append(path)
    return files


def _call_func_name(call_node):
    func = call_node.func
    if isinstance(func, ast.Name):
        return func.id
    if isinstance(func, ast.Attribute):
        return func.attr
    return None


class BannedPatternRuleTests(unittest.TestCase):
    """The project rule: no eval/exec, no pickle, no subprocess shell=True."""

    def test_no_eval_calls_anywhere(self):
        for path in _project_py_files():
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and _call_func_name(node) == "eval":
                    self.fail(f"{path.name} calls eval(...)")

    def test_no_exec_calls_anywhere(self):
        for path in _project_py_files():
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and _call_func_name(node) == "exec":
                    self.fail(f"{path.name} calls exec(...)")

    def test_no_pickle_module_anywhere(self):
        for path in _project_py_files():
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    names = {alias.name for alias in node.names}
                    self.assertNotIn("pickle", names, f"{path.name} imports pickle")
                if isinstance(node, ast.ImportFrom):
                    self.assertNotEqual(
                        node.module, "pickle", f"{path.name} imports from pickle"
                    )

    def test_no_subprocess_shell_true_anywhere(self):
        for path in _project_py_files():
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if not isinstance(node, ast.Call):
                    continue
                for kw in node.keywords:
                    if kw.arg == "shell" and isinstance(kw.value, ast.Constant) and kw.value.value is True:
                        self.fail(f"{path.name} calls something with shell=True")

    def test_formula_rejects_sandbox_escape_attempt(self):
        # The real discriminator: eval()/exec() would happily execute
        # this and return a harmless-looking string; a safe AST-walking
        # evaluator has no Call/Attribute support and must reject it.
        from stats import StatSheet

        sheet = StatSheet()
        with self.assertRaises(Exception):
            # Rejecting the formula when it is stored, or when it is evaluated, are both fine.
            sheet.set_formula("danger", "__import__('os').name")
            sheet.value_of("danger")

    def test_formula_rejects_operators_outside_the_pinned_grammar(self):
        # Only +, -, *, / and parentheses were asked for; ** is not in
        # that grammar. A real eval() would compute it anyway (8).
        from stats import StatSheet

        sheet = StatSheet()
        with self.assertRaises(Exception):
            # Rejecting the formula when it is stored, or when it is evaluated, are both fine.
            sheet.set_formula("pw", "2 ** 3")
            sheet.value_of("pw")


class StatSheetFunctionalityTests(unittest.TestCase):
    def test_set_and_get_cell_round_trip(self):
        from stats import StatSheet

        sheet = StatSheet()
        sheet.set_cell("points", 10)
        self.assertEqual(sheet.get_cell("points"), 10)

    def test_total_sums_plain_cells(self):
        from stats import StatSheet

        sheet = StatSheet()
        sheet.set_cell("points", 10)
        sheet.set_cell("rebounds", 4)
        self.assertEqual(sheet.total(), 14)

    def test_set_cell_overwrites_previous_value(self):
        from stats import StatSheet

        sheet = StatSheet()
        sheet.set_cell("points", 10)
        sheet.set_cell("points", 20)
        self.assertEqual(sheet.get_cell("points"), 20)

    def test_formula_simple_addition(self):
        from stats import StatSheet

        sheet = StatSheet()
        sheet.set_cell("a", 2)
        sheet.set_cell("b", 3)
        sheet.set_formula("c", "a + b")
        self.assertEqual(sheet.value_of("c"), 5)

    def test_formula_respects_operator_precedence(self):
        from stats import StatSheet

        sheet = StatSheet()
        sheet.set_cell("points", 10)
        sheet.set_cell("rebounds", 4)
        sheet.set_formula("fp", "points + rebounds * 2")
        self.assertEqual(sheet.value_of("fp"), 18)

    def test_formula_parentheses_override_precedence(self):
        from stats import StatSheet

        sheet = StatSheet()
        sheet.set_cell("points", 10)
        sheet.set_cell("rebounds", 4)
        sheet.set_formula("fp2", "(points + rebounds) * 2")
        self.assertEqual(sheet.value_of("fp2"), 28)

    def test_formula_can_reference_another_formula_cell(self):
        from stats import StatSheet

        sheet = StatSheet()
        sheet.set_cell("points", 10)
        sheet.set_cell("rebounds", 4)
        sheet.set_formula("fp", "points + rebounds * 2")
        sheet.set_formula("chain", "fp * 2")
        self.assertEqual(sheet.value_of("chain"), 36)

    def test_formula_division(self):
        from stats import StatSheet

        sheet = StatSheet()
        sheet.set_cell("a", 6)
        sheet.set_cell("b", 3)
        sheet.set_formula("ratio", "a / b")
        self.assertEqual(sheet.value_of("ratio"), 2.0)

    def test_formula_unary_minus(self):
        from stats import StatSheet

        sheet = StatSheet()
        sheet.set_cell("a", 6)
        sheet.set_cell("b", 3)
        sheet.set_formula("neg", "-a + b")
        self.assertEqual(sheet.value_of("neg"), -3)

    def test_formula_unknown_cell_name_raises(self):
        from stats import StatSheet

        sheet = StatSheet()
        sheet.set_cell("a", 1)
        with self.assertRaises(Exception):
            # Rejecting the formula when it is stored, or when it is evaluated, are both fine.
            sheet.set_formula("typo", "a + nope")
            sheet.value_of("typo")

    def test_two_independent_formula_cells_do_not_interfere(self):
        # regression guard: computing one formula cell must not require
        # (or blow up on) an unrelated sibling formula cell.
        from stats import StatSheet

        sheet = StatSheet()
        sheet.set_cell("points", 10)
        sheet.set_cell("rebounds", 4)
        sheet.set_formula("fp", "points + rebounds * 2")
        sheet.set_formula("fp2", "(points + rebounds) * 2")
        self.assertEqual(sheet.value_of("fp"), 18)
        self.assertEqual(sheet.value_of("fp2"), 28)


if __name__ == "__main__":
    unittest.main()
