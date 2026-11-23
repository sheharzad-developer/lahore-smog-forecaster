from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "database": "connected",
    }


def test_stations_endpoint():
    response = client.get("/api/stations")
    assert response.status_code == 200
    assert "stations" in response.json()


def test_summary_endpoint():
    response = client.get("/api/summary")
    assert response.status_code == 200
    assert "total_stations" in response.json()


def test_history_endpoint():
    response = client.get("/api/history/weekly")
    assert response.status_code == 200


def test_invalid_history_range():
    response = client.get("/api/history/invalid")
    assert response.status_code == 400
    assert response.json()["error_code"] == "BAD_REQUEST"