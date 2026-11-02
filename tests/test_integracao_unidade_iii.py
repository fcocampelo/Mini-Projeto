"""Atividade Unidade III: integração API -> Service -> Repository/Advisor.

Gerado com apoio do ChatGPT a partir do código de fcocampelo/Mini-Projeto.
Executar na RAIZ do repositório: python -m pytest tests/test_integracao_unidade_iii.py -v
"""
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.api import task_routes
from app.repositories.task_repository import TaskRepository
from app.services.priority_advisor import PriorityAdvisor
from app.services.task_service import TaskService
from app.services import priority_advisor


@pytest.fixture
def client(monkeypatch):
    """Isola armazenamento e evita chave real de IA entre casos."""
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    original_service = task_routes._task_service
    task_routes._task_service = TaskService(TaskRepository(), PriorityAdvisor(api_key=""))
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        task_routes._task_service = original_service


def create(client, title="Tarefa valida", **others):
    response = client.post("/tasks", json={"title": title, **others})
    assert response.status_code == 201, response.text
    return response.json()


def test_it_f01_criar_e_consultar(client):
    """IT-F01: o POST deve persistir campos e GET recuperar a tarefa."""
    task = create(client, "Preparar relatorio")
    assert isinstance(task["id"], int)
    assert task["created_at"]
    assert task["status"] == "pendente"
    assert task["priority"] == "media"
    response = client.get(f'/tasks/{task["id"]}')
    assert response.status_code == 200
    assert response.json() == task


def test_it_f02_listar_duas_tarefas(client):
    """IT-F02: dois POSTs aparecem na listagem, com IDs distintos."""
    a = create(client, "Primeira tarefa")
    b = create(client, "Segunda tarefa")
    response = client.get("/tasks")
    assert response.status_code == 200
    assert {x["id"] for x in response.json()} == {a["id"], b["id"]}
    assert {x["title"] for x in response.json()} == {"Primeira tarefa", "Segunda tarefa"}


def test_it_f03_atualizacao_parcial(client):
    """IT-F03: PUT parcial preserva campos não informados."""
    task = create(client, "Prioridade definida", description="Descricao original", priority="alta")
    response = client.put(f'/tasks/{task["id"]}', json={"status": "concluida"})
    assert response.status_code == 200
    persisted = client.get(f'/tasks/{task["id"]}').json()
    assert persisted["status"] == "concluida"
    assert persisted["title"] == task["title"]
    assert persisted["description"] == task["description"]
    assert persisted["priority"] == task["priority"]
    assert persisted["updated_at"] is not None


def test_it_f04_excluir_e_consultar(client):
    """IT-F04: DELETE elimina objeto da consulta posterior."""
    task = create(client, "Excluir tarefa")
    response = client.delete(f'/tasks/{task["id"]}')
    assert response.status_code == 204
    assert response.content == b""
    subsequent = client.get(f'/tasks/{task["id"]}')
    assert subsequent.status_code == 404
    assert subsequent.json()["detail"] == "Task not found"


def test_it_f05_limites_validos_do_titulo(client):
    """IT-F05: títulos de 3 e 120 caracteres são aceitos e recuperados."""
    for title in ("abc", "X" * 120):
        task = create(client, title)
        response = client.get(f'/tasks/{task["id"]}')
        assert response.status_code == 200
        assert response.json()["title"] == title


def test_it_f06_normalizacao_do_titulo(client):
    """IT-F06: título é normalizado antes de persistir."""
    task = create(client, "  Tarefa ajustada  ")
    assert task["title"] == "Tarefa ajustada"
    assert client.get(f'/tasks/{task["id"]}').json()["title"] == "Tarefa ajustada"


def test_it_f07_atualizar_titulo_preserva_outros_campos(client):
    """IT-F07: atualizar somente título mantém descrição e prioridade."""
    task = create(client, "Titulo original", description="Texto original", priority="alta")
    response = client.put(f'/tasks/{task["id"]}', json={"title": "Titulo revisado"})
    assert response.status_code == 200
    persisted = client.get(f'/tasks/{task["id"]}').json()
    assert persisted["title"] == "Titulo revisado"
    assert persisted["description"] == "Texto original"
    assert persisted["priority"] == "alta"


def test_it_f08_prioridade_manual_preservada(client):
    """IT-F08: auto_priority=false não aplica heurística."""
    response = client.post("/tasks?auto_priority=false", json={"title": "Resolver urgente", "priority": "baixa"})
    assert response.status_code == 201
    task = response.json()
    assert client.get(f'/tasks/{task["id"]}').json()["priority"] == "baixa"


def test_it_r01_titulo_curto(client):
    """IT-R01: título menor que mínimo retorna 422 e não persiste."""
    assert client.post("/tasks", json={"title": "ab"}).status_code == 422
    assert client.get("/tasks").json() == []


def test_it_r02_titulo_longo(client):
    """IT-R02: título maior que máximo retorna 422 e não persiste."""
    assert client.post("/tasks", json={"title": "X" * 121}).status_code == 422
    assert client.get("/tasks").json() == []


def test_it_r03_prioridade_invalida(client):
    """IT-R03: enum de prioridade inválido retorna 422."""
    assert client.post("/tasks", json={"title": "Revisar demanda", "priority": "extrema"}).status_code == 422
    assert client.get("/tasks").json() == []


def test_it_r04_put_invalido_preserva_estado(client):
    """IT-R04: falha de validação em PUT não altera a tarefa."""
    task = create(client, "Manter situacao", priority="alta")
    before = client.get(f'/tasks/{task["id"]}').json()
    assert client.put(f'/tasks/{task["id"]}', json={"status": "parada"}).status_code == 422
    after = client.get(f'/tasks/{task["id"]}').json()
    assert after == before


def test_it_r05_id_inexistente(client):
    """IT-R05: GET, PUT e DELETE retornam 404 quando ID não existe."""
    path = "/tasks/99999"
    responses = (client.get(path), client.put(path, json={"title": "Tarefa inexistente"}), client.delete(path))
    for response in responses:
        assert response.status_code == 404
        assert response.json()["detail"] == "Task not found"
    assert client.get("/tasks").json() == []


def test_it_r06_heuristica_sem_chave(client):
    """IT-R06: auto_priority=true sem API key usa heurística crítica."""
    response = client.post("/tasks?auto_priority=true", json={"title": "Incidente urgente"})
    assert response.status_code == 201
    task = response.json()
    assert client.get(f'/tasks/{task["id"]}').json()["priority"] == "critica"


def test_it_r07_timeout_fallback(client, monkeypatch):
    """IT-R07: erro de timeout da LLM é recuperado sem rede externa."""
    def timeout(*args, **kwargs):
        raise TimeoutError("timeout de teste")
    monkeypatch.setattr(priority_advisor, "urlopen", timeout)
    task_routes._task_service = TaskService(TaskRepository(), PriorityAdvisor(api_key="fake-test-key"))
    response = client.post("/tasks?auto_priority=true", json={"title": "Erro no sistema"})
    assert response.status_code == 201
    task = response.json()
    assert client.get(f'/tasks/{task["id"]}').json()["priority"] == "alta"


def test_it_r08_json_invalido_fallback(client, monkeypatch):
    """IT-R08: resposta JSON inválida da LLM usa fallback sem rede externa."""
    class InvalidResponse:
        def __enter__(self):
            return self
        def __exit__(self, *args):
            return False
        def read(self):
            return b"{invalid-json"
    def fake_urlopen(*args, **kwargs):
        return InvalidResponse()
    monkeypatch.setattr(priority_advisor, "urlopen", fake_urlopen)
    task_routes._task_service = TaskService(TaskRepository(), PriorityAdvisor(api_key="fake-test-key"))
    response = client.post("/tasks?auto_priority=true", json={"title": "Atualizar documentacao"})
    assert response.status_code == 201
    task = response.json()
    assert client.get(f'/tasks/{task["id"]}').json()["priority"] == "baixa"
