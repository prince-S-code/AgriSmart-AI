from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def auth_headers():
    email = f"test{__import__('time').time_ns()}@example.com"
    response = client.post("/api/auth/register", json={
        "full_name": "Test Farmer", "email": email, "mobile_number": "9876543210",
        "password": "Strong123", "confirm_password": "Strong123",
        "state": "Gujarat", "district": "Anand", "village": "Test"
    })
    assert response.status_code == 201
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["database"] == "sqlite"


def test_crop_validation():
    response = client.post("/api/crop/recommend", headers=auth_headers(), json={
        "nitrogen": -1, "phosphorus": 40, "potassium": 40,
        "temperature": 25, "humidity": 70, "ph": 6.5, "rainfall": 200
    })
    assert response.status_code == 422


def test_disease_rejects_bad_type():
    response = client.post("/api/disease/predict", headers=auth_headers(), files={"image": ("test.txt", b"hello", "text/plain")})
    assert response.status_code == 400
