from urllib.error import URLError

import pytest

from app.models.task import TaskCreate, TaskPriority
from app.services import priority_advisor
from app.services.priority_advisor import PriorityAdvisor


class FakeResponse:
    def __enter__(self) -> "FakeResponse":
        return self

    def __exit__(self, *args: object) -> None:
        return None

    def read(self) -> bytes:
        return b'{"output_text": "alta"}'


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


def test_suggest_uses_valid_llm_response_when_available(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    def fake_urlopen(*args: object, **kwargs: object) -> FakeResponse:
        return FakeResponse()

    monkeypatch.setattr(priority_advisor, "urlopen", fake_urlopen)

    advisor = PriorityAdvisor(api_key="test-key")
    task = TaskCreate(
        title="Triar demanda comum",
        description="Sem urgencia explicita",
        priority=TaskPriority.MEDIUM,
    )

    assert advisor.suggest(task) == TaskPriority.HIGH


def test_suggest_falls_back_when_llm_call_times_out(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    def raise_timeout(*args: object, **kwargs: object) -> None:
        raise TimeoutError("request timed out")

    monkeypatch.setattr(priority_advisor, "urlopen", raise_timeout)

    advisor = PriorityAdvisor(api_key="test-key", timeout_seconds=0.1)
    task = TaskCreate(
        title="Atualizar documentacao",
        description="Melhoria simples no README",
        priority=TaskPriority.MEDIUM,
    )

    assert advisor.suggest(task) == TaskPriority.LOW
