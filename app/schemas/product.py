from pydantic import BaseModel, Field, ConfigDict
from typing import List,Optional
from datetime import datetime

class ProductBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    price: float = Field(..., gt=0)
    stock_quantity: int = Field(..., ge=0)
    manufacturer_id: int # ID do fabricante que você já criou

class ProductCreate(ProductBase):
    pass

class ProductResponse(BaseModel):
    id: int
    name: str
    category: str
    price: float
    stock_quantity: int
    manufacturer_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


class ProductPaginationResponse(BaseModel):
    total: int
    items: List[ProductResponse]