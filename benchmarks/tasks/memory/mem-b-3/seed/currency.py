"""Supported currency codes for invoices."""

SUPPORTED_CURRENCIES = {"USD", "EUR", "MYR"}


def is_supported_currency(code):
    return code in SUPPORTED_CURRENCIES
