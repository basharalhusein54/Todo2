import json

from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

from app.db.database import Base
from app.db.database import get_db
from app.crud.auth import authorize_user
from app.main import app
from app.models.users import Users

url = settings.testing_database_url
connect_args = {"check_same_thread": False} if url.startswith("sqlite") else {}
engine = create_engine(url, connect_args=connect_args,poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#very important to use the same Base because all metadata there.

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
    return {"sub":"admin","role":"superuser"}
def override_authorize_user():
    return {"sub":"admin","role":"user"}

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[authorize_user] = override_authorize_superuser


client = TestClient(app)


json_data = {
    "username": "alice123",
    "email": "alice1@example.com",
    "password": "password1",
    "first_name": "Alice",
    "last_name": "Anderson"
  }

def test_create_user():
    response = client.post("/users/create_user", json=json_data)
    assert response.status_code == status.HTTP_201_CREATED,"test_create_user"

def test_read_all_users():
    response = client.get(url="/users/get_users")
    assert response.status_code == status.HTTP_200_OK,"test_read_all_users"
    users = response.json()
    assert isinstance(users, list), "Expected a list of users"
    assert len(users) > 0, "User list is empty"
    matching_user = next((user for user in users if user["username"] == json_data["username"]), None)
    assert matching_user is not None, "Expected user to be found"
    assert matching_user["email"] == json_data["email"], "Email mismatch"
    assert matching_user["first_name"] == json_data["first_name"], "First name mismatch"
    assert matching_user["last_name"] == json_data["last_name"], "Last name mismatch"
    assert matching_user["is_active"] is True, "Expected user to be active"
    assert matching_user["role"] == "user", "Expected role to be 'user'"
    assert matching_user["is_superuser"] is False, "Expected is_superuser to be False"
