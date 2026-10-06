# Task Management API

A simple, production-style REST API for managing personal tasks, built with FastAPI and JWT authentication.

## Tech Stack

- **Python** 3.11+
- **FastAPI** + **Uvicorn**
- **PostgreSQL** + **SQLAlchemy 2.x**
- **Alembic** (migrations)
- **Pydantic v2** (validation)
- **python-jose** (JWT) + **passlib/bcrypt** (password hashing)

## Architecture

```
app/
├── main.py           # FastAPI app + router registration
├── core/
│   ├── config.py      # Settings (env vars)
│   └── security.py    # Password hashing, JWT create/decode
├── database/
│   ├── database.py     # Engine, session, Base
│   └── models.py       # SQLAlchemy models (User, Task)
├── schemas/           # Pydantic request/response models
├── crud/               # DB query functions
├── routers/            # auth, users, tasks endpoints
└── dependencies.py     # get_current_user (JWT auth)
```

`User` has a one-to-many relationship with `Task` (`user_id` foreign key). Each task belongs to exactly one user.

## Setup

### 1. Clone & install

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. PostgreSQL

Create a database:

```bash
psql -U postgres -c "CREATE DATABASE task_manager;"
```

### 3. Environment variables

Copy `.env` and edit values:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/task_manager
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 4. Run migrations

```bash
alembic revision --autogenerate -m "initial migration"
alembic upgrade head
```

### 5. Run the API

```bash
uvicorn app.main:app --reload
```

Docs available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Main Endpoints

| Method | Endpoint          | Auth | Description                  |
|--------|-------------------|------|-------------------------------|
| POST   | `/auth/register`  | No   | Create a new user             |
| POST   | `/auth/login`     | No   | Get JWT access token          |
| GET    | `/users/me`       | Yes  | Get current user profile      |
| POST   | `/tasks`          | Yes  | Create a task                 |
| GET    | `/tasks`          | Yes  | List your tasks               |
| GET    | `/tasks/{id}`     | Yes  | Get a single task             |
| PUT    | `/tasks/{id}`     | Yes  | Update a task                 |
| DELETE | `/tasks/{id}`     | Yes  | Delete a task                 |

## Authentication

`/auth/login` uses the standard OAuth2 password form (`username` + `password` fields), which lets you use the **Authorize** button in `/docs` directly.

1. Register: `POST /auth/register` with `username`, `email`, `password`.
2. Login: `POST /auth/login` (form-encoded) → returns `{"access_token": "...", "token_type": "bearer"}`.
3. Use the token on protected routes:

```
Authorization: Bearer <access_token>
```

Tasks are always scoped to the authenticated user — you cannot view, edit, or delete another user's tasks (returns `404`).
