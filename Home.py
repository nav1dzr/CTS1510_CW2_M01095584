import streamlit as st
from session_manager import is_logged_in, logout_user

st.set_page_config(page_title="Cyber Intelligence Platform", page_icon="🛡️")

st.title("🛡️ Cyber Intelligence Platform")
st.write("Welcome to your multi-domain intelligence dashboard.")

st.markdown("""
### Platform Features  
- 🔐 Secure Login & Registration  
- 📊 Cybersecurity Dashboard  
- 🗂️ Loaded datasets & analytics  
- 🎯 Filtering, charts & insights  
""")

st.write("---")

# -----------------------
# SIDEBAR LOGOUT BUTTON
# -----------------------
if is_logged_in():
    if st.sidebar.button("🚪 Log Out"):
        logout_user()
        st.success("Logged out successfully!")
        st.switch_page("Home.py")

# -----------------------
# MAIN CONTENT
# -----------------------
if is_logged_in():
    st.success(f"Logged in as **{st.session_state['user']}**")

    st.page_link("pages/3_Dashboard.py", label="📊 Go to Dashboard")
else:
    st.info("You are not logged in.")

    col1, col2 = st.columns(2)
    with col1:
        st.page_link("pages/1_Login.py", label="🔑 Login")

    with col2:
        st.page_link("pages/2_Register.py", label="📝 Register")
