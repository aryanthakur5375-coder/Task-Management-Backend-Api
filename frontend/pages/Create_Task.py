import streamlit as st
from datetime import date

from utils.api import create_task

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Create Task",
    page_icon="➕",
    layout="centered"
)

# ==========================================================
# AUTH CHECK
# ==========================================================

if "access_token" not in st.session_state or not st.session_state["access_token"]:
    st.warning("Please login first.")
    st.switch_page("pages/Login.py")

# ==========================================================
# PAGE TITLE
# ==========================================================

st.title("➕ Create New Task")

st.markdown("---")

# ==========================================================
# TASK FORM
# ==========================================================

with st.form("create_task_form"):

    title = st.text_input(
        "Task Title",
        placeholder="Enter task title"
    )

    description = st.text_area(
        "Description",
        placeholder="Enter task description"
    )

    priority = st.selectbox(
        "Priority",
        [
            "Low",
            "Medium",
            "High"
        ]
    )

    due_date = st.date_input(
        "Due Date",
        min_value=date.today()
    )

    submitted = st.form_submit_button("Create Task")

# ==========================================================
# CREATE TASK
# ==========================================================

if submitted:

    if not title.strip():

        st.error("Task title is required.")
        st.stop()

    with st.spinner("Creating task..."):

        response = create_task(
            title=title,
            description=description,
            priority=priority,
            due_date=due_date
        )

    if response.status_code == 201:

        st.success("Task created successfully!")

        st.balloons()

        st.markdown("---")

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "Create Another Task",
                use_container_width=True
            ):
                st.rerun()

        with col2:

            if st.button(
                "Go to Dashboard",
                use_container_width=True
            ):
                st.switch_page("pages/Dashboard.py")

    else:

        try:
            error = response.json()["detail"]
        except Exception:
            error = "Unable to create task."

        st.error(error)