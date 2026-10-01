"""A small product catalog, backed by SQLite, that shoppers can search."""
import sqlite3


class ProductCatalog:
    def __init__(self):
        self._conn = sqlite3.connect(":memory:")
        self._conn.execute(
            "CREATE TABLE products ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "name TEXT NOT NULL, "
            "category TEXT NOT NULL, "
            "price REAL NOT NULL)"
        )
        self._conn.commit()

    def add_product(self, name, category, price):
        if price < 0:
            raise ValueError("price must not be negative")
        cur = self._conn.execute(
            "INSERT INTO products (name, category, price) VALUES (?, ?, ?)",
            (name, category, price),
        )
        self._conn.commit()
        return cur.lastrowid

    def search(self, name_contains=None, category=None, min_price=None, max_price=None):
        clauses, params = [], []
        if name_contains is not None:
            clauses.append("LOWER(name) LIKE ?")
            params.append(f"%{name_contains.lower()}%")
        if category is not None:
            clauses.append("category = ?")
            params.append(category)
        if min_price is not None:
            clauses.append("price >= ?")
            params.append(min_price)
        if max_price is not None:
            clauses.append("price <= ?")
            params.append(max_price)
        where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        sql = f"SELECT id, name, category, price FROM products {where} ORDER BY name, id"
        rows = self._conn.execute(sql, params).fetchall()
        return [{"id": r[0], "name": r[1], "category": r[2], "price": r[3]} for r in rows]
