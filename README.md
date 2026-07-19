# 🚀 Task Management Backend API

A modern **Task Management Backend API** built with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, and **JWT Authentication**. The project provides secure user authentication and complete task management features, following RESTful API principles.

---

## 📌 Features

### 🔐 Authentication
- User Registration
- User Login
- JWT Authentication
- Password Hashing using bcrypt
- Protected Routes

### 📋 Task Management
- Create Task
- View All Tasks
- View Task by ID
- Update Task
- Delete Task
- User-specific Tasks

### 🔍 Additional Features
- Search Tasks
- Filter Tasks by Priority
- Dashboard Statistics
- Pagination
- RESTful API Design

---

## 🛠 Tech Stack

| Technology | Purpose |
|------------|---------|
| FastAPI | Backend Framework |
| PostgreSQL | Database |
| SQLAlchemy | ORM |
| Pydantic | Data Validation |
| JWT | Authentication |
| Passlib (bcrypt) | Password Hashing |
| Uvicorn | ASGI Server |
| Streamlit | Frontend |

---

## 📂 Project Structure

```
Task-Management-Backend-Api/
│
├── backend/
│   ├── app/
│   │   ├── routers/
│   │   │   ├── auth.py
│   │   │   └── tasks.py
│   │   ├── auth.py
│   │   ├── config.py
│   │   ├── crud.py
│   │   ├── database.py
│   │   ├── dependencies.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── main.py
│   │
│   ├── run.py
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── app.py
│   ├── pages/
│   └── utils/
│
├── README.md
└── .gitignore
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/aryanthakur5375-coder/Task-Management-Backend-Api.git
```

```bash
cd Task-Management-Backend-Api
```

---

### Create Virtual Environment

Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### Install Dependencies

```bash
pip install -r backend/requirements.txt
```

---

### Configure Environment Variables

Create a `.env` file inside the **backend** folder.

Example:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/task_management

SECRET_KEY=your_secret_key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

### Run Backend

```bash
cd backend
python run.py
```

or

```bash
uvicorn app.main:app --reload
```

---

### Run Frontend

```bash
cd frontend
streamlit run app.py
```

---

## 📖 API Documentation

FastAPI automatically generates API documentation.

Swagger UI

```
http://127.0.0.1:8000/docs
```

ReDoc

```
http://127.0.0.1:8000/redoc
```

---

## 📌 API Endpoints

### Authentication

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/auth/register` | Register User |
| POST | `/auth/login` | Login User |
| GET | `/auth/me` | Current Logged-in User |

---

### Tasks

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/tasks` | Create Task |
| GET | `/tasks` | Get All Tasks |
| GET | `/tasks/{id}` | Get Task by ID |
| PUT | `/tasks/{id}` | Update Task |
| DELETE | `/tasks/{id}` | Delete Task |
| GET | `/tasks/search` | Search Tasks |
| GET | `/tasks/filter` | Filter by Priority |
| GET | `/tasks/dashboard/stats` | Dashboard Statistics |

---

## 🔒 Security

- Passwords are securely hashed using **bcrypt**.
- JWT Authentication protects private routes.
- User-specific authorization ensures users can only access their own tasks.
- Environment variables are used for sensitive configuration.

---

## 🚀 Future Improvements

- Refresh Tokens
- Role-Based Access Control (RBAC)
- Email Verification
- Password Reset
- Alembic Database Migrations
- Docker Support
- Unit & Integration Tests
- CI/CD Pipeline
- Task Categories & Labels
- File Attachments

---

## 👨‍💻 Author

**Aryan Thakur**

GitHub: https://github.com/aryanthakur5375-coder

---

## ⭐ If you like this project

If you found this project useful, consider giving it a **⭐ Star** on GitHub.
