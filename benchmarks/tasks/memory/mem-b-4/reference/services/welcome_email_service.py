"""Builds the welcome email sent to a brand-new signup."""


class WelcomeEmailService:
    def build(self, user_name, plan):
        return {
            "subject": f"Welcome, {user_name}!",
            "body": f"Hi {user_name}, thanks for joining the {plan} plan!",
        }
