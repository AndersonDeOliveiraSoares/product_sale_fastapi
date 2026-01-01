from pydantic import BaseModel, EmailStr,Field,ConfigDict
from typing import Optional
from typing import List
from datetime import datetime

class CustomerBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100, example="João Silva")
    email: EmailStr = Field(..., example="joao@email.com")
    document: Optional[str] = Field(None, min_length=11, max_length=14)

class CustomerCreate(CustomerBase):
    pass

class CustomerResponse(BaseModel):
    id: int
    name: str
    email: str
    document: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)
    created_at: datetime
    updated_at: Optional[datetime] = None

class CustomerPaginationResponse(BaseModel):
    total: int
    items: List[CustomerResponse]