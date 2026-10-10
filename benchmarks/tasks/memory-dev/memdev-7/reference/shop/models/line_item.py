class LineItem:
    def __init__(self, sku, qty, unit_cents):
        self.sku = sku
        self.qty = qty
        self.unit_cents = unit_cents

    def total_cents(self):
        return self.qty * self.unit_cents
