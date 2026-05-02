from fastapi import APIRouter, HTTPException, Query, Response, status

from app.models.task import TaskCreate, TaskOut, TaskUpdate
from app.repositories.task_repository import TaskRepository
from app.services.priority_advisor import PriorityAdvisor
from app.services.task_service import TaskService


router = APIRouter(prefix="/tasks", tags=["tasks"])

_task_service = TaskService(
    repository=TaskRepository(),
    priority_advisor=PriorityAdvisor(),
)


@router.post("", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(
    task: TaskCreate,
    auto_priority: bool = Query(default=False),
) -> TaskOut:
    return _task_service.create(task, auto_priority=auto_priority)


@router.get("", response_model=list[TaskOut])
def list_tasks() -> list[TaskOut]:
    return _task_service.list()


@router.get("/{task_id}", response_model=TaskOut)
def get_task(task_id: int) -> TaskOut:
    task = _task_service.get_by_id(task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return task


@router.put("/{task_id}", response_model=TaskOut)
def update_task(task_id: int, task_update: TaskUpdate) -> TaskOut:
    task = _task_service.update(task_id, task_update)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int) -> Response:
    deleted = _task_service.delete(task_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
