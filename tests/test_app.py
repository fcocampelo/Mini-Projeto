from fastapi.testclient import TestClient

from app.main import app


def test_health_returns_200() -> None:
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert "timestamp" in response.json()


def test_tasks_router_is_registered_in_main_app() -> None:
    client = TestClient(app)

    response = client.get("/tasks")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
