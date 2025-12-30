from pydantic import BaseModel
from typing import List
from datetime import datetime

class SaleItemCreate(BaseModel):
    product_id: int
    quantity: int

class SaleCreate(BaseModel):
    customer_id: int
    items: List[SaleItemCreate]

class SaleItemResponse(BaseModel):
    product_id: int
    quantity: int
    unit_price: float
    class Config:
        from_attributes = True

class SaleResponse(BaseModel):
    id: int
    sale_date: datetime
    total_price: float
    items: List[SaleItemResponse]
    class Config:
        from_attributes = True