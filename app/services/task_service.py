from app.models.task import TaskCreate, TaskOut, TaskPriority, TaskUpdate
from app.repositories.task_repository import TaskRepository
from app.services.priority_advisor import PriorityAdvisor


class TaskService:
    """Orquestra regras de negocio de tarefas."""

    def __init__(
        self,
        repository: TaskRepository,
        priority_advisor: PriorityAdvisor | None = None,
    ) -> None:
        self._repository = repository
        self._priority_advisor = priority_advisor

    def create(self, task: TaskCreate, *, auto_priority: bool = False) -> TaskOut:
        """Cria uma tarefa com prioridade manual ou sugerida."""
        task_to_create = task

        if auto_priority:
            suggested_priority = self._suggest_priority(task)
            if suggested_priority is not None:
                task_to_create = task.model_copy(
                    update={"priority": suggested_priority}
                )

        return self._repository.create(task_to_create)

    def list(self) -> list[TaskOut]:
        """Lista tarefas cadastradas."""
        return self._repository.list()

    def get_by_id(self, task_id: int) -> TaskOut | None:
        """Busca uma tarefa pelo identificador."""
        return self._repository.get_by_id(task_id)

    def update(self, task_id: int, task_update: TaskUpdate) -> TaskOut | None:
        """Atualiza uma tarefa existente."""
        return self._repository.update(task_id, task_update)

    def delete(self, task_id: int) -> bool:
        """Remove uma tarefa existente."""
        return self._repository.delete(task_id)

    def _suggest_priority(self, task: TaskCreate) -> TaskPriority | None:
        if self._priority_advisor is None:
            return None

        return self._priority_advisor.suggest(task)
