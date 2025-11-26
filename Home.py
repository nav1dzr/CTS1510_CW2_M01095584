import streamlit as st

st.set_page_config(page_title="Cyber Intelligence Platform", page_icon="🛡️")

st.title("🛡️ Cyber Intelligence Platform")
st.write("Welcome to your multi-domain intelligence dashboard.")

st.markdown("""
This platform allows you to:

- 🔐 Register or log in  
- 📊 Access cybersecurity dashboards  
- 🗂️ Explore datasets and IT tickets  
- 🎯 Use analytics and filters  
""")

st.write("---")

# If user already logged in
if "user" in st.session_state:
    st.success(f"Logged in as **{st.session_state['user']}**")
    st.page_link("pages/3_Dashboard.py", label="Go to Dashboard", icon="📊")
else:
    st.info("You are not logged in.")

    col1, col2 = st.columns(2)
    with col1:
        st.page_link("pages/1_Login.py", label="🔑 Login")

    with col2:
        st.page_link("pages/2_Register.py", label="📝 Register")
