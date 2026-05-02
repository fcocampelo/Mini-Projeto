import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api import task_routes
from app.models.task import TaskCreate, TaskPriority
from app.repositories.task_repository import TaskRepository
from app.services.priority_advisor import PriorityAdvisor
from app.services.task_service import TaskService


class CriticalPriorityAdvisor:
    def suggest(self, task: TaskCreate) -> TaskPriority:
        return TaskPriority.CRITICAL


@pytest.fixture
def client() -> TestClient:
    original_task_service = task_routes._task_service
    task_routes._task_service = TaskService(
        repository=TaskRepository(),
        priority_advisor=PriorityAdvisor(api_key=""),
    )

    app = FastAPI()
    app.include_router(task_routes.router)

    try:
        yield TestClient(app)
    finally:
        task_routes._task_service = original_task_service


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


def test_create_task_with_minimal_payload_uses_defaults(client: TestClient) -> None:
    response = client.post(
        "/tasks",
        json={
            "title": "Criar tarefa simples",
        },
    )

    assert response.status_code == 201
    assert response.json()["title"] == "Criar tarefa simples"
    assert response.json()["description"] is None
    assert response.json()["status"] == "pendente"
    assert response.json()["priority"] == "media"


def test_create_task_with_auto_priority_uses_advisor(client: TestClient) -> None:
    task_routes._task_service = TaskService(
        repository=TaskRepository(),
        priority_advisor=CriticalPriorityAdvisor(),
    )

    response = client.post(
        "/tasks?auto_priority=true",
        json={
            "title": "Priorizar tarefa comum",
            "description": "Sem criterio local critico",
            "priority": "baixa",
        },
    )

    assert response.status_code == 201
    assert response.json()["priority"] == "critica"


def test_create_task_with_auto_priority_false_preserves_manual_priority(
    client: TestClient,
) -> None:
    task_routes._task_service = TaskService(
        repository=TaskRepository(),
        priority_advisor=CriticalPriorityAdvisor(),
    )

    response = client.post(
        "/tasks?auto_priority=false",
        json={
            "title": "Manter prioridade manual",
            "description": "Advisor nao deve sobrescrever",
            "priority": "baixa",
        },
    )

    assert response.status_code == 201
    assert response.json()["priority"] == "baixa"


def test_create_task_returns_422_for_invalid_payload(client: TestClient) -> None:
    response = client.post(
        "/tasks",
        json={
            "title": "ab",
            "priority": "invalida",
        },
    )

    assert response.status_code == 422


def test_list_tasks_returns_empty_list(client: TestClient) -> None:
    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == []


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


def test_update_task_allows_partial_payload(client: TestClient) -> None:
    created_response = client.post(
        "/tasks",
        json={
            "title": "Atualizar parcialmente",
            "description": "Descricao original",
            "priority": "media",
        },
    )
    task_id = created_response.json()["id"]

    response = client.put(
        f"/tasks/{task_id}",
        json={
            "status": "concluida",
        },
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Atualizar parcialmente"
    assert response.json()["description"] == "Descricao original"
    assert response.json()["status"] == "concluida"
    assert response.json()["priority"] == "media"


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


def test_delete_task_removes_task_from_repository(client: TestClient) -> None:
    created_response = client.post(
        "/tasks",
        json={
            "title": "Excluir e consultar",
            "description": "Validar remocao completa",
        },
    )
    task_id = created_response.json()["id"]

    delete_response = client.delete(f"/tasks/{task_id}")
    get_response = client.get(f"/tasks/{task_id}")

    assert delete_response.status_code == 204
    assert get_response.status_code == 404


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
    request = getattr(client, method)
    response = request(path, json=json) if json is not None else request(path)

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


@pytest.mark.parametrize(
    ("method", "path", "json"),
    [
        ("get", "/tasks/abc", None),
        ("put", "/tasks/1", {"priority": "invalida"}),
        ("delete", "/tasks/abc", None),
    ],
)
def test_task_routes_return_422_for_invalid_request(
    client: TestClient,
    method: str,
    path: str,
    json: dict[str, str] | None,
) -> None:
    request = getattr(client, method)
    response = request(path, json=json) if json is not None else request(path)

    assert response.status_code == 422
