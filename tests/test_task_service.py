import pytest

from app.models.task import TaskCreate, TaskPriority, TaskStatus, TaskUpdate
from app.repositories.task_repository import TaskRepository
from app.services.task_service import TaskService


@pytest.fixture
def task_service() -> TaskService:
    return TaskService(repository=TaskRepository())


@pytest.fixture
def task_create() -> TaskCreate:
    return TaskCreate(
        title="Implementar endpoint de tarefas",
        description="Criar fluxo inicial para cadastro de tarefas",
        priority=TaskPriority.HIGH,
    )


def test_create_task_returns_task_with_generated_id(
    task_service: TaskService,
    task_create: TaskCreate,
) -> None:
    created_task = task_service.create(task_create)

    assert created_task.id == 1
    assert created_task.title == task_create.title
    assert created_task.description == task_create.description
    assert created_task.status == TaskStatus.PENDING
    assert created_task.priority == TaskPriority.HIGH
    assert created_task.created_at is not None
    assert created_task.updated_at is None


def test_list_tasks_returns_created_tasks(
    task_service: TaskService,
    task_create: TaskCreate,
) -> None:
    first_task = task_service.create(task_create)
    second_task = task_service.create(
        TaskCreate(title="Revisar documentacao", priority=TaskPriority.LOW)
    )

    tasks = task_service.list()

    assert tasks == [first_task, second_task]


def test_update_task_changes_existing_task(
    task_service: TaskService,
    task_create: TaskCreate,
) -> None:
    created_task = task_service.create(task_create)

    updated_task = task_service.update(
        created_task.id,
        TaskUpdate(
            title="Implementar CRUD de tarefas",
            status=TaskStatus.IN_PROGRESS,
            priority=TaskPriority.CRITICAL,
        ),
    )

    assert updated_task is not None
    assert updated_task.id == created_task.id
    assert updated_task.title == "Implementar CRUD de tarefas"
    assert updated_task.description == created_task.description
    assert updated_task.status == TaskStatus.IN_PROGRESS
    assert updated_task.priority == TaskPriority.CRITICAL
    assert updated_task.created_at == created_task.created_at
    assert updated_task.updated_at is not None


def test_delete_task_removes_existing_task(
    task_service: TaskService,
    task_create: TaskCreate,
) -> None:
    created_task = task_service.create(task_create)

    deleted = task_service.delete(created_task.id)

    assert deleted is True
    assert task_service.get_by_id(created_task.id) is None
    assert task_service.list() == []


def test_get_update_and_delete_return_not_found_result_for_unknown_id(
    task_service: TaskService,
) -> None:
    assert task_service.get_by_id(999) is None
    assert task_service.update(999, TaskUpdate(title="Tarefa inexistente")) is None
    assert task_service.delete(999) is False
