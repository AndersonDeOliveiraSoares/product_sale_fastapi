import pytest
from unittest.mock import MagicMock
from app.controller.sale_controller import SaleController
from app.models.product import Product
from app.models.customer import Customer
from app.exceptions import InsufficientStockException


def test_process_sale_insufficient_stock(db_session):
    controller = SaleController(db_session)

    # Mock do Cliente
    mock_customer = MagicMock(spec=Customer)
    mock_customer.id = 1

    # Mock do Produto com estoque baixo (5 unidades)
    mock_product = MagicMock(spec=Product)
    mock_product.id = 1
    mock_product.name = "Mesa"
    mock_product.stock_quantity = 5
    mock_product.price = 200.0

    # Configura o mock do DB para retornar cliente e depois produto
    # Note o uso de .with_for_update() conforme o seu controller
    db_session.query().filter().first.return_value = mock_customer
    db_session.query().filter().with_for_update().first.return_value = mock_product

    # Simulação de item de venda pedindo 10 unidades
    item_simulado = MagicMock(product_id=1, quantity=10)

    with pytest.raises(InsufficientStockException):
        controller.process_new_sale(customer_id=1, items=[item_simulado])

    # Garante que houve rollback se falhou
    assert db_session.rollback.called


def test_process_sale_success_stock_deduction(db_session):
    controller = SaleController(db_session)

    mock_customer = MagicMock(spec=Customer)
    mock_product = MagicMock(spec=Product)
    mock_product.stock_quantity = 20
    mock_product.price = 50.0

    db_session.query().filter().first.return_value = mock_customer
    db_session.query().filter().with_for_update().first.return_value = mock_product

    item_simulado = MagicMock(product_id=1, quantity=5)

    controller.process_new_sale(customer_id=1, items=[item_simulado])

    # Verifica se o estoque foi subtraído corretamente (20 - 5 = 15)
    assert mock_product.stock_quantity == 15
    # Verifica se houve commit
    assert db_session.commit.called