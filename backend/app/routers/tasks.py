from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from .. import crud, models, schemas
from ..database import get_db
from ..dependencies import get_current_user

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


# ==========================================================
# CREATE TASK
# ==========================================================

@router.post(
    "/",
    response_model=schemas.TaskResponse,
    status_code=status.HTTP_201_CREATED
)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.create_task(
        db=db,
        task=task,
        user_id=current_user.id
    )


# ==========================================================
# GET ALL TASKS
# ==========================================================

@router.get(
    "/",
    response_model=list[schemas.TaskResponse]
)
def get_all_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.get_tasks(
        db=db,
        user_id=current_user.id,
        skip=skip,
        limit=limit
    )


# ==========================================================
# SEARCH TASKS
# ==========================================================

@router.get(
    "/search",
    response_model=list[schemas.TaskResponse]
)
def search_tasks(
    keyword: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.search_tasks(
        db=db,
        keyword=keyword,
        user_id=current_user.id
    )


# ==========================================================
# FILTER TASKS
# ==========================================================

@router.get(
    "/filter",
    response_model=list[schemas.TaskResponse]
)
def filter_tasks(
    priority: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.filter_tasks_by_priority(
        db=db,
        priority=priority,
        user_id=current_user.id
    )


# ==========================================================
# DASHBOARD STATS
# ==========================================================

@router.get(
    "/dashboard/stats",
    response_model=schemas.DashboardStats
)
def dashboard_stats(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.get_dashboard_stats(
        db=db,
        user_id=current_user.id
    )


# ==========================================================
# GET TASK BY ID
# ==========================================================

@router.get(
    "/{task_id}",
    response_model=schemas.TaskResponse
)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    task = crud.get_task_by_id(
        db=db,
        task_id=task_id,
        user_id=current_user.id
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


# ==========================================================
# UPDATE TASK
# ==========================================================

@router.put(
    "/{task_id}",
    response_model=schemas.TaskResponse
)
def update_task(
    task_id: int,
    updated_task: schemas.TaskUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_task = crud.get_task_by_id(
        db=db,
        task_id=task_id,
        user_id=current_user.id
    )

    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return crud.update_task(
        db=db,
        db_task=db_task,
        task=updated_task
    )


# ==========================================================
# DELETE TASK
# ==========================================================

@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_task = crud.get_task_by_id(
        db=db,
        task_id=task_id,
        user_id=current_user.id
    )

    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    crud.delete_task(
        db=db,
        db_task=db_task
    )

    return None