from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.product import ProductCreate, ProductResponse
from app.controller.product_controller import ProductController
from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductPaginationResponse

router = APIRouter()

@router.post("/", response_model=ProductResponse, status_code=201)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    controller = ProductController(db)
    return controller.create_product(product)

@router.get("/", response_model=ProductPaginationResponse)
def list_products(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100) # Definimos um padrão de 20 itens por página
):
    repository = ProductRepository(db)
    return repository.get_all_paginated(skip=skip, limit=limit)