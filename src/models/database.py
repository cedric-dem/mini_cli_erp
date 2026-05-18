import sqlite3
from typing import Iterable

from models.product import Product


class Database:
    def __init__(self, database_path):
        self.database_path = database_path
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize_schema()

    def _connect(self):
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize_schema(self):
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF
                    NOT EXISTS products
                (
                    id
                    INTEGER
                    PRIMARY
                    KEY
                    AUTOINCREMENT,
                    name
                    TEXT
                    NOT
                    NULL
                    UNIQUE,
                    quantity
                    INTEGER
                    NOT
                    NULL
                    DEFAULT
                    0
                    CHECK
                (
                    quantity
                    >=
                    0
                )
                    )
                """
            )

    def list_products(self):

        with self._connect() as connection:
            rows: Iterable[sqlite3.Row] = connection.execute(
                "SELECT id, name, quantity FROM products ORDER BY name"
            )
            return [self._row_to_product(row) for row in rows]

    def create_product(self, name, quantity=0):
        with self._connect() as connection:
            cursor = connection.execute(
                "INSERT INTO products (name, quantity) VALUES (?, ?)",
                (name, quantity),
            )
            product_id = cursor.lastrowid
        return Product(id=product_id, name=name, quantity=quantity)

    def get_product(self, product_id):
        with self._connect() as connection:
            row = connection.execute(
                "SELECT id, name, quantity FROM products WHERE id = ?",
                (product_id,),
            ).fetchone()
        if row is None:
            return None
        return self._row_to_product(row)

    def update_quantity(self, product_id, quantity):
        with self._connect() as connection:
            connection.execute(
                "UPDATE products SET quantity = ? WHERE id = ?",
                (quantity, product_id),
            )
            row = connection.execute(
                "SELECT id, name, quantity FROM products WHERE id = ?",
                (product_id,),
            ).fetchone()
        if row is None:
            raise ValueError("cant find product")
        return self._row_to_product(row)

    @staticmethod
    def _row_to_product(row):
        return Product(id=row["id"], name=row["name"], quantity=row["quantity"])
