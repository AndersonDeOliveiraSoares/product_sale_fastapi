from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.sale import Sale, SaleItem
from app.models.product import Product


class SaleRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_global_kpis(self):
        # Busca os totais reais do banco
        stats = self.db.query(
            func.sum(Sale.total_price).label("rev"),
            func.count(Sale.id).label("count")
        ).first()

        rev = float(stats.rev) if stats.rev else 0.0
        orders = int(stats.count) if stats.count else 0
        ticket = rev / orders if orders > 0 else 0.0

        # O RETORNO PRECISA TER ESTES 6 CAMPOS EXATOS
        return {
            "total_revenue": rev,
            "revenue_delta": 0.0,
            "total_orders": orders,
            "orders_delta": 0,
            "average_ticket": ticket,
            "ticket_delta": 0.0
        }

    def get_sales_by_category(self):
        results = self.db.query(Product.category, func.sum(SaleItem.quantity)) \
            .join(SaleItem, SaleItem.product_id == Product.id) \
            .group_by(Product.category).all()

        return [{"category": str(r[0]), "total_sold": int(r[1])} for r in results]