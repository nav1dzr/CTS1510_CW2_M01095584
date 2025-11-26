import streamlit as st
from app.data.users import get_user_by_username, verify_password
from session_manager import login_user, is_logged_in

st.title("🔑 Login")

# If already logged in
if is_logged_in():
    st.success("You are already logged in.")
    st.switch_page("pages/3_Dashboard.py")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    user = get_user_by_username(username)

    if user:
        user_id, db_username, password_hash = user

        if verify_password(password, password_hash):
            login_user(db_username)
            st.success("Login successful! Redirecting...")
            st.switch_page("pages/3_Dashboard.py")
        else:
            st.error("Incorrect password.")
    else:
        st.error("User does not exist.")
