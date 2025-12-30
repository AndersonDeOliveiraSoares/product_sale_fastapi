from fastapi import APIRouter, Depends,Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.manufacturer import ManufacturerCreate, ManufacturerResponse
from app.controller.manufacturer_controller import ManufacturerController
from app.schemas.manufacturer import ManufacturerPaginationResponse
from app.repositories.manufacturer_repository import ManufacturerRepository

router = APIRouter()

@router.post("/", response_model=ManufacturerResponse)
def create(manufacturer: ManufacturerCreate, db: Session = Depends(get_db)):
    controller = ManufacturerController(db)
    return controller.create_manufacturer(manufacturer)

@router.get("/", response_model=ManufacturerPaginationResponse)
def list_factories(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0), # Não permite números negativos
    limit: int = Query(10, ge=1, le=100) # Limite padrão 10, máximo 100
):
    repository = ManufacturerRepository(db)
    return repository.get_all_paginated(skip=skip, limit=limit)