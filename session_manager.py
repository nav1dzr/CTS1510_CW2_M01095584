import streamlit as st

def login_user(username):
    """Store logged-in user in session."""
    st.session_state["user"] = username

def logout_user():
    """Clear user session."""
    st.session_state.clear()

def is_logged_in():
    """Check if user logged in."""
    return "user" in st.session_state

def require_login():
    """Redirect users who are NOT logged in."""
    if not is_logged_in():
        st.warning("You must log in first.")
        st.switch_page("Home.py")
