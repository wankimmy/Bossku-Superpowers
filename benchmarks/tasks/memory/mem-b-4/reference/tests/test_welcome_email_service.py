import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.welcome_email_service import WelcomeEmailService


class WelcomeEmailServiceTests(unittest.TestCase):
    def test_build_subject_and_body(self):
        message = WelcomeEmailService().build("Mia", "pro")
        self.assertEqual(message["subject"], "Welcome, Mia!")
        self.assertEqual(message["body"], "Hi Mia, thanks for joining the pro plan!")


if __name__ == "__main__":
    unittest.main()
