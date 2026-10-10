from shop.models.currency import Currency


class LineItem:
    def __init__(self, sku, qty, unit_cents, currency=Currency.MYR):
        self.sku = sku
        self.qty = qty
        self.unit_cents = unit_cents
        self.currency = currency

    def total_cents(self):
        return self.qty * self.unit_cents
