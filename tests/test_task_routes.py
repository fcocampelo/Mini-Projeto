import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api import task_routes
from app.repositories.task_repository import TaskRepository
from app.services.priority_advisor import PriorityAdvisor
from app.services.task_service import TaskService


@pytest.fixture
def client() -> TestClient:
    task_routes._task_service = TaskService(
        repository=TaskRepository(),
        priority_advisor=PriorityAdvisor(api_key=""),
    )

    app = FastAPI()
    app.include_router(task_routes.router)

    return TestClient(app)


def test_create_task_returns_201(client: TestClient) -> None:
    response = client.post(
        "/tasks",
        json={
            "title": "Implementar rotas de tarefas",
            "description": "Criar endpoints CRUD",
            "priority": "alta",
        },
    )

    assert response.status_code == 201
    assert response.json()["id"] == 1
    assert response.json()["title"] == "Implementar rotas de tarefas"
    assert response.json()["priority"] == "alta"


def test_list_tasks_returns_200(client: TestClient) -> None:
    client.post(
        "/tasks",
        json={
            "title": "Listar tarefas",
            "description": "Validar endpoint de listagem",
        },
    )

    response = client.get("/tasks")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Listar tarefas"


def test_get_task_by_id_returns_200(client: TestClient) -> None:
    created_response = client.post(
        "/tasks",
        json={
            "title": "Consultar tarefa",
            "description": "Validar busca por ID",
        },
    )
    task_id = created_response.json()["id"]

    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json()["id"] == task_id
    assert response.json()["title"] == "Consultar tarefa"


def test_update_task_returns_200(client: TestClient) -> None:
    created_response = client.post(
        "/tasks",
        json={
            "title": "Atualizar tarefa",
            "description": "Validar alteracao",
        },
    )
    task_id = created_response.json()["id"]

    response = client.put(
        f"/tasks/{task_id}",
        json={
            "title": "Atualizar tarefa existente",
            "status": "em_andamento",
            "priority": "critica",
        },
    )

    assert response.status_code == 200
    assert response.json()["id"] == task_id
    assert response.json()["title"] == "Atualizar tarefa existente"
    assert response.json()["status"] == "em_andamento"
    assert response.json()["priority"] == "critica"


def test_delete_task_returns_204(client: TestClient) -> None:
    created_response = client.post(
        "/tasks",
        json={
            "title": "Remover tarefa",
            "description": "Validar exclusao",
        },
    )
    task_id = created_response.json()["id"]

    response = client.delete(f"/tasks/{task_id}")

    assert response.status_code == 204
    assert response.content == b""


@pytest.mark.parametrize(
    ("method", "path", "json"),
    [
        ("get", "/tasks/999", None),
        ("put", "/tasks/999", {"title": "Tarefa inexistente"}),
        ("delete", "/tasks/999", None),
    ],
)
def test_task_routes_return_404_for_unknown_id(
    client: TestClient,
    method: str,
    path: str,
    json: dict[str, str] | None,
) -> None:
    response = getattr(client, method)(path, json=json)

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"
