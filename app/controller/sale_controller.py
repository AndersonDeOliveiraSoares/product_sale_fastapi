from sqlalchemy.orm import Session
from app.models.sale import Sale, SaleItem
from app.models.product import Product
from app.models.customer import Customer
from app.exceptions import (
    CustomerNotFoundException, ProductNotFoundException,
    InsufficientStockException, EmptySaleException, DatabaseException
)
from datetime import datetime, time
from app.repositories.sale_repository import SaleRepository

class SaleController:
    def __init__(self, db: Session):
        self.db = db
        self.repository = SaleRepository(db)


    def process_new_sale(self, customer_id: int, items: list):
        if not items:
            raise EmptySaleException()

        # Início da transação explícita para segurança de stock
        try:
            customer = self.db.query(Customer).filter(Customer.id == customer_id).first()
            if not customer:
                raise CustomerNotFoundException(customer_id)

            total_price = 0
            new_sale_items = []

            for item_data in items:
                product = self.db.query(Product).filter(Product.id == item_data.product_id).with_for_update().first()

                if not product:
                    raise ProductNotFoundException(item_data.product_id)

                if product.stock_quantity < item_data.quantity:
                    raise InsufficientStockException(
                        product_name=product.name,
                        requested=item_data.quantity,
                        available=product.stock_quantity
                    )

                # Baixa de stock e cálculo
                product.stock_quantity -= item_data.quantity
                subtotal = product.price * item_data.quantity
                total_price += subtotal

                new_sale_items.append(SaleItem(
                    product_id=product.id,
                    quantity=item_data.quantity,
                    unit_price=product.price
                ))

            new_sale = Sale(
                customer_id=customer_id,
                total_price=total_price,
                items=new_sale_items
            )

            self.db.add(new_sale)
            self.db.commit()  # Grava venda, itens e stock de uma vez
            self.db.refresh(new_sale)
            return new_sale


        except Exception as e:

            self.db.rollback()

            # Adicione o TypeError aqui para ele não "esconder" erros de Mock

            if isinstance(e, (CustomerNotFoundException, ProductNotFoundException,

                              InsufficientStockException, EmptySaleException, TypeError)):
                raise e

            raise DatabaseException(detail=str(e))

    def list_sales_paginated(self, skip: int = 0, limit: int = 10):
        """Retorna as vendas paginadas usando o repositório."""
        return self.repository.get_all_paginated(skip=skip, limit=limit)

    def list_sales_filtered(self, start_date=None, end_date=None, skip: int = 0, limit: int = 10):
        return self.repository.get_sales_filtered(
            start_date=start_date,
            end_date=end_date,
            skip=skip,
            limit=limit
        )