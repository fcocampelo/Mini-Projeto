from urllib.error import URLError

import pytest

from app.models.task import TaskCreate, TaskPriority
from app.services import priority_advisor
from app.services.priority_advisor import PriorityAdvisor


@pytest.mark.parametrize(
    ("task", "expected_priority"),
    [
        (
            TaskCreate(
                title="Documentar fluxo de tarefas",
                description="Atualizar documentacao da API",
            ),
            TaskPriority.LOW,
        ),
        (
            TaskCreate(
                title="Corrigir bug no cadastro",
                description="Erro afeta cliente antes da release",
            ),
            TaskPriority.HIGH,
        ),
        (
            TaskCreate(
                title="Resolver bloqueio urgente em producao",
                description="Servico indisponivel para equipe interna",
            ),
            TaskPriority.CRITICAL,
        ),
    ],
)
def test_suggest_returns_local_priority_levels(
    monkeypatch: pytest.MonkeyPatch,
    task: TaskCreate,
    expected_priority: TaskPriority,
) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    advisor = PriorityAdvisor()

    assert advisor.suggest(task) == expected_priority


def test_suggest_falls_back_to_local_priority_when_llm_call_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    def raise_url_error(*args: object, **kwargs: object) -> None:
        raise URLError("timeout")

    monkeypatch.setattr(priority_advisor, "urlopen", raise_url_error)

    advisor = PriorityAdvisor(api_key="test-key", timeout_seconds=0.1)
    task = TaskCreate(
        title="Bug urgente em producao",
        description="Falha critica bloqueia o time",
        priority=TaskPriority.MEDIUM,
    )

    assert advisor.suggest(task) == TaskPriority.CRITICAL
