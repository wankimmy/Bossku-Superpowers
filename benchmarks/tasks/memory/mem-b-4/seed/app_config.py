"""Small static configuration values for the notification service."""

APP_NAME = "NotifyPrototype"
SUPPORT_EMAIL = "support@example.com"


def signature_block():
    return f"-- {APP_NAME} ({SUPPORT_EMAIL})"
