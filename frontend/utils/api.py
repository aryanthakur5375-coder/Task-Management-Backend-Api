import requests
import streamlit as st

# Backend API URL
BASE_URL = "http://127.0.0.1:8000"


# ==========================================================
# Helper Functions
# ==========================================================

def get_headers():
    """
    Returns authorization headers if user is logged in.
    """

    token = st.session_state.get("access_token")

    if token:
        return {
            "Authorization": f"Bearer {token}"
        }

    return {}


# ==========================================================
# Authentication APIs
# ==========================================================

def register(username: str, email: str, password: str):
    response = requests.post(
        f"{BASE_URL}/auth/register",
        json={
            "username": username,
            "email": email,
            "password": password
        }
    )

    return response


def login(email: str, password: str):
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={
            "email": email,
            "password": password
        }
    )

    return response


def get_current_user():
    response = requests.get(
        f"{BASE_URL}/auth/me",
        headers=get_headers()
    )

    return response


# ==========================================================
# Task APIs
# ==========================================================

def get_tasks(skip=0, limit=20):
    response = requests.get(
        f"{BASE_URL}/tasks",
        params={
            "skip": skip,
            "limit": limit
        },
        headers=get_headers()
    )

    return response


def get_task(task_id):
    response = requests.get(
        f"{BASE_URL}/tasks/{task_id}",
        headers=get_headers()
    )

    return response


def create_task(
    title,
    description,
    priority,
    due_date
):
    response = requests.post(
        f"{BASE_URL}/tasks",
        json={
            "title": title,
            "description": description,
            "priority": priority,
            "due_date": str(due_date)
        },
        headers=get_headers()
    )

    return response


def update_task(
    task_id,
    title,
    description,
    priority,
    completed,
    due_date
):
    response = requests.put(
        f"{BASE_URL}/tasks/{task_id}",
        json={
            "title": title,
            "description": description,
            "priority": priority,
            "completed": completed,
            "due_date": str(due_date)
        },
        headers=get_headers()
    )

    return response


def delete_task(task_id):
    response = requests.delete(
        f"{BASE_URL}/tasks/{task_id}",
        headers=get_headers()
    )

    return response


# ==========================================================
# Search
# ==========================================================

def search_tasks(keyword):
    response = requests.get(
        f"{BASE_URL}/tasks/search",
        params={
            "keyword": keyword
        },
        headers=get_headers()
    )

    return response


# ==========================================================
# Filter
# ==========================================================

def filter_tasks(priority):
    response = requests.get(
        f"{BASE_URL}/tasks/filter",
        params={
            "priority": priority
        },
        headers=get_headers()
    )

    return response


# ==========================================================
# Dashboard
# ==========================================================

def dashboard_stats():
    response = requests.get(
        f"{BASE_URL}/tasks/dashboard/stats",
        headers=get_headers()
    )

    return response