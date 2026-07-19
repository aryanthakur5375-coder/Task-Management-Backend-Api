from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)

from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    username = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    email = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    hashed_password = Column(
        String(255),
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    tasks = relationship(
        "Task",
        back_populates="owner",
        cascade="all, delete-orphan",
    )


class Task(Base):
    __tablename__ = "tasks"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    title = Column(
        String(150),
        nullable=False,
    )

    description = Column(
        Text,
        nullable=True,
    )

    priority = Column(
        String(20),
        default="Medium",
        nullable=False,
    )

    completed = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    due_date = Column(
        Date,
        nullable=True,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    owner = relationship(
        "User",
        back_populates="tasks",
    )