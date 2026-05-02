import json
import os
import socket
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from app.models.task import TaskCreate, TaskPriority


class PriorityAdvisor:
    """Sugere prioridade com heuristica local e LLM opcional."""

    _OPENAI_URL = "https://api.openai.com/v1/responses"
    _DEFAULT_MODEL = "gpt-4.1-mini"
    _DEFAULT_TIMEOUT_SECONDS = 5.0

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
        timeout_seconds: float | None = None,
    ) -> None:
        self._api_key = api_key or os.getenv("OPENAI_API_KEY")
        self._model = model or os.getenv("OPENAI_MODEL", self._DEFAULT_MODEL)
        self._timeout_seconds = timeout_seconds or self._read_timeout()

    def suggest(self, task: TaskCreate) -> TaskPriority:
        """Sugere prioridade com fallback local obrigatorio."""
        fallback_priority = self._suggest_locally(task)

        if not self._api_key:
            return fallback_priority

        return self._suggest_with_llm(task) or fallback_priority

    def _suggest_locally(self, task: TaskCreate) -> TaskPriority:
        text = self._task_text(task)

        critical_terms = (
            "critico",
            "critica",
            "urgente",
            "bloqueio",
            "bloqueador",
            "producao",
            "indisponivel",
            "seguranca",
            "vazamento",
        )
        high_terms = (
            "alta",
            "cliente",
            "erro",
            "falha",
            "bug",
            "prazo",
            "hoje",
            "amanha",
            "release",
        )
        low_terms = (
            "baixa",
            "documentacao",
            "documentar",
            "refatorar",
            "melhoria",
            "ajuste visual",
        )

        if self._contains_any(text, critical_terms):
            return TaskPriority.CRITICAL

        if self._contains_any(text, high_terms):
            return TaskPriority.HIGH

        if self._contains_any(text, low_terms):
            return TaskPriority.LOW

        return task.priority

    def _suggest_with_llm(self, task: TaskCreate) -> TaskPriority | None:
        try:
            request = Request(
                self._OPENAI_URL,
                data=self._build_payload(task),
                headers={
                    "Authorization": f"Bearer {self._api_key}",
                    "Content-Type": "application/json",
                },
                method="POST",
            )

            with urlopen(request, timeout=self._timeout_seconds) as response:
                response_body = response.read().decode("utf-8")

            return self._parse_priority(response_body)
        except (HTTPError, URLError, TimeoutError, socket.timeout, OSError, ValueError):
            return None

    def _build_payload(self, task: TaskCreate) -> bytes:
        payload = {
            "model": self._model,
            "input": [
                {
                    "role": "system",
                    "content": (
                        "Voce sugere prioridade para tarefas internas. "
                        "Responda apenas uma palavra: baixa, media, alta ou critica."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Titulo: {task.title}\n"
                        f"Descricao: {task.description or ''}\n"
                        f"Status: {task.status.value}\n"
                        f"Prioridade atual: {task.priority.value}"
                    ),
                },
            ],
            "max_output_tokens": 10,
        }
        return json.dumps(payload).encode("utf-8")

    def _parse_priority(self, response_body: str) -> TaskPriority | None:
        data = json.loads(response_body)

        candidates = [
            data.get("output_text"),
            self._extract_output_text(data),
        ]

        for candidate in candidates:
            if not candidate:
                continue

            priority = self._priority_from_text(candidate)
            if priority is not None:
                return priority

        return None

    def _extract_output_text(self, data: dict[str, object]) -> str | None:
        output = data.get("output")
        if not isinstance(output, list):
            return None

        texts: list[str] = []
        for item in output:
            if not isinstance(item, dict):
                continue

            content = item.get("content")
            if not isinstance(content, list):
                continue

            for content_item in content:
                if not isinstance(content_item, dict):
                    continue

                text = content_item.get("text")
                if isinstance(text, str):
                    texts.append(text)

        return " ".join(texts) if texts else None

    def _priority_from_text(self, text: str) -> TaskPriority | None:
        normalized_text = self._normalize(text)

        for priority in TaskPriority:
            if priority.value in normalized_text:
                return priority

        return None

    def _task_text(self, task: TaskCreate) -> str:
        return self._normalize(f"{task.title} {task.description or ''}")

    @staticmethod
    def _contains_any(text: str, terms: tuple[str, ...]) -> bool:
        return any(term in text for term in terms)

    @staticmethod
    def _normalize(text: str) -> str:
        return text.strip().lower()

    def _read_timeout(self) -> float:
        raw_timeout = os.getenv("OPENAI_TIMEOUT_SECONDS")
        if raw_timeout is None:
            return self._DEFAULT_TIMEOUT_SECONDS

        try:
            timeout = float(raw_timeout)
        except ValueError:
            return self._DEFAULT_TIMEOUT_SECONDS

        return timeout if timeout > 0 else self._DEFAULT_TIMEOUT_SECONDS
