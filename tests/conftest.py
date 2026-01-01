import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session

@pytest.fixture
def db_session():
    return MagicMock(spec=Session)