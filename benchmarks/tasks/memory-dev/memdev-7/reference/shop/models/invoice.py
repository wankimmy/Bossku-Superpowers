class Invoice:
    def __init__(self, number, customer, total_cents, paid=False):
        self.number = number
        self.customer = customer
        self.total_cents = total_cents
        self.paid = paid

    def is_paid(self):
        return self.paid
