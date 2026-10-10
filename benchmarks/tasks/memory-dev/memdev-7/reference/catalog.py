"""Item catalog."""
import uuid


class Catalog:
    def __init__(self):
        self._items = {}

    def get(self, item_id):
        return self._items[item_id]

    def all(self):
        return list(self._items.values())

    def __len__(self):
        return len(self._items)

    def create_item(self, name, price_cents):
        if not isinstance(name, str) or not name or not isinstance(price_cents, int) or price_cents < 0:
            raise ValueError("bad item")
        item = {"id": uuid.uuid4().hex, "name": name, "price_cents": price_cents}
        self._items[item["id"]] = item
        return item
