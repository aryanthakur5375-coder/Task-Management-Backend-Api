import streamlit as st

from utils.api import dashboard_stats, get_tasks

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)

# ==========================================================
# AUTH CHECK
# ==========================================================

if "access_token" not in st.session_state or not st.session_state["access_token"]:
    st.warning("Please login first.")
    st.switch_page("pages/Login.py")

# ==========================================================
# TITLE
# ==========================================================

st.title("📊 Dashboard")

st.markdown("---")

# ==========================================================
# LOAD DASHBOARD STATS
# ==========================================================

stats_response = dashboard_stats()

if stats_response.status_code != 200:
    st.error("Unable to load dashboard.")
    st.stop()

stats = stats_response.json()

# ==========================================================
# METRICS
# ==========================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "📋 Total Tasks",
        stats["total_tasks"]
    )

with col2:
    st.metric(
        "✅ Completed",
        stats["completed_tasks"]
    )

with col3:
    st.metric(
        "⏳ Pending",
        stats["pending_tasks"]
    )

with col4:
    st.metric(
        "🔥 High Priority",
        stats["high_priority_tasks"]
    )

st.markdown("---")

# ==========================================================
# PROGRESS BAR
# ==========================================================

total = stats["total_tasks"]
completed = stats["completed_tasks"]

if total > 0:
    progress = completed / total
else:
    progress = 0

st.subheader("Task Completion Progress")

st.progress(progress)

st.write(f"{completed} of {total} tasks completed.")

st.markdown("---")

# ==========================================================
# RECENT TASKS
# ==========================================================

st.subheader("Recent Tasks")

task_response = get_tasks(limit=5)

if task_response.status_code == 200:

    tasks = task_response.json()

    if len(tasks) == 0:

        st.info("No tasks available.")

    else:

        for task in tasks:

            with st.container():

                left, right = st.columns([4, 1])

                with left:

                    st.write(f"### {task['title']}")

                    st.write(task["description"] or "No description")

                    st.caption(
                        f"Priority: {task['priority']} | Due: {task['due_date']}"
                    )

                with right:

                    if task["completed"]:
                        st.success("Completed")
                    else:
                        st.warning("Pending")

                st.divider()

else:

    st.error("Unable to fetch tasks.")

# ==========================================================
# QUICK ACTIONS
# ==========================================================

st.markdown("---")

st.subheader("Quick Actions")

c1, c2 = st.columns(2)

with c1:

    if st.button(
        "➕ Create Task",
        use_container_width=True
    ):
        st.switch_page("pages/Create_Task.py")

with c2:

    if st.button(
        "📋 View All Tasks",
        use_container_width=True
    ):
        st.switch_page("pages/View_Tasks.py")