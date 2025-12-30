from sqlalchemy.orm import Session
from app.models.manufacturer import Manufacturer
from sqlalchemy import func
from app.models.manufacturer import Manufacturer
from app.models.product import Product
from app.models.sale import SaleItem


class ManufacturerRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, name: str, contact_email: str):
        db_manufacturer = Manufacturer(name=name, contact_email=contact_email)
        self.db.add(db_manufacturer)
        self.db.commit()
        self.db.refresh(db_manufacturer)
        return db_manufacturer

    def get_all(self):
        return self.db.query(Manufacturer).all()


    def get_manufacturer_ranking(self):
        return (
            self.db.query(
                Manufacturer.id.label("manufacturer_id"),
                Manufacturer.name.label("manufacturer_name"),
                func.sum(SaleItem.quantity * SaleItem.unit_price).label("total_sales_value"),
                func.sum(SaleItem.quantity).label("products_sold_count")
            )
            .join(Product, Manufacturer.id == Product.manufacturer_id)
            .join(SaleItem, Product.id == SaleItem.product_id)
            .group_by(Manufacturer.id, Manufacturer.name)
            .order_by(func.sum(SaleItem.quantity * SaleItem.unit_price).desc())
            .all()
        )


    def get_all_paginated(self, skip: int = 0, limit: int = 10):
        total = self.db.query(Manufacturer).count()

        items = self.db.query(Manufacturer) \
            .offset(skip) \
            .limit(limit) \
            .all()

        return {"total": total, "items": items}