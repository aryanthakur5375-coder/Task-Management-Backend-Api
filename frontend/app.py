import streamlit as st

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Task Management System",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# SESSION STATE
# ==========================================================

if "access_token" not in st.session_state:
    st.session_state["access_token"] = None

if "username" not in st.session_state:
    st.session_state["username"] = None

# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.title("📝 Task Manager")

    st.markdown("---")

    if st.session_state["access_token"]:

        st.success(f"Logged in as **{st.session_state['username']}**")

        st.markdown("---")

        st.info(
            """
### Navigation

Use the pages on the left sidebar:

- Dashboard
- Create Task
- View Tasks
            """
        )

        st.markdown("---")

        if st.button("🚪 Logout", use_container_width=True):

            st.session_state["access_token"] = None
            st.session_state["username"] = None

            st.success("Logged out successfully.")

            st.rerun()

    else:

        st.warning("You are not logged in.")

        st.info(
            """
Please login or register first.

Use the pages:

- Login
- Register
            """
        )

# ==========================================================
# HOME PAGE
# ==========================================================

st.title("📝 Task Management System")

st.markdown("---")

if st.session_state["access_token"]:

    st.success("Welcome back!")

    st.markdown(
        """
This application allows you to:

- ✅ Create Tasks
- ✏️ Update Tasks
- 🗑 Delete Tasks
- 🔍 Search Tasks
- 🎯 Filter by Priority
- 📊 Dashboard Statistics

Use the sidebar to navigate through the application.
"""
    )

else:

    st.markdown(
        """
## Welcome!

This Task Management System is built using:

- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT Authentication
- Streamlit

### To get started:

1. Register a new account
2. Login
3. Start managing your tasks
"""
    )

st.markdown("---")

st.caption("Built with ❤️ using FastAPI + Streamlit")