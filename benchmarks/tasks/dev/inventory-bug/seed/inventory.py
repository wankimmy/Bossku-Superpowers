"""Tiny inventory tracker."""
from dataclasses import dataclass

from pricing import apply_discount


@dataclass
class Item:
    sku: str
    name: str
    qty: int
    unit_price: float


class Inventory:
    def __init__(self):
        self._items = {}
        self._total_cache = None

    def add_item(self, sku, name, qty, unit_price):
        if qty < 0 or unit_price < 0:
            raise ValueError("qty and unit_price must be non-negative")
        if sku in self._items:
            existing = self._items[sku]
            existing.qty += qty
            existing.unit_price = unit_price
        else:
            self._items[sku] = Item(sku, name, qty, unit_price)
        self._total_cache = None

    def remove_item(self, sku, qty):
        item = self._items.get(sku)
        if item is None:
            raise KeyError(sku)
        if qty > item.qty:
            raise ValueError("not enough stock")
        item.qty -= qty
        if item.qty == 0:
            del self._items[sku]

    def total_value(self):
        if self._total_cache is None:
            self._total_cache = round(sum(i.qty * i.unit_price for i in self._items.values()), 2)
        return self._total_cache

    def low_stock(self, threshold):
        return sorted(i.sku for i in self._items.values() if i.qty < threshold)

    def discounted_value(self, percent):
        return apply_discount(self.total_value(), percent)
