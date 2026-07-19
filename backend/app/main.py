from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .routers import auth, tasks

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Management API",
    description="A Task Management Backend built using FastAPI, PostgreSQL, SQLAlchemy, JWT Authentication, and Streamlit.",
    version="1.0.0",
)

# Allow frontend to access the backend
origins = [
    "http://localhost:8501",  # Streamlit
    "http://127.0.0.1:8501",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routers
app.include_router(auth.router)
app.include_router(tasks.router)


@app.get("/", tags=["Home"])
def home():
    return {
        "message": "Welcome to Task Management API 🚀",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy"
    }