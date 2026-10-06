import os

import requests

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


class APIError(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)


def _raise_for_error(resp: requests.Response):
    if resp.status_code >= 400:
        try:
            detail = resp.json().get("detail", resp.text)
        except ValueError:
            detail = resp.text
        raise APIError(resp.status_code, detail)


def _auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def login(username: str, password: str) -> dict:
    resp = requests.post(
        f"{API_BASE_URL}/auth/login",
        data={"username": username, "password": password},
        timeout=10,
    )
    _raise_for_error(resp)
    return resp.json()


def register(username: str, email: str, password: str) -> dict:
    resp = requests.post(
        f"{API_BASE_URL}/auth/register",
        json={"username": username, "email": email, "password": password},
        timeout=10,
    )
    _raise_for_error(resp)
    return resp.json()


def get_tasks(token: str) -> list[dict]:
    resp = requests.get(f"{API_BASE_URL}/tasks", headers=_auth_headers(token), timeout=10)
    _raise_for_error(resp)
    return resp.json()


def create_task(token: str, title: str, description: str | None, completed: bool = False) -> dict:
    resp = requests.post(
        f"{API_BASE_URL}/tasks",
        json={"title": title, "description": description, "completed": completed},
        headers=_auth_headers(token),
        timeout=10,
    )
    _raise_for_error(resp)
    return resp.json()


def update_task(token: str, task_id: int, **fields) -> dict:
    resp = requests.put(
        f"{API_BASE_URL}/tasks/{task_id}",
        json=fields,
        headers=_auth_headers(token),
        timeout=10,
    )
    _raise_for_error(resp)
    return resp.json()


def delete_task(token: str, task_id: int) -> None:
    resp = requests.delete(f"{API_BASE_URL}/tasks/{task_id}", headers=_auth_headers(token), timeout=10)
    _raise_for_error(resp)