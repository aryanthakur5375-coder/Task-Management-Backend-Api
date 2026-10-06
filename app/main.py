from fastapi import FastAPI

from app.routers import auth, tasks, users

app = FastAPI(
    title="Task Management API",
    description="A simple REST API for managing personal tasks with JWT authentication.",
    version="1.0.0",
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tasks.router)


@app.get("/", tags=["health"])
def root():
    return {"status": "ok"}
