from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models import Task
from app.schemas.task import TaskCreate, TaskUpdate


def get_tasks(db: Session, user_id: int) -> list[Task]:
    return list(db.scalars(select(Task).where(Task.user_id == user_id)))


def get_task(db: Session, task_id: int, user_id: int) -> Task | None:
    return db.scalar(select(Task).where(Task.id == task_id, Task.user_id == user_id))


def create_task(db: Session, task_in: TaskCreate, user_id: int) -> Task:
    task = Task(**task_in.model_dump(), user_id=user_id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def update_task(db: Session, task: Task, task_in: TaskUpdate) -> Task:
    for field, value in task_in.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task: Task) -> None:
    db.delete(task)
    db.commit()
