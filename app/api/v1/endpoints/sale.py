from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.sale import SaleCreate, SaleResponse
from app.repositories.sale_repository import SaleRepository

router = APIRouter()


@router.post("/", response_model=SaleResponse)
def create_sale(sale_data: SaleCreate, db: Session = Depends(get_db)):
    repo = SaleRepository(db)
    sale = repo.create(sale_data)

    if not sale:
        # Se o repository retornar None, é porque faltou estoque ou produto
        raise HTTPException(
            status_code=400,
            detail="Erro ao processar venda: estoque insuficiente ou produto inexistente."
        )
    return sale


@router.get("/", response_model=list[SaleResponse])
def list_sales(db: Session = Depends(get_db)):
    repo = SaleRepository(db)
    # Certifique-se de que tem o método get_all no seu repository
    return repo.get_all_sales()