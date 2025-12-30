from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, default=0)
    category = Column(String, nullable=False, default="Geral")

    # Chave Estrangeira: Aponta para o ID do fabricante
    manufacturer_id = Column(Integer, ForeignKey("manufacturers.id"), nullable=False)

    # Relação: Permite acessar o objeto fabricante direto do produto
    manufacturer = relationship("Manufacturer", back_populates="products")