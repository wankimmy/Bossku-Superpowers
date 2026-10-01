"""Shopping cart with line items."""

from decimal import Decimal

from .money import round_half_up


class Line:
    __slots__ = ("sku", "unit_price", "quantity")

    def __init__(self, sku, unit_price, quantity):
        self.sku = sku
        self.unit_price = unit_price
        self.quantity = quantity


class Cart:
    def __init__(self, lines=None, applied_codes=None):
        self.lines = lines if lines is not None else []
        self.applied_codes = applied_codes if applied_codes is not None else []

    def add_item(self, sku, unit_price, quantity=1):
        unit_price = Decimal(str(unit_price))
        for line in self.lines:
            if line.sku == sku:
                if line.unit_price != unit_price:
                    raise ValueError(
                        f"{sku} is already in the cart at a different price"
                    )
                line.quantity += quantity
                return
        self.lines.append(Line(sku, unit_price, quantity))

    def subtotal(self):
        total = Decimal("0")
        for line in self.lines:
            total += line.unit_price * line.quantity
        return round_half_up(total)
