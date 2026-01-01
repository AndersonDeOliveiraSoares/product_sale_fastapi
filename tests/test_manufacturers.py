import pytest
from unittest.mock import MagicMock
from app.controller.manufacturer_controller import ManufacturerController
from app.repositories.manufacturer_repository import ManufacturerRepository
from app.schemas.manufacturer import ManufacturerCreate
from app.models.manufacturer import Manufacturer


@pytest.fixture
def db_session():
    return MagicMock()


# --- Testes do Controller ---

def test_create_manufacturer_controller_calls_repository(db_session):
    # Arrange
    controller = ManufacturerController(db_session)
    # Mock do repositório para não precisar testar o banco aqui
    controller.repository = MagicMock()

    data = ManufacturerCreate(name="Tech Corp", contact_email="tech@corp.com")

    # Act
    controller.create_manufacturer(data)

    # Assert: Verifica se o controller repassou os dados corretamente para o repository
    controller.repository.create.assert_called_once_with(
        name="Tech Corp",
        contact_email="tech@corp.com"
    )


# --- Testes do Repository ---

def test_create_manufacturer_repository_success(db_session):
    # Arrange
    repository = ManufacturerRepository(db_session)
    name = "Industrial Ltda"
    email = "contato@industrial.com"

    # Act
    result = repository.create(name=name, contact_email=email)

    # Assert
    assert db_session.add.called
    assert db_session.commit.called
    assert db_session.refresh.called
    assert isinstance(result, Manufacturer)


def test_get_all_paginated(db_session):
    # Arrange
    repository = ManufacturerRepository(db_session)
    mock_query = db_session.query.return_value

    # Simula o retorno do count e da lista de itens
    mock_query.count.return_value = 1
    mock_query.offset.return_value.limit.return_value.all.return_value = [
        Manufacturer(id=1, name="Factory A")
    ]

    # Act
    result = repository.get_all_paginated(skip=0, limit=10)

    # Assert
    assert result["total"] == 1
    assert len(result["items"]) == 1
    assert result["items"][0].name == "Factory A"