from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_chat_route():
    response = client.post(
        "/api/chat",
        json={"message": "Hello there", "user_id": "user-123"},
    )
    assert response.status_code == 200
    assert "reply" in response.json()
