import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from app import crud
from app.core.dependencies import get_session
from app.core.security import get_password_hash
from app.main import app
from app.schemas import UserCreate
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


@pytest.fixture
def admin_payload():
    return {
        "user_id": "adm001",
        "name": "Admin User",
        "email": "admin@example.com",
        "profile": "admin", 
        "role": "admin",
        "password": "secret123",
    }


@pytest.fixture
def user_payload():
    return {
        "user_id": "u001",
        "name": "Test User",
        "email": "user@example.com",
        "profile": "tester",
        "role": "user",
        "password": "secret123",
    }


@pytest.fixture
def create_user(client, engine):
    def _create_user(payload: dict):
        user_in = UserCreate(**payload)
        hashed = get_password_hash(payload["password"])
        with Session(engine) as session:
            return crud.create_user(session, user_in, hashed)

    return _create_user


@pytest.fixture
def auth_token(client, create_user, admin_payload):
    create_user(admin_payload)
    response = client.post(
        "/auth/login",
        data={"username": admin_payload["email"], "password": admin_payload["password"]},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture
def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}


@pytest.fixture
def user_token(client, create_user, user_payload):
    create_user(user_payload)
    response = client.post(
        "/auth/login",
        data={"username": user_payload["email"], "password": user_payload["password"]},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture
def user_headers(user_token):
    return {"Authorization": f"Bearer {user_token}"}
