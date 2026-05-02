from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TaskStatus(StrEnum):
    """Status permitidos para uma tarefa."""

    PENDING = "pendente"
    IN_PROGRESS = "em_andamento"
    DONE = "concluida"
    CANCELED = "cancelada"


class TaskPriority(StrEnum):
    """Prioridades permitidas para uma tarefa."""

    LOW = "baixa"
    MEDIUM = "media"
    HIGH = "alta"
    CRITICAL = "critica"


class TaskBase(BaseModel):
    """Campos compartilhados da tarefa."""

    title: str = Field(..., min_length=3, max_length=120)
    description: str | None = Field(default=None, max_length=1000)
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        title = value.strip()
        if not title:
            raise ValueError("title must not be blank")
        return title

    @field_validator("description")
    @classmethod
    def normalize_description(cls, value: str | None) -> str | None:
        if value is None:
            return None

        description = value.strip()
        return description or None


class TaskCreate(TaskBase):
    """Dados para criar uma tarefa."""


class TaskUpdate(BaseModel):
    """Dados para atualizar uma tarefa."""

    title: str | None = Field(default=None, min_length=3, max_length=120)
    description: str | None = Field(default=None, max_length=1000)
    status: TaskStatus | None = None
    priority: TaskPriority | None = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str | None) -> str | None:
        if value is None:
            return None

        title = value.strip()
        if not title:
            raise ValueError("title must not be blank")
        return title

    @field_validator("description")
    @classmethod
    def normalize_description(cls, value: str | None) -> str | None:
        if value is None:
            return None

        description = value.strip()
        return description or None


class TaskOut(TaskBase):
    """Dados retornados pela API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime | None = None
