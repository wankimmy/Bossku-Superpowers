"""Compute invoice totals with per-line discounts, an invoice discount, and tax."""

from decimal import Decimal, ROUND_HALF_UP, InvalidOperation

_CENT = Decimal("0.01")
_HUNDRED = Decimal(100)


class InvoiceError(ValueError):
    """Raised when invoice input values are the right type but invalid."""


def _round2(value):
    return value.quantize(_CENT, rounding=ROUND_HALF_UP)


def _to_decimal(value, name):
    if isinstance(value, bool) or isinstance(value, float):
        raise TypeError(f"{name} must be a str, int, or Decimal, not {type(value).__name__}")
    if isinstance(value, Decimal):
        return value
    if isinstance(value, int):
        return Decimal(value)
    if isinstance(value, str):
        try:
            return Decimal(value)
        except InvalidOperation:
            raise InvoiceError(f"{name} is not a valid number: {value!r}")
    raise TypeError(f"{name} must be a str, int, or Decimal, not {type(value).__name__}")


def _to_price(value, name):
    d = _to_decimal(value, name)
    if not d.is_finite():
        raise InvoiceError(f"{name} must be finite")
    if d < 0:
        raise InvoiceError(f"{name} must not be negative")
    return d


def _to_percent(value, name):
    d = _to_decimal(value, name)
    if not d.is_finite():
        raise InvoiceError(f"{name} must be finite")
    if d < 0 or d > _HUNDRED:
        raise InvoiceError(f"{name} must be between 0 and 100")
    return d


def _validate_quantity(value):
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"quantity must be an int, not {type(value).__name__}")
    if value < 1:
        raise InvoiceError("quantity must be at least 1")
    return value


def line_item_subtotal(quantity, unit_price, discount_percent="0"):
    qty = _validate_quantity(quantity)
    price = _to_price(unit_price, "unit_price")
    discount = _to_percent(discount_percent, "discount_percent")

    raw = Decimal(qty) * price
    line_total = raw * (_HUNDRED - discount) / _HUNDRED
    return str(_round2(line_total))


def compute_invoice_total(line_items, invoice_discount_percent=0, tax_percent=0):
    if isinstance(line_items, bool) or not isinstance(line_items, (list, tuple)):
        raise TypeError(f"line_items must be a list or tuple, not {type(line_items).__name__}")

    invoice_discount = _to_percent(invoice_discount_percent, "invoice_discount_percent")
    tax = _to_percent(tax_percent, "tax_percent")

    subtotal = Decimal("0.00")
    for item in line_items:
        if not isinstance(item, dict):
            raise TypeError(f"each line item must be a dict, not {type(item).__name__}")
        if "quantity" not in item:
            raise InvoiceError("line item missing required key 'quantity'")
        if "unit_price" not in item:
            raise InvoiceError("line item missing required key 'unit_price'")

        line_str = line_item_subtotal(
            item["quantity"],
            item["unit_price"],
            item.get("discount_percent", "0"),
        )
        subtotal += Decimal(line_str)

    discounted_total = _round2(subtotal * (_HUNDRED - invoice_discount) / _HUNDRED)
    final_total = _round2(discounted_total * (_HUNDRED + tax) / _HUNDRED)
    return str(final_total)
