import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from app.core.dependencies import get_session
from app.main import app
import app.models  # noqa: F401 - registra metadatos


def create_test_engine():
    return create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})


@pytest.fixture(scope="session")
def engine():
    engine = create_test_engine()
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)


@pytest.fixture
def client(engine):
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

    def get_session_override():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = get_session_override
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
