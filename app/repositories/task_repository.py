from datetime import datetime, timezone

from app.models.task import TaskCreate, TaskOut, TaskUpdate


class TaskRepository:
    """Repositorio em memoria para tarefas."""

    def __init__(self) -> None:
        self._tasks: dict[int, TaskOut] = {}
        self._next_id = 1

    def create(self, task: TaskCreate) -> TaskOut:
        """Cria uma nova tarefa."""
        task_id = self._next_id
        self._next_id += 1

        now = datetime.now(timezone.utc)
        created_task = TaskOut(
            id=task_id,
            created_at=now,
            updated_at=None,
            **task.model_dump(),
        )

        self._tasks[task_id] = created_task
        return self._copy(created_task)

    def list(self) -> list[TaskOut]:
        """Lista todas as tarefas."""
        return [self._copy(task) for task in self._tasks.values()]

    def get_by_id(self, task_id: int) -> TaskOut | None:
        """Busca uma tarefa pelo identificador."""
        task = self._tasks.get(task_id)
        if task is None:
            return None

        return self._copy(task)

    def update(self, task_id: int, task_update: TaskUpdate) -> TaskOut | None:
        """Atualiza uma tarefa existente."""
        current_task = self._tasks.get(task_id)
        if current_task is None:
            return None

        update_data = task_update.model_dump(exclude_unset=True)
        updated_task = current_task.model_copy(
            update={
                **update_data,
                "updated_at": datetime.now(timezone.utc),
            }
        )

        self._tasks[task_id] = updated_task
        return self._copy(updated_task)

    def delete(self, task_id: int) -> bool:
        """Remove uma tarefa existente."""
        if task_id not in self._tasks:
            return False

        del self._tasks[task_id]
        return True

    @staticmethod
    def _copy(task: TaskOut) -> TaskOut:
        return task.model_copy()
