from sqlalchemy.orm import Session
from app.schemas.customer import CustomerCreate
from sqlalchemy import func
from app.models.customer import Customer
from app.models.sale import Sale

class CustomerRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, customer_data: CustomerCreate):
        db_customer = Customer(**customer_data.model_dump())
        self.db.add(db_customer)
        self.db.commit()
        self.db.refresh(db_customer)
        return db_customer

    def get_all(self):
        return self.db.query(Customer).all()

    def get_top_customers(self, limit: int = 5):
        return (
            self.db.query(
                Customer.id.label("customer_id"),
                Customer.name.label("customer_name"),
                func.sum(Sale.total_price).label("total_spent"),
                func.count(Sale.id).label("order_count")
            )
            .join(Sale, Customer.id == Sale.customer_id)
            .group_by(Customer.id, Customer.name)
            .order_by(func.sum(Sale.total_price).desc())
            .limit(limit)
            .all()
        )

    # app/repositories/customer_repository.py

    def get_all_paginated(self, skip: int = 0, limit: int = 20):
        total = self.db.query(Customer).count()

        items = self.db.query(Customer) \
            .offset(skip) \
            .limit(limit) \
            .all()

        return {"total": total, "items": items}