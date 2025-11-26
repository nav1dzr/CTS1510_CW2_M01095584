import streamlit as st
from app.data.users import register_user, get_user_by_username

st.title("📝 Register")

username = st.text_input("Choose a username")
password = st.text_input("Choose a password", type="password")

if st.button("Create Account"):
    if not username or not password:
        st.error("Please enter both username and password.")
    else:
        # Check if user exists
        if get_user_by_username(username):
            st.error("This username already exists.")
        else:
            register_user(username, password)
            st.success("Account created! You can now log in.")
            st.page_link("pages/1_Login.py", label="Proceed to Login")
