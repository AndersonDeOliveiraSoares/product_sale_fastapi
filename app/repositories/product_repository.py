from sqlalchemy.orm import Session

from sqlalchemy import func
from app.models.product import Product
from app.models.sale import SaleItem
from app.exceptions import ProductNotFoundException


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id_or_404(self, product_id: int):
        """Busca um produto ou lança 404 estruturado."""
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise ProductNotFoundException(product_id)
        return product

    def create(self, product_data: Product):
        try:
            self.db.add(product_data)
            self.db.commit()
            self.db.refresh(product_data)
            return product_data
        except Exception:
            self.db.rollback()
            raise

    def get_all(self):
        return self.db.query(Product).all()

    def get_most_sold_products(self, limit: int = 10):
        return (
            self.db.query(
                Product.id.label("product_id"),
                Product.name.label("product_name"),
                func.sum(SaleItem.quantity).label("total_quantity_sold"),
                func.sum(SaleItem.quantity * SaleItem.unit_price).label("total_revenue")
            )
            .join(SaleItem, Product.id == SaleItem.product_id)
            .group_by(Product.id, Product.name)
            .order_by(func.sum(SaleItem.quantity).desc())
            .limit(limit)
            .all()
        )

    def get_low_stock_alerts(self, threshold: int = 25):
        return (
            self.db.query(Product)
            .filter(Product.stock_quantity <= threshold)
            .order_by(Product.stock_quantity.asc())
            .all()
        )

    def get_sales_by_category(self):
        category_func = func.split_part(Product.name, ' ', 1)

        return (
            self.db.query(
                category_func.label("category"),
                func.sum(SaleItem.quantity).label("total_sold")
            )
            .join(SaleItem, Product.id == SaleItem.product_id)  # Corrigido para ==
            .group_by(category_func)
            .all()
        )


    def get_all_paginated(self, skip: int = 0, limit: int = 20):
        # Conta quantos produtos existem no total para a lógica de páginas do Dashboard
        total = self.db.query(Product).count()

        # Busca os produtos com deslocamento e limite
        items = self.db.query(Product) \
            .offset(skip) \
            .limit(limit) \
            .all()

        return {"total": total, "items": items}