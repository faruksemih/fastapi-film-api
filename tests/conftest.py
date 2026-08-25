import pytest

from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from film_api.app import app
from film_api.database import get_session

@pytest.fixture
def client():
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )

    SQLModel.metadata.create_all(test_engine)
    with Session(test_engine) as session:
        def get_session_ovveride():
            yield session
        app.dependency_overrides[get_session] = get_session_ovveride
        with TestClient(app) as test_client:
            yield test_client
        app.dependency_overrides.clear()