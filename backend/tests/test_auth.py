import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_auth_flow():
    # Register new user
    reg_payload = {
        "username": "nurse_kavita",
        "email": "kavita@maternacare.org",
        "password": "SecurePassword123!",
        "full_name": "Kavita Sharma (Staff Nurse)",
        "role": "NURSE"
    }
    res = client.post("/api/v1/auth/register", json=reg_payload)
    assert res.status_code in [200, 201, 400]  # 400 if already exists

    # Login
    login_res = client.post("/api/v1/auth/login", json={
        "username": "nurse_kavita",
        "password": "SecurePassword123!"
    })
    assert login_res.status_code == 200
    token_data = login_res.json()
    assert "access_token" in token_data
    assert token_data["role"] == "NURSE"


def test_root_and_health():
    res = client.get("/")
    assert res.status_code == 200
    assert res.json()["status"] == "OPERATIONAL"

    health = client.get("/health")
    assert health.status_code == 200
    assert health.json()["status"] == "healthy"
