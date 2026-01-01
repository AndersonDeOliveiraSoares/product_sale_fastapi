from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.sale import SaleCreate, SaleResponse
from app.controller.sale_controller import SaleController
from datetime import datetime
from typing import Optional, List, Dict, Any
from app.schemas.sale import SaleCreate, SaleResponse, SalePaginationResponse
router = APIRouter()


@router.get("/", response_model=SalePaginationResponse) # <--- Mude de dict para SalePaginationResponse
def list_sales(
    db: Session = Depends(get_db),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    skip: int = 0,
    limit: int = 10
):
    controller = SaleController(db)
    return controller.list_sales_filtered(
        start_date=start_date,
        end_date=end_date,
        skip=skip,
        limit=limit
    )

@router.post("/", response_model=SaleResponse, status_code=201)
def create_sale(sale_data: SaleCreate, db: Session = Depends(get_db)):
    controller = SaleController(db)
    return controller.process_new_sale(
        customer_id=sale_data.customer_id,
        items=sale_data.items
    )

@router.get("/list_sales_all/", response_model=List[SaleResponse])
def list_sales_all(db: Session = Depends(get_db)):
    from app.repositories.sale_repository import SaleRepository
    repo = SaleRepository(db)
    return repo.get_all()