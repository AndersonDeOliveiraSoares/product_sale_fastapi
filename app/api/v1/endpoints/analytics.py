from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.repositories.customer_repository import CustomerRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.manufacturer_repository import ManufacturerRepository
from app.repositories.sale_repository import SaleRepository
from app.schemas.analytics import (
    TopCustomerResponse,
    ProductSalesResponse,
    ManufacturerRankingResponse,
    GlobalKPIsResponse,
    SalesByCategoryResponse
)
from app.schemas.product import ProductResponse
router = APIRouter()

@router.get("/top-customers", response_model=List[TopCustomerResponse])
def read_top_customers(db: Session = Depends(get_db)):
    repo = CustomerRepository(db)
    return repo.get_top_customers(limit=5)


@router.get("/most-sold-products", response_model=List[ProductSalesResponse])
def read_most_sold_products(db: Session = Depends(get_db), limit: int = 1000):
    repo = ProductRepository(db)
    return repo.get_most_sold_products(limit=limit)


@router.get("/manufacturer-ranking", response_model=List[ManufacturerRankingResponse])
def read_manufacturer_ranking(db: Session = Depends(get_db)):
    repo = ManufacturerRepository(db)
    return repo.get_manufacturer_ranking()


@router.get("/kpis", response_model=GlobalKPIsResponse)
def read_kpis(db: Session = Depends(get_db)):
    return SaleRepository(db).get_global_kpis()

@router.get("/sales-by-category", response_model=List[SalesByCategoryResponse])
def read_sales_by_category(db: Session = Depends(get_db)):
    return SaleRepository(db).get_sales_by_category()

@router.get("/low-stock-report", response_model=List[ProductResponse])
def read_low_stock(db: Session = Depends(get_db), threshold: int = 25):
    return ProductRepository(db).get_low_stock_alerts(threshold)