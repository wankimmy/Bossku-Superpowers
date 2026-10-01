import ast
import inspect
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HIDDEN_FILENAME = Path(__file__).name

BUILTIN_EXCEPTION_NAMES = {
    "ValueError",
    "KeyError",
    "TypeError",
    "IndexError",
    "AttributeError",
    "RuntimeError",
    "Exception",
    "StopIteration",
    "LookupError",
    "NotImplementedError",
    "ArithmeticError",
    "OSError",
    "AssertionError",
    "NameError",
}


def _project_py_files():
    files = []
    for path in sorted(ROOT.rglob("*.py")):
        if path.name == HIDDEN_FILENAME:
            continue
        if "tests" in path.relative_to(ROOT).parts[:-1]:
            continue
        files.append(path)
    return files


def _bare_builtin_raises(tree):
    for node in ast.walk(tree):
        if isinstance(node, ast.Raise) and node.exc is not None:
            target = node.exc
            if isinstance(target, ast.Call):
                target = target.func
            if isinstance(target, ast.Name) and target.id in BUILTIN_EXCEPTION_NAMES:
                yield target.id


class AppErrorRuleTests(unittest.TestCase):
    """The project rule: every failure raises an AppError subclass."""

    def test_no_bare_builtin_exceptions_raised_anywhere(self):
        for path in _project_py_files():
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            offenders = list(_bare_builtin_raises(tree))
            self.assertEqual(
                offenders,
                [],
                f"{path.name} raises a bare builtin exception {offenders}; "
                "use an AppError subclass instead",
            )

    def test_errors_module_defines_apperror(self):
        import errors

        self.assertTrue(issubclass(errors.AppError, Exception))
        self.assertIsNot(errors.AppError, Exception)

    def test_all_exception_classes_in_errors_module_subclass_apperror(self):
        import errors

        for name, obj in vars(errors).items():
            if inspect.isclass(obj) and issubclass(obj, BaseException) and obj is not BaseException:
                if obj is Exception:
                    continue
                self.assertTrue(
                    issubclass(obj, errors.AppError),
                    f"errors.{name} does not subclass AppError",
                )

    def test_book_conflict_raises_apperror(self):
        import errors
        from desks import DeskBooking

        board = DeskBooking()
        board.book("A1", "mia", "2026-10-01")
        with self.assertRaises(errors.AppError):
            board.book("A1", "noah", "2026-10-01")

    def test_cancel_missing_booking_raises_apperror(self):
        import errors
        from desks import DeskBooking

        board = DeskBooking()
        with self.assertRaises(errors.AppError):
            board.cancel("A1", "mia", "2026-10-01")

    def test_move_booking_conflict_raises_apperror(self):
        # session-2 trap: a forgetful solution tends to raise a bare
        # ValueError/KeyError here since the prompt never mentions errors.
        import errors
        from desks import DeskBooking

        board = DeskBooking()
        board.book("A1", "mia", "2026-10-01")
        board.book("A1", "noah", "2026-10-02")
        with self.assertRaises(errors.AppError):
            board.move_booking("A1", "mia", "2026-10-01", "2026-10-02")

    def test_move_booking_not_found_raises_apperror(self):
        import errors
        from desks import DeskBooking

        board = DeskBooking()
        with self.assertRaises(errors.AppError):
            board.move_booking("A1", "mia", "2026-10-01", "2026-10-02")


class DeskBookingFunctionalityTests(unittest.TestCase):
    def test_book_then_list_bookings_for_user(self):
        from desks import DeskBooking

        board = DeskBooking()
        board.book("A1", "mia", "2026-10-01")
        self.assertEqual(board.list_bookings_for_user("mia"), [("A1", "2026-10-01")])

    def test_list_bookings_for_user_empty(self):
        from desks import DeskBooking

        board = DeskBooking()
        self.assertEqual(board.list_bookings_for_user("nobody"), [])

    def test_list_bookings_for_user_sorted_multiple(self):
        from desks import DeskBooking

        board = DeskBooking()
        board.book("B1", "mia", "2026-10-03")
        board.book("A1", "mia", "2026-10-01")
        board.book("A2", "noah", "2026-10-01")
        self.assertEqual(
            board.list_bookings_for_user("mia"),
            [("A1", "2026-10-01"), ("B1", "2026-10-03")],
        )

    def test_cancel_frees_the_desk_for_rebooking(self):
        from desks import DeskBooking

        board = DeskBooking()
        board.book("A1", "mia", "2026-10-01")
        board.cancel("A1", "mia", "2026-10-01")
        board.book("A1", "noah", "2026-10-01")  # should not raise
        self.assertEqual(board.list_bookings_for_user("noah"), [("A1", "2026-10-01")])

    def test_move_booking_happy_path(self):
        from desks import DeskBooking

        board = DeskBooking()
        board.book("A1", "mia", "2026-10-01")
        board.move_booking("A1", "mia", "2026-10-01", "2026-10-05")
        self.assertEqual(board.list_bookings_for_user("mia"), [("A1", "2026-10-05")])

    def test_move_booking_frees_up_the_old_day(self):
        from desks import DeskBooking

        board = DeskBooking()
        board.book("A1", "mia", "2026-10-01")
        board.move_booking("A1", "mia", "2026-10-01", "2026-10-05")
        board.book("A1", "noah", "2026-10-01")  # old day should be free now
        self.assertEqual(board.list_bookings_for_user("noah"), [("A1", "2026-10-01")])

    def test_failed_move_leaves_original_booking_intact(self):
        import errors
        from desks import DeskBooking

        board = DeskBooking()
        board.book("A1", "mia", "2026-10-01")
        board.book("A1", "noah", "2026-10-02")
        with self.assertRaises(errors.AppError):
            board.move_booking("A1", "mia", "2026-10-01", "2026-10-02")
        # the original booking must still be there, untouched
        self.assertEqual(board.list_bookings_for_user("mia"), [("A1", "2026-10-01")])


if __name__ == "__main__":
    unittest.main()
