import streamlit as st

st.set_page_config(
    page_title="Cyber Intelligence Platform",
    page_icon="🛡️",
    layout="centered"
)

# ---------------------------------------
# HEADER / SPLASH SECTION
# ---------------------------------------
st.title("🛡️ Cyber Intelligence Platform")
st.write("### Unified Multi-Domain Intelligence System")

st.markdown("""
Welcome to the platform where you can:

- 🔐 **Register or log in** to your secure account  
- 📊 **View cybersecurity dashboards**  
- 🗂️ **Analyse datasets and IT tickets**  
- 📈 **Use interactive charts and filters**  
""")

st.write("---")

# ---------------------------------------
# CHECK LOGIN STATUS
# ---------------------------------------
if "user" in st.session_state:
    st.success(f"Logged in as **{st.session_state['user']}**")

    st.page_link("pages/3_Dashboard.py", label="📊 Go to Dashboard")

    # Logout button
    if st.button("Logout"):
        st.session_state.pop("user")
        st.rerun()

else:
    st.info("You are not logged in.")

    col1, col2 = st.columns(2)

    with col1:
        st.page_link("pages/1_Login.py", label="🔑 Login")

    with col2:
        st.page_link("pages/2_Register.py", label="📝 Register")
