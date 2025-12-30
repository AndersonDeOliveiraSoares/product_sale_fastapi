from pydantic import BaseModel, EmailStr
from typing import Optional
from typing import List

class CustomerBase(BaseModel):
    name: str
    email: EmailStr
    document: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerResponse(BaseModel):
    id: int
    name: str
    email: str
    document: Optional[str] = None

    class Config:
        from_attributes = True

class CustomerPaginationResponse(BaseModel):
    total: int
    items: List[CustomerResponse]