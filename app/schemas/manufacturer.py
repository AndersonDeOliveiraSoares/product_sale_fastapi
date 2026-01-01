from typing import Optional
from typing import List
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class ManufacturerBase(BaseModel):
    name: str
    contact_email: Optional[str]

class ManufacturerCreate(ManufacturerBase):
    pass  # O que é necessário para criar

class ManufacturerResponse(ManufacturerBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
    created_at: datetime
    updated_at: Optional[datetime] = None


class ManufacturerPaginationResponse(BaseModel):
    total: int
    items: List[ManufacturerBase]