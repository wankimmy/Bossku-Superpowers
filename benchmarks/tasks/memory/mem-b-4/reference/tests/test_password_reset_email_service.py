import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.password_reset_email_service import PasswordResetEmailService


class PasswordResetEmailServiceTests(unittest.TestCase):
    def test_build_subject_and_body(self):
        message = PasswordResetEmailService().build("Mia", "tok123")
        self.assertEqual(message["subject"], "Reset your password")
        self.assertIn("tok123", message["body"])


if __name__ == "__main__":
    unittest.main()
