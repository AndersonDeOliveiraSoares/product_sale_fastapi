from typing import Optional
from typing import List
from pydantic import BaseModel, EmailStr

class ManufacturerBase(BaseModel):
    name: str
    contact_email: Optional[str]

class ManufacturerCreate(ManufacturerBase):
    pass  # O que é necessário para criar

class ManufacturerResponse(ManufacturerBase):
    id: int

    class Config:
        from_attributes = True

class ManufacturerPaginationResponse(BaseModel):
    total: int
    items: List[ManufacturerBase]