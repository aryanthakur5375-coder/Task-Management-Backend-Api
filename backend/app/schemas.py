from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ==========================================================
# User Schemas
# ==========================================================

class UserCreate(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=50
    )

    email: EmailStr

    password: str = Field(
        min_length=6,
        max_length=100
    )


class UserLogin(BaseModel):
    email: EmailStr

    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# ==========================================================
# JWT Schemas
# ==========================================================

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int | None = None


# ==========================================================
# Task Schemas
# ==========================================================

class TaskBase(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=150
    )

    description: str | None = None

    priority: str = Field(
        default="Medium"
    )

    due_date: date | None = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: str | None = None

    description: str | None = None

    priority: str | None = None

    completed: bool | None = None

    due_date: date | None = None


class TaskResponse(TaskBase):
    id: int

    completed: bool

    created_at: datetime

    updated_at: datetime

    user_id: int

    model_config = ConfigDict(
        from_attributes=True
    )


# ==========================================================
# Dashboard Schemas
# ==========================================================

class DashboardStats(BaseModel):
    total_tasks: int

    completed_tasks: int

    pending_tasks: int

    high_priority_tasks: int