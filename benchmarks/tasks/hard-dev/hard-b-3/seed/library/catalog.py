"""Book catalog: tracks how many copies of each title are available."""


class Catalog:
    def __init__(self):
        self._titles = {}

    def add_title(self, isbn, title, copies):
        if isbn in self._titles:
            raise ValueError(f"{isbn} is already in the catalog")
        self._titles[isbn] = {"title": title, "total": copies, "available": copies}

    def available(self, isbn):
        return self._titles[isbn]["available"]

    def title_of(self, isbn):
        return self._titles[isbn]["title"]

    def checkout_copy(self, isbn):
        record = self._titles[isbn]
        if record["available"] <= 0:
            raise ValueError("no copies available")
        record["available"] -= 1

    def return_copy(self, isbn):
        record = self._titles[isbn]
        if record["available"] < record["total"]:
            record["available"] += 1
