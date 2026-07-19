import streamlit as st

from utils.api import (
    delete_task,
    filter_tasks,
    get_tasks,
    search_tasks,
    update_task
)

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="View Tasks",
    page_icon="📋",
    layout="wide"
)

# ==========================================================
# AUTH CHECK
# ==========================================================

if "access_token" not in st.session_state or not st.session_state["access_token"]:
    st.warning("Please login first.")
    st.switch_page("pages/Login.py")

st.title("📋 Task Manager")

st.markdown("---")

# ==========================================================
# SEARCH & FILTER
# ==========================================================

col1, col2, col3 = st.columns([3, 2, 1])

with col1:
    keyword = st.text_input(
        "Search Tasks",
        placeholder="Enter title..."
    )

with col2:
    priority = st.selectbox(
        "Priority",
        ["All", "Low", "Medium", "High"]
    )

with col3:
    refresh = st.button("🔄 Refresh")

# ==========================================================
# FETCH TASKS
# ==========================================================

if keyword:

    response = search_tasks(keyword)

elif priority != "All":

    response = filter_tasks(priority)

else:

    response = get_tasks(limit=100)

if response.status_code != 200:
    st.error("Unable to load tasks.")
    st.stop()

tasks = response.json()

# ==========================================================
# EMPTY
# ==========================================================

if len(tasks) == 0:
    st.info("No tasks found.")
    st.stop()

# ==========================================================
# TASKS
# ==========================================================

for task in tasks:

    with st.expander(
        f"{task['title']} ({task['priority']})",
        expanded=False
    ):

        st.write("### Description")
        st.write(task["description"] or "No description")

        st.write("### Due Date")
        st.write(task["due_date"])

        st.write("### Status")

        completed = st.checkbox(
            "Completed",
            value=task["completed"],
            key=f"completed_{task['id']}"
        )

        st.markdown("---")

        st.subheader("Edit Task")

        new_title = st.text_input(
            "Title",
            value=task["title"],
            key=f"title_{task['id']}"
        )

        new_description = st.text_area(
            "Description",
            value=task["description"] or "",
            key=f"desc_{task['id']}"
        )

        new_priority = st.selectbox(
            "Priority",
            ["Low", "Medium", "High"],
            index=["Low", "Medium", "High"].index(task["priority"]),
            key=f"priority_{task['id']}"
        )

        col_update, col_delete = st.columns(2)

        with col_update:

            if st.button(
                "💾 Update",
                key=f"update_{task['id']}",
                use_container_width=True
            ):

                response = update_task(
                    task_id=task["id"],
                    title=new_title,
                    description=new_description,
                    priority=new_priority,
                    completed=completed,
                    due_date=task["due_date"]
                )

                if response.status_code == 200:
                    st.success("Task Updated")
                    st.rerun()
                else:
                    st.error("Update failed.")

        with col_delete:

            if st.button(
                "🗑 Delete",
                key=f"delete_{task['id']}",
                use_container_width=True
            ):

                response = delete_task(task["id"])

                if response.status_code == 204:
                    st.success("Task Deleted")
                    st.rerun()
                else:
                    st.error("Delete failed.")