from fastapi import APIRouter, Depends, HTTPException,Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.customer import CustomerCreate, CustomerResponse
from app.repositories.customer_repository import CustomerRepository
from app.schemas.customer import CustomerPaginationResponse

router = APIRouter()

@router.post("/", response_model=CustomerResponse)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    repo = CustomerRepository(db)
    return repo.create(customer)

@router.get("/", response_model=CustomerPaginationResponse)
def list_customers(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100)
):
    repository = CustomerRepository(db)
    return repository.get_all_paginated(skip=skip, limit=limit)