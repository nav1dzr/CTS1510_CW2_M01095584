import streamlit as st
from session_manager import is_logged_in, logout_user

st.set_page_config(
    page_title="Your App",
    page_icon="🛡️",
    initial_sidebar_state="collapsed",
    layout="wide"
)

st.title("🛡️ Cyber Intelligence Platform")

st.write("""
Welcome to the Multi-Domain Intelligence Platform.

This platform provides:
- 🔐 Secure Login & Registration  
- 📊 Cybersecurity Analytics  
- 🗂️ Dataset Insights  
- 🛠️ IT Ticket Monitoring  
""")

st.write("---")

if is_logged_in():
    st.success(f"Logged in as **{st.session_state['user']}**")

    st.page_link("pages/3_Dashboard.py", label="📊 Go to Dashboard")

    if st.button("Logout"):
        logout_user()
        st.rerun()

else:
    st.info("Please login or register to access the dashboard.")

    col1, col2 = st.columns(2)

    with col1:
        st.page_link("pages/1_Login.py", label="🔑 Login")

    with col2:
        st.page_link("pages/2_Register.py", label="📝 Register")


# HIDE STREAMLIT'S DEFAULT NAVIGATION
hide_nav = """
<style>
section[data-testid="stSidebarNav"] {display: none;}
header[data-testid="stHeader"] {display: none;}
</style>
"""
st.markdown(hide_nav, unsafe_allow_html=True)
