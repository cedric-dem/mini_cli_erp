import sqlite3


class StockService:
    def __init__(self, database):
        self.database = database

    def list_stock(self):
        return self.database.list_products()

    def create_product(self, name, quantity=0):
        try:
            cleaned_name = name.strip()

            if not cleaned_name:
                return {"success": False, "error": "Product name is required."}

            if quantity < 0:
                return {
                    "success": False,
                    "error": "Initial quantity cannot be negative.",
                }

            product = self.database.create_product(cleaned_name, quantity)

            return {"success": True, "product": product}

        except sqlite3.IntegrityError:
            return {
                "success": False,
                "error": "A product with this name already exists.",
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    def add_to_stock(self, product_id, quantity):
        try:
            if quantity <= 0:
                return {
                    "success": False,
                    "error": "The quantity to add must be positive.",
                }

            product = self._require_product(product_id)
            updated_product = self.database.update_quantity(
                product.id, product.quantity + quantity
            )

            return {"success": True, "product": updated_product}

        except Exception as e:
            return {"success": False, "error": str(e)}

    def remove_from_stock(self, product_id, quantity):
        try:
            if quantity <= 0:
                return {
                    "success": False,
                    "error": "The quantity to remove must be positive.",
                }

            product = self._require_product(product_id)
            if quantity > product.quantity:
                return {
                    "success": False,
                    "error": "Insufficient stock for this operation.",
                }

            updated_product = self.database.update_quantity(
                product.id, product.quantity - quantity
            )

            return {"success": True, "product": updated_product}

        except Exception as e:
            return {"success": False, "error": str(e)}

    def _require_product(self, product_id):
        product = self.database.get_product(product_id)
        if product is None:
            raise ValueError("Product not found.")
        return product
