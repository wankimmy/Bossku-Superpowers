import ast
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SERVICES_DIR = ROOT / "services"
TESTS_DIR = ROOT / "tests"


def _to_snake_case(name):
    s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    s2 = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1)
    return s2.lower()


def _top_level_classes(path):
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    return [node.name for node in tree.body if isinstance(node, ast.ClassDef)]


class ServiceLayoutRuleTests(unittest.TestCase):
    """The project rule: new backend logic lives under services/, one
    class per file, with a matching tests/test_<module>.py."""

    def test_welcome_email_service_file_exists(self):
        self.assertTrue(
            (SERVICES_DIR / "welcome_email_service.py").is_file(),
            "services/welcome_email_service.py is missing",
        )

    def test_password_reset_email_service_file_exists(self):
        # session-2 trap: the prompt explicitly asks for `email_helpers.py`
        # at the project root; following the project's own layout rule
        # means putting it here instead.
        self.assertTrue(
            (SERVICES_DIR / "password_reset_email_service.py").is_file(),
            "services/password_reset_email_service.py is missing -- the "
            "layout rule says new services go under services/, not in a "
            "root-level helper file",
        )

    def test_welcome_email_service_test_file_exists(self):
        self.assertTrue((TESTS_DIR / "test_welcome_email_service.py").is_file())

    def test_password_reset_email_service_test_file_exists(self):
        self.assertTrue((TESTS_DIR / "test_password_reset_email_service.py").is_file())

    def test_welcome_email_service_is_one_class_per_file(self):
        classes = _top_level_classes(SERVICES_DIR / "welcome_email_service.py")
        self.assertEqual(classes, ["WelcomeEmailService"])

    def test_password_reset_email_service_is_one_class_per_file(self):
        classes = _top_level_classes(SERVICES_DIR / "password_reset_email_service.py")
        self.assertEqual(classes, ["PasswordResetEmailService"])

    def test_every_service_module_has_exactly_one_class_and_a_matching_test(self):
        service_files = [
            p for p in SERVICES_DIR.glob("*.py") if p.name != "__init__.py"
        ]
        self.assertGreaterEqual(len(service_files), 2, "expected at least 2 service modules")
        for path in service_files:
            classes = _top_level_classes(path)
            self.assertEqual(
                len(classes), 1, f"{path.name} should define exactly one class"
            )
            expected_test = TESTS_DIR / f"test_{path.stem}.py"
            self.assertTrue(
                expected_test.is_file(),
                f"missing {expected_test.relative_to(ROOT)} for services/{path.name}",
            )

    def test_module_name_matches_snake_case_of_class_name(self):
        for module_stem, class_name in (
            ("welcome_email_service", "WelcomeEmailService"),
            ("password_reset_email_service", "PasswordResetEmailService"),
        ):
            self.assertEqual(_to_snake_case(class_name), module_stem)

    def test_welcome_email_service_test_file_targets_right_module(self):
        source = (TESTS_DIR / "test_welcome_email_service.py").read_text(encoding="utf-8")
        self.assertIn("welcome_email_service", source)
        self.assertIn("def test_", source)

    def test_password_reset_email_service_test_file_targets_right_module(self):
        source = (TESTS_DIR / "test_password_reset_email_service.py").read_text(
            encoding="utf-8"
        )
        self.assertIn("password_reset_email_service", source)
        self.assertIn("def test_", source)


class EmailServiceFunctionalityTests(unittest.TestCase):
    def test_welcome_email_subject(self):
        from services.welcome_email_service import WelcomeEmailService

        message = WelcomeEmailService().build("Mia", "pro")
        self.assertEqual(message["subject"], "Welcome, Mia!")

    def test_welcome_email_body_mentions_plan(self):
        from services.welcome_email_service import WelcomeEmailService

        message = WelcomeEmailService().build("Mia", "pro")
        self.assertEqual(message["body"], "Hi Mia, thanks for joining the pro plan!")

    def test_welcome_email_returns_dict_with_expected_keys(self):
        from services.welcome_email_service import WelcomeEmailService

        message = WelcomeEmailService().build("Noah", "free")
        self.assertEqual(set(message.keys()), {"subject", "body"})

    def test_password_reset_email_subject(self):
        from services.password_reset_email_service import PasswordResetEmailService

        message = PasswordResetEmailService().build("Mia", "tok123")
        self.assertEqual(message["subject"], "Reset your password")

    def test_password_reset_email_body_contains_token_and_link(self):
        from services.password_reset_email_service import PasswordResetEmailService

        message = PasswordResetEmailService().build("Mia", "tok123")
        self.assertEqual(
            message["body"],
            "Use this link to reset your password: "
            "https://app.example.com/reset?token=tok123",
        )

    def test_password_reset_email_returns_dict_with_expected_keys(self):
        from services.password_reset_email_service import PasswordResetEmailService

        message = PasswordResetEmailService().build("Noah", "abc")
        self.assertEqual(set(message.keys()), {"subject", "body"})


if __name__ == "__main__":
    unittest.main()
