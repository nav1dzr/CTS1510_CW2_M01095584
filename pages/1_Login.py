import streamlit as st
from app.data.users import get_user_by_username, verify_password
from session_manager import login_user, is_logged_in

# So AI assistant knows current page if you use it later
st.session_state["current_page"] = "login"

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
# LOGIN FORM (supports ENTER)
# --------------------------
with st.form("login_form"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submitted = st.form_submit_button("Login")   # ENTER triggers this

if submitted:
    user = get_user_by_username(username)

    if not user:
        st.error("❌ User does not exist.")
    else:
        user_id, db_username, password_hash = user

        if verify_password(password, password_hash):
            login_user(db_username)
            st.success(f"Welcome back, **{db_username}**! Redirecting...")
            st.switch_page("pages/3_Dashboard.py")
        else:
            st.error("❌ Incorrect password.")

# Optional: link to register page
st.write("---")
st.page_link("pages/2_Register.py", label="📝 Create a new account")
