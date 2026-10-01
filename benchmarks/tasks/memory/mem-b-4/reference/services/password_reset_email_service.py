"""Builds the password-reset email sent when a user requests one."""


class PasswordResetEmailService:
    def build(self, user_name, reset_token):
        return {
            "subject": "Reset your password",
            "body": (
                "Use this link to reset your password: "
                f"https://app.example.com/reset?token={reset_token}"
            ),
        }
