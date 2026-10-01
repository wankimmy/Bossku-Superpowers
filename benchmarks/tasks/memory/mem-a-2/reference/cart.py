"""Helpers for pricing a shopping cart. All money is an integer number of cents."""


class Item:
    def __init__(self, name, unit_price_cents, quantity):
        self.name = name
        self.unit_price_cents = unit_price_cents
        self.quantity = quantity


def compute_subtotal_cents(items):
    total = 0
    for item in items:
        total += item.unit_price_cents * item.quantity
    return total


def apply_discount_cents(subtotal_cents, percent_off):
    discount = (subtotal_cents * percent_off + 50) // 100
    return subtotal_cents - discount


def split_evenly_cents(total_cents, num_people):
    base = total_cents // num_people
    remainder = total_cents % num_people
    shares = []
    for i in range(num_people):
        shares.append(base + 1 if i < remainder else base)
    return shares
