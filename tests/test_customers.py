import pytest
from unittest.mock import MagicMock
from app.repositories.customer_repository import CustomerRepository
from app.schemas.customer import CustomerCreate
from app.models.customer import Customer

# ADICIONE ESTES IMPORTS PARA REGISTRAR OS MODELOS NO SQLALCHEMY
from app.models.product import Product
from app.models.sale import Sale, SaleItem
from app.models.manufacturer import Manufacturer

from pydantic import ValidationError


@pytest.fixture
def db_session():
    """Fixture para criar um mock da sessão do banco de dados."""
    return MagicMock()


# --- Testes de Validação de Schema (Pydantic) ---

def test_customer_schema_validation_error():
    """Garante que o Pydantic valida o tamanho mínimo do nome e formato de email."""
    # Nome muito curto (min_length=3)
    with pytest.raises(ValidationError):
        CustomerCreate(name="Ab", email="teste@email.com")

    # Email inválido
    with pytest.raises(ValidationError):
        CustomerCreate(name="Jose Silva", email="email-invalido")


# --- Testes do Repositório ---

def test_create_customer_repository_success(db_session):
    """Valida se o repositório executa corretamente o ciclo de criação no DB."""
    repository = CustomerRepository(db_session)
    customer_data = CustomerCreate(
        name="Jose Silva",
        email="jose@email.com",
        document="123456789"
    )

    # Act
    result = repository.create(customer_data)

    # Assert
    assert db_session.add.called
    assert db_session.commit.called
    assert db_session.refresh.called
    assert isinstance(result, Customer)
    assert result.name == "Jose Silva"


def test_get_all_paginated_customers(db_session):
    """Valida se a estrutura de retorno da paginação está correta."""
    repository = CustomerRepository(db_session)

    # Configurar Mocks para o query.count() e query.offset().limit().all()
    mock_query = db_session.query.return_value
    mock_query.count.return_value = 10
    mock_query.offset.return_value.limit.return_value.all.return_value = [
        Customer(id=1, name="Cliente 1", email="c1@email.com")
    ]

    # Act
    result = repository.get_all_paginated(skip=0, limit=5)

    # Assert
    assert result["total"] == 10
    assert len(result["items"]) == 1
    assert result["items"][0].name == "Cliente 1"