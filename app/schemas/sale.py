from pydantic import BaseModel, ConfigDict
from typing import List,Optional
from datetime import datetime

class SaleItemResponse(BaseModel):
    product_id: int
    quantity: int
    unit_price: float
    created_at: datetime
    updated_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)

class SaleResponse(BaseModel):
    id: int
    total_price: float
    sale_date: datetime
    updated_at: Optional[datetime] = None
    items: List[SaleItemResponse]
    model_config = ConfigDict(from_attributes=True)

# ADICIONE ESTE SCHEMA PARA A LISTAGEM PAGINADA
class SalePaginationResponse(BaseModel):
    total: int
    items: List[SaleResponse]

class SaleCreate(BaseModel):
    customer_id: int
    items: List[dict]