from pydantic import BaseModel
from typing import List


class ProductBase(BaseModel):
    name: str
    price: float
    stock_quantity: int
    manufacturer_id: int # ID do fabricante que você já criou

class ProductCreate(ProductBase):
    pass

# class ProductResponse(ProductBase):
#     id: int
#     manufacturer_name: str | None = None
#     class Config:
#         from_attributes = True
#

class ProductResponse(BaseModel):
    id: int
    name: str
    category: str
    price: float
    stock_quantity: int
    manufacturer_id: int

    class Config:
        from_attributes = True

class ProductPaginationResponse(BaseModel):
    total: int
    items: List[ProductResponse]