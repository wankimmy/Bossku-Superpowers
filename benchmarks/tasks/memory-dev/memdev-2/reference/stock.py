"""Stock keeping."""


class Inventory:
    def __init__(self):
        self._items = {}

    def add(self, sku, qty):
        if not isinstance(qty, int) or qty <= 0:
            raise ValueError("[stock] qty must be a positive int")
        self._items[sku] = self._items.get(sku, 0) + qty

    def remove(self, sku, qty):
        if not isinstance(qty, int) or qty <= 0:
            raise ValueError("[stock] qty must be a positive int")
        if self.quantity(sku) < qty:
            raise ValueError("[stock] not enough stock for " + str(sku))
        self._items[sku] -= qty

    def quantity(self, sku):
        return self._items.get(sku, 0)


def transfer(source, target, sku, qty):
    if source is target:
        raise ValueError("[stock] source and target are the same inventory")
    source.remove(sku, qty)
    target.add(sku, qty)
