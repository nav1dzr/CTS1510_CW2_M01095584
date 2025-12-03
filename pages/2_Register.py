import streamlit as st
from app.data.users import register_user, get_user_by_username
from session_manager import is_logged_in

st.title("📝 Register")

st.set_page_config(
    page_title="Your App",
    page_icon="🛡️",
    initial_sidebar_state="collapsed",
    layout="wide"
)

# --------------------------
# Already logged in
# --------------------------
if is_logged_in():
    st.success("You are already logged in!")
    st.stop()

# --------------------------
# Registration Form (supports ENTER)
# --------------------------
with st.form("register_form"):
    username = st.text_input("Choose a username")
    password = st.text_input("Choose a password", type="password")
    confirm_password = st.text_input("Confirm your password", type="password")

    submit = st.form_submit_button("Create Account")   # Enter triggers this

if submit:
    # 1. Required fields
    if not username or not password or not confirm_password:
        st.error("Please fill all fields.")
        st.stop()

    # 2. Password match
    if password != confirm_password:
        st.error("Passwords do not match. Please try again.")
        st.stop()

    # 3. Username unique
    existing_user = get_user_by_username(username)
    if existing_user:
        st.error("⚠️ Username already exists. Please choose another one.")
        st.stop()

    # 4. Create user
    register_user(username, password)
    st.success("✅ Account created successfully! You can now log in.")
