import streamlit as st
from app.data.users import register_user
from session_manager import is_logged_in

st.title("📝 Register")

st.set_page_config(
    page_title="Your App",
    page_icon="🛡️",
    initial_sidebar_state="collapsed",
    layout="wide"
)

if is_logged_in():
    st.success("You are already logged in!")
    st.stop()

username = st.text_input("Choose a username")
password = st.text_input("Choose a password", type="password")

if st.button("Create Account"):
    if username and password:
        register_user(username, password)
        st.success("Account created! You can now log in.")
    else:
        st.error("Please fill all fields.")
