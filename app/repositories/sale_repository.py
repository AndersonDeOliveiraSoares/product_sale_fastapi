from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.sale import Sale, SaleItem
from app.models.product import Product
from app.exceptions import DatabaseException
from datetime import datetime

class SaleRepository:
    def __init__(self, db: Session):
        self.db = db


    # Mantenha o create_sale simples para uso genérico se necessário
    def create_sale(self, sale_obj: Sale):
        try:
            self.db.add(sale_obj)
            self.db.commit()
            self.db.refresh(sale_obj)
            return sale_obj
        except Exception as e:
            self.db.rollback()
            raise DatabaseException(detail=f"Erro ao persistir venda: {str(e)}")

    def get_all(self):
        return self.db.query(Sale).all()

    def get_all_paginated(self, skip: int = 0, limit: int = 10):
        total = self.db.query(Sale).count()

        items = self.db.query(Sale) \
            .offset(skip) \
            .limit(limit) \
            .all()

        return {"total": total, "items": items}

    def get_global_kpis(self):
        # 1. Busca os totais agregados diretamente via SQL (mais rápido que trazer todos os objetos)
        stats = self.db.query(
            func.sum(Sale.total_price).label("rev"),
            func.count(Sale.id).label("count")
        ).first()

        # 2. Tratamento de valores nulos (caso o banco esteja vazio)
        total_revenue = float(stats.rev) if stats.rev else 0.0
        total_orders = int(stats.count) if stats.count else 0

        # 3. Cálculo do Ticket Médio (Faturamento / Quantidade de Vendas)
        average_ticket = total_revenue / total_orders if total_orders > 0 else 0.0

        # 4. Retorno com a estrutura exata esperada pelo seu Frontend/Streamlit
        return {
            "total_revenue": total_revenue,
            "revenue_delta": 12.5,  # Valor simulado (depois podemos calcular a variação real vs mês anterior)
            "total_orders": total_orders,
            "orders_delta": 5,  # Valor simulado
            "average_ticket": average_ticket,
            "ticket_delta": -2.3  # Valor simulado
        }

    def get_sales_by_category(self):
        results = self.db.query(Product.category, func.sum(SaleItem.quantity)) \
            .join(SaleItem, SaleItem.product_id == Product.id) \
            .group_by(Product.category).all()

        return [{"category": str(r[0]), "total_sold": int(r[1])} for r in results]

    def get_sales_filtered(self, start_date: datetime = None, end_date: datetime = None, skip: int = 0,
                           limit: int = 10):
        query = self.db.query(Sale)

        if start_date:
            query = query.filter(Sale.sale_date >= start_date)
        if end_date:
            query = query.filter(Sale.sale_date <= end_date)

        total = query.count()
        items = query.order_by(Sale.sale_date.desc()).offset(skip).limit(limit).all()

        return {"total": total, "items": items}