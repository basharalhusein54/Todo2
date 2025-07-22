from http.client import responses

from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

from app.db.database import Base
from app.db.database import get_db
from app.crud.auth import authorize_user
from app.main import app
from unittest.mock import patch
from sqlalchemy.exc import OperationalError, IntegrityError

url = settings.testing_database_url
connect_args = {"check_same_thread": False} if url.startswith("sqlite") else {}
engine = create_engine(url, connect_args=connect_args, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

import pytest


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    # Create tables before tests
    Base.metadata.create_all(engine)
    yield
    # Drop tables after tests
    Base.metadata.drop_all(engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_authorize_superuser():
    return {"sub": "admin", "role": "superuser"}


def override_authorize_user():
    return {"sub": "admin", "role": "user"}


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

json_data = {
    "username": "alice123",
    "email": "alice1@example.com",
    "password": "password1",
    "first_name": "Alice",
    "last_name": "Anderson",
    "role":"user"
}


@pytest.mark.order(1)
def test_create_user_as_superuser():
    app.dependency_overrides[authorize_user] = override_authorize_superuser
    response = client.post("/users/create_user", json=json_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() ==  {
    "username": "alice123",
    "email": "alice1@example.com",
    "first_name": "Alice",
    "last_name": "Anderson",
        "role":"user"
}


@pytest.mark.order(2)
def test_read_all_users_superuser():
    app.dependency_overrides[authorize_user] = override_authorize_superuser
    response = client.get(url="/users/get_users")
    assert response.status_code == status.HTTP_200_OK, "test_read_all_users"
    users = response.json()
    assert isinstance(users, list), "Expected a list of users"
    assert len(users) > 0, "User list is empty"


@pytest.mark.order(3)
@patch("sqlalchemy.orm.Session.commit", side_effect=IntegrityError("msg", {}, None))
def test_integrity_error_on_commit(mock_commit):
    app.dependency_overrides[authorize_user] = override_authorize_superuser
    response = client.post("/users/create_user", json=json_data)
    assert response.status_code == status.HTTP_409_CONFLICT



@pytest.mark.order(4)
@patch("sqlalchemy.orm.Session.commit", side_effect=OperationalError("msg", {}, None))
def test_operational_error_on_commit(mock_commit):
    app.dependency_overrides[authorize_user] = override_authorize_superuser
    response = client.post("/users/create_user", json=json_data)
    assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE

@pytest.mark.order(5)
def test_get_user_by_username_as_superuser():
    app.dependency_overrides[authorize_user] = override_authorize_superuser
    response = client.get("/users/get_user/alice123")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
    "username": "alice123",
    "email": "alice1@example.com",
    "first_name": "Alice",
    "last_name": "Anderson",
        "role":"user"
}
@pytest.mark.order(6)
def test_get_wrong_user_by_username_as_superuser():
    app.dependency_overrides[authorize_user] = override_authorize_superuser
    response = client.get("/users/get_user/ghost")
    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.order(7)
def test_get_wrong_user_by_id_as_superuser():
    app.dependency_overrides[authorize_user] = override_authorize_superuser
    response = client.get("/users/get_user_by_id/0")
    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.order(8)
def test_create_user_as_normal_user():
    app.dependency_overrides[authorize_user] = override_authorize_user
    response = client.post("/users/create_user", json=json_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.order(9)
def test_read_all_users_as_normal_user():
    app.dependency_overrides[authorize_user] = override_authorize_user
    response = client.get(url="/users/get_users")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.order(10)
def test_delete_user():
    app.dependency_overrides[authorize_user] = override_authorize_superuser
    response = client.delete("/users/delete_user/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT
