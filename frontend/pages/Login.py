import streamlit as st

from utils.api import login, get_current_user

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Login",
    page_icon="🔐"
)

st.title("🔐 Login")

st.markdown("---")

# ==========================================================
# ALREADY LOGGED IN
# ==========================================================

if st.session_state.get("access_token"):

    st.success("You are already logged in.")

    if st.button("Go to Dashboard"):
        st.switch_page("pages/Dashboard.py")

    st.stop()

# ==========================================================
# LOGIN FORM
# ==========================================================

with st.form("login_form"):

    email = st.text_input(
        "Email"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    submitted = st.form_submit_button("Login")

# ==========================================================
# LOGIN LOGIC
# ==========================================================

if submitted:

    if not email or not password:
        st.warning("Please fill all fields.")
        st.stop()

    with st.spinner("Logging in..."):

        response = login(email, password)

    if response.status_code == 200:

        token = response.json()["access_token"]

        st.session_state["access_token"] = token

        # Fetch current user information
        user_response = get_current_user()

        if user_response.status_code == 200:

            user = user_response.json()

            st.session_state["username"] = user["username"]

            st.session_state["email"] = user["email"]

        st.success("Login successful!")

        st.balloons()

        st.switch_page("pages/Dashboard.py")

    else:

        try:
            error = response.json()["detail"]
        except Exception:
            error = "Login failed."

        st.error(error)

st.markdown("---")

st.info(
    "Don't have an account? Go to the Register page."
)