from fastapi.testclient import TestClient
from fastapi import status
from app.main import app
import uuid
client = TestClient(app)


def test_create_user():
    unique_id = str(uuid.uuid4())[:8]
    username = f"admin_{unique_id}"
    email = f"{username}@example.com"
    response = client.post(url="/users/",
                           json={
                               "username": username,
                               "email": email,
                               "password": "12345678",
                               "first_name": "admin",
                               "last_name": "admin"
                           })
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["username"] == username
    assert response.json()["email"] == email