from fastapi.testclient import TestClient
from fastapi import status
from app.main import app
from app.api import auth

client = TestClient(app)
def test_login():
    response = client.post(url="/auth/login",
                           json={"username":"admin","password":"12345678"})
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()
    assert "access_token" in response.cookies
    assert "refresh_token" in response.cookies
