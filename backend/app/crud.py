from sqlalchemy.orm import Session
from sqlalchemy import func

from . import auth, models, schemas


# ==========================================================
# USER CRUD
# ==========================================================

def get_user_by_email(db: Session, email: str):
    return (
        db.query(models.User)
        .filter(models.User.email == email)
        .first()
    )


def get_user_by_username(db: Session, username: str):
    return (
        db.query(models.User)
        .filter(models.User.username == username)
        .first()
    )


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.hash_password(user.password)

    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


# ==========================================================
# TASK CRUD
# ==========================================================

def create_task(
    db: Session,
    task: schemas.TaskCreate,
    user_id: int
):
    db_task = models.Task(
        title=task.title,
        description=task.description,
        priority=task.priority,
        due_date=task.due_date,
        user_id=user_id
    )

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task


def get_tasks(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 10
):
    return (
        db.query(models.Task)
        .filter(models.Task.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_task_by_id(
    db: Session,
    task_id: int,
    user_id: int
):
    return (
        db.query(models.Task)
        .filter(
            models.Task.id == task_id,
            models.Task.user_id == user_id
        )
        .first()
    )


def update_task(
    db: Session,
    db_task: models.Task,
    task: schemas.TaskUpdate
):
    update_data = task.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_task, key, value)

    db.commit()
    db.refresh(db_task)

    return db_task


def delete_task(
    db: Session,
    db_task: models.Task
):
    db.delete(db_task)
    db.commit()


# ==========================================================
# SEARCH
# ==========================================================

def search_tasks(
    db: Session,
    keyword: str,
    user_id: int
):
    return (
        db.query(models.Task)
        .filter(
            models.Task.user_id == user_id,
            models.Task.title.ilike(f"%{keyword}%")
        )
        .all()
    )


# ==========================================================
# FILTER
# ==========================================================

def filter_tasks_by_priority(
    db: Session,
    priority: str,
    user_id: int
):
    return (
        db.query(models.Task)
        .filter(
            models.Task.user_id == user_id,
            models.Task.priority == priority
        )
        .all()
    )


# ==========================================================
# DASHBOARD
# ==========================================================

def get_dashboard_stats(
    db: Session,
    user_id: int
):
    total_tasks = (
        db.query(func.count(models.Task.id))
        .filter(models.Task.user_id == user_id)
        .scalar()
    )

    completed_tasks = (
        db.query(func.count(models.Task.id))
        .filter(
            models.Task.user_id == user_id,
            models.Task.completed == True
        )
        .scalar()
    )

    pending_tasks = total_tasks - completed_tasks

    high_priority_tasks = (
        db.query(func.count(models.Task.id))
        .filter(
            models.Task.user_id == user_id,
            models.Task.priority == "High"
        )
        .scalar()
    )

    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "high_priority_tasks": high_priority_tasks
    }