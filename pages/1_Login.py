import streamlit as st
from app.data.users import get_user_by_username, verify_password

st.title("🔑 Login")

# If already logged in
if "user" in st.session_state:
    st.success(f"You are already logged in as **{st.session_state['user']}**")
    st.page_link("pages/3_Dashboard.py", label="Go to Dashboard", icon="📊")
    st.stop()

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    user = get_user_by_username(username)

    if not user:
        st.error("User does not exist.")
        st.stop()

    _, db_username, password_hash = user

    if verify_password(password, password_hash):
        # SAVE LOGIN TO SESSION STATE
        st.session_state["user"] = db_username

        st.success(f"Welcome, {db_username}!")

        # REDIRECT TO DASHBOARD IMMEDIATELY
        st.switch_page("pages/3_Dashboard.py")

    else:
        st.error("Incorrect password.")
