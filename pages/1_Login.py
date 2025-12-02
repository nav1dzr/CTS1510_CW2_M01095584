import streamlit as st
from app.data.users import get_user_by_username, verify_password
from session_manager import login_user, is_logged_in

# --------------------------
# PAGE CONFIG
# --------------------------
st.set_page_config(page_title="Login", page_icon="🔐")

st.title("🔐 Login")

# If already logged in → auto redirect to dashboard
if is_logged_in():
    st.success(f"Already logged in as **{st.session_state['user']}**")
    st.info("Redirecting to dashboard...")
    st.switch_page("pages/3_Dashboard.py")
    st.stop()

# --------------------------
# LOGIN FORM
# --------------------------
username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    user = get_user_by_username(username)

    if not user:
        st.error("❌ User does not exist.")
        st.stop()

    user_id, db_username, password_hash = user

    if verify_password(password, password_hash):
        login_user(db_username)
        st.success(f"Welcome back, **{db_username}**! Redirecting...")

        # Auto redirect
        st.rerun()

    else:
        st.error("❌ Incorrect password.")

# --------------------------
# REGISTER LINK
# --------------------------
st.write("---")
st.page_link("pages/2_Register.py", label="📝 Create a new account")
