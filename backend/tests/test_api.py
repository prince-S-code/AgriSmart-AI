from fastapi.testclient import TestClient
from app.main import app
from app.api import disease as disease_api
from app.database import sqlite as sqlite_database

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


def test_disease_returns_both_model_predictions(monkeypatch, tmp_path):
    monkeypatch.setattr(disease_api, "UPLOAD_DIR", tmp_path)
    monkeypatch.setattr(disease_api.disease_service, "predict", lambda _: {
        "crop_name": "Tomato",
        "predicted_disease": "Tomato___healthy",
        "confidence": 0.96,
        "test_accuracy": 0.9656,
        "model_used": "MobileNetV2",
        "low_confidence": False,
        "description": "Healthy plant.",
        "severity": "low",
        "treatment_steps": [],
    })
    monkeypatch.setattr(disease_api.yolo_service, "predict", lambda _: {
        "model": "YOLOv8",
        "predicted_disease": "Tomato___healthy",
        "confidence": 0.91,
        "test_accuracy": None,
        "detections": [{"class_name": "Tomato___healthy", "confidence": 0.91}],
    })

    response = client.post(
        "/api/disease/predict",
        headers=auth_headers(),
        files={"image": ("leaf.jpg", b"mock image", "image/jpeg")},
    )

    assert response.status_code == 200
    results = response.json()["model_results"]
    assert [result["model"] for result in results] == ["MobileNetV2 CNN", "YOLOv8"]
    assert results[0]["test_accuracy"] == 0.9656
    assert results[1]["test_accuracy"] is None


def test_production_database_does_not_seed_demo_account(monkeypatch, tmp_path):
    monkeypatch.setattr(sqlite_database.settings, "app_env", "production")
    monkeypatch.setattr(sqlite_database, "DB_PATH", tmp_path / "production.db")

    sqlite_database.init_db()
    conn = sqlite_database.get_db()
    user_count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    conn.close()

    assert user_count == 0
