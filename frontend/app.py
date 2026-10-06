import streamlit as st

import api

st.set_page_config(page_title="Task Manager", page_icon="✅")

if "token" not in st.session_state:
    st.session_state.token = None
if "username" not in st.session_state:
    st.session_state.username = None


def handle_error(e: api.APIError):
    msgs = {
        401: "Session expired. Please log in again.",
        403: "You are not authorized to do this.",
        404: "Task not found.",
        422: "Invalid input.",
        500: "Server error. Try again later.",
    }
    st.error(msgs.get(e.status_code, e.detail))
    if e.status_code == 401:
        st.session_state.token = None
        st.session_state.username = None


def login_view():
    st.title("✅ Task Manager - Login")
    tab_login, tab_register = st.tabs(["Login", "Register"])

    with tab_login:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.form_submit_button("Login"):
                try:
                    data = api.login(username, password)
                    st.session_state.token = data["access_token"]
                    st.session_state.username = username
                    st.rerun()
                except api.APIError as e:
                    handle_error(e)

    with tab_register:
        with st.form("register_form"):
            r_username = st.text_input("Username", key="r_username")
            r_email = st.text_input("Email", key="r_email")
            r_password = st.text_input("Password", type="password", key="r_password")
            if st.form_submit_button("Register"):
                try:
                    api.register(r_username, r_email, r_password)
                    st.success("Account created. Please log in.")
                except api.APIError as e:
                    handle_error(e)


def dashboard_view():
    st.title("✅ My Tasks")

    with st.sidebar:
        st.write(f"Logged in as **{st.session_state.username}**")
        if st.button("Refresh"):
            st.rerun()
        if st.button("Logout"):
            st.session_state.token = None
            st.session_state.username = None
            st.rerun()

    with st.form("create_task_form", clear_on_submit=True):
        st.subheader("Add Task")
        title = st.text_input("Title")
        description = st.text_area("Description")
        if st.form_submit_button("Create"):
            if not title.strip():
                st.error("Title is required.")
            else:
                try:
                    api.create_task(st.session_state.token, title.strip(), description.strip() or None)
                    st.success("Task created.")
                    st.rerun()
                except api.APIError as e:
                    handle_error(e)

    try:
        tasks = api.get_tasks(st.session_state.token)
    except api.APIError as e:
        handle_error(e)
        return

    if not tasks:
        st.info("No tasks yet.")
        return

    for task in tasks:
        with st.expander(f"{'✅' if task['completed'] else '⬜'} {task['title']}"):
            st.write(task.get("description") or "_No description_")
            st.caption(f"Created: {task['created_at']} | Updated: {task['updated_at']}")

            completed = st.checkbox("Completed", value=task["completed"], key=f"done_{task['id']}")
            if completed != task["completed"]:
                try:
                    api.update_task(st.session_state.token, task["id"], completed=completed)
                    st.rerun()
                except api.APIError as e:
                    handle_error(e)

            with st.form(f"edit_form_{task['id']}"):
                new_title = st.text_input("Title", value=task["title"], key=f"title_{task['id']}")
                new_desc = st.text_area(
                    "Description", value=task.get("description") or "", key=f"desc_{task['id']}"
                )
                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("Update"):
                        try:
                            api.update_task(
                                st.session_state.token,
                                task["id"],
                                title=new_title,
                                description=new_desc or None,
                            )
                            st.success("Task updated.")
                            st.rerun()
                        except api.APIError as e:
                            handle_error(e)
                with col2:
                    if st.form_submit_button("Delete"):
                        try:
                            api.delete_task(st.session_state.token, task["id"])
                            st.success("Task deleted.")
                            st.rerun()
                        except api.APIError as e:
                            handle_error(e)


if st.session_state.token:
    dashboard_view()
else:
    login_view()