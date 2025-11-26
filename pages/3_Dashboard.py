import streamlit as st
import pandas as pd
import plotly.express as px

from session_manager import is_logged_in, logout_user
from app.data.incidents import load_incidents
from app.data.datasets import load_datasets_metadata
from app.data.tickets import load_it_tickets

# ----------------------------
# AUTH CHECK
# ----------------------------
if not is_logged_in():
    st.error("You must log in to access the dashboard.")
    st.stop()

st.title("📊 Intelligence Dashboard")

# Logout Button (top-right)
st.sidebar.button("Logout", on_click=logout_user, use_container_width=True)

# ----------------------------
# TABS
# ----------------------------
tab1, tab2, tab3 = st.tabs([
    "🛡 Cybersecurity Incidents",
    "📚 Dataset Metadata",
    "🧾 IT Ticket Analytics"
])

# ===============================================================
# TAB 1 — CYBER INCIDENTS
# ===============================================================
with tab1:
    st.subheader("Cybersecurity Incidents")

    df = load_incidents()

    # Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Incidents", len(df))
    col2.metric("Critical", (df["severity"] == "Critical").sum())
    col3.metric("Phishing", (df["incident_type"] == "Phishing").sum())

    st.write("### Incident Records")
    st.dataframe(df)

    # Chart: Severity
    st.write("### Incidents by Severity")
    st.bar_chart(df["severity"].value_counts())

    # Chart: Incident Types (Pie)
    fig = px.pie(df, names="incident_type", title="Incident Type Distribution")
    st.plotly_chart(fig)

# ===============================================================
# TAB 2 — DATASET METADATA
# ===============================================================
with tab2:
    st.subheader("Dataset Metadata Overview")

    df_meta = load_datasets_metadata()

    st.write("### Raw Metadata")
    st.dataframe(df_meta)

    # Records chart
    st.write("### Dataset Size Comparison")
    fig_meta = px.bar(df_meta, x="dataset_name", y="records",
                      title="Record Count per Dataset")
    st.plotly_chart(fig_meta)

# ===============================================================
# TAB 3 — IT TICKETS
# ===============================================================
with tab3:
    st.subheader("IT Ticket Analytics")

    df_tickets = load_it_tickets()

    st.write("### Ticket Records")
    st.dataframe(df_tickets)

    # Bar chart of priorities
    st.write("### Tickets by Priority")
    fig_t = px.bar(df_tickets["priority"].value_counts(),
                   title="Priority Distribution")
    st.plotly_chart(fig_t)
