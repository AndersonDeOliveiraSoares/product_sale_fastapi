import pytest
from unittest.mock import MagicMock
from app.controller.product_controller import ProductController
from app.schemas.product import ProductCreate
from app.exceptions import  ManufacturerNotFoundException
from app.models.manufacturer import Manufacturer
from pydantic import ValidationError


def test_create_product_invalid_price(db_session):
    controller = ProductController(db_session)

    # O Pydantic lança ValidationError ao tentar criar o objeto com preço 0
    with pytest.raises(ValidationError):
        ProductCreate(name="Teste", price=0, stock_quantity=10, manufacturer_id=1)


def test_create_product_manufacturer_not_found(db_session):
    controller = ProductController(db_session)
    # Simula que o fabricante não existe no banco
    db_session.query().filter().first.return_value = None

    data = ProductCreate(name="Teste", price=10.0, stock_quantity=10, manufacturer_id=99)

    with pytest.raises(ManufacturerNotFoundException):
        controller.create_product(data)


def test_create_product_success(db_session):
    controller = ProductController(db_session)

    # Simula fabricante encontrado
    mock_manufacturer = MagicMock(spec=Manufacturer)
    mock_manufacturer.id = 1
    db_session.query().filter().first.return_value = mock_manufacturer

    data = ProductCreate(name="Cadeira", price=150.0, stock_quantity=20, manufacturer_id=1)

    # Chamada do método
    result = controller.create_product(data)

    # Verifica se o repositório foi chamado (o controller inicializa o repositório com o db)
    assert db_session.add.called