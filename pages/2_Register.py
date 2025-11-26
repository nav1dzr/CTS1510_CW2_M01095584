import streamlit as st
from app.data.users import register_user

st.title("Register")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Create account"):
    if username and password:
        register_user(username, password)
        st.success("Account created! You can now log in.")
    else:
        st.error("Please enter both username and password.")
