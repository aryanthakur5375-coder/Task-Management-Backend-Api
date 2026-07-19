import streamlit as st

from utils.api import register

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Register",
    page_icon="📝"
)

st.title("📝 Create Account")

st.markdown("---")

# ==========================================================
# REGISTER FORM
# ==========================================================

with st.form("register_form"):

    username = st.text_input(
        "Username"
    )

    email = st.text_input(
        "Email"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    confirm_password = st.text_input(
        "Confirm Password",
        type="password"
    )

    submitted = st.form_submit_button("Register")

# ==========================================================
# REGISTER LOGIC
# ==========================================================

if submitted:

    # Validation
    if not username or not email or not password or not confirm_password:
        st.warning("Please fill all the fields.")
        st.stop()

    if password != confirm_password:
        st.error("Passwords do not match.")
        st.stop()

    if len(password) < 6:
        st.error("Password must be at least 6 characters long.")
        st.stop()

    with st.spinner("Creating account..."):

        response = register(
            username=username,
            email=email,
            password=password
        )

    if response.status_code == 201:

        st.success("Account created successfully!")

        st.balloons()

        st.info("Go to the Login page to sign in.")

        if st.button("Go to Login"):
            st.switch_page("pages/Login.py")

    else:

        try:
            error = response.json()["detail"]
        except Exception:
            error = "Registration failed."

        st.error(error)

st.markdown("---")

st.info("Already have an account? Open the Login page.")