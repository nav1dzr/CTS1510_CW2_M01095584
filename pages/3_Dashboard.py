import streamlit as st
import pandas as pd
import plotly.express as px

from session_manager import require_login
from app.data.incidents import load_all_incidents
from app.data.datasets import load_dataset_metadata
from app.data.tickets import load_it_tickets


# ----------------------
# REQUIRE LOGIN
# ----------------------
require_login()

st.title("📊 Multi-Domain Intelligence Dashboard")
st.write("""
Welcome to the unified dashboard.  
Below you can explore visual insights from **Cyber Security**, **Dataset Metadata**, 
and **IT Support Tickets**.  
Use the tabs below to navigate each domain.
""")

# ----------------------
# LOAD ALL DATA ONCE
# ----------------------
df_cs = load_all_incidents()
df_data = load_dataset_metadata()
df_it = load_it_tickets()

# Ensure date columns are datetime
df_cs["date"] = pd.to_datetime(df_cs["date"], errors="coerce")
df_it["created_at"] = pd.to_datetime(df_it["created_at"], errors="coerce")

# ----------------------
# TABS
# ----------------------
tab1, tab2, tab3 = st.tabs(["🛡 Cyber Security", "📚 Dataset Metadata", "🛠 IT Support Tickets"])

# ======================================================
#                     TAB 1 — CYBER SECURITY
# ======================================================
with tab1:
    st.header("🛡 Cyber Security Incidents Overview")

    st.write("""
    This section displays analysed security incident records.  
    Visualisations help identify **incident trends**, **severity levels**, and **threat distribution**.
    """)

    st.subheader("📌 Raw Data Preview")
    st.dataframe(df_cs, use_container_width=True)

    # ---------------- Chart 1: Severity distribution
    st.subheader("🔥 Incident Severity Distribution")
    st.write("""
    This bar chart shows how incidents are distributed between different severity levels.
    It helps understand how many **critical**, **high**, and **medium** risks your organisation faces.
    """)

    severity_counts = df_cs["severity"].value_counts()
    st.bar_chart(severity_counts)

    # ---------------- Chart 2: Incident type distribution
    st.subheader("🎯 Incident Types Breakdown")

    fig1 = px.pie(
        df_cs,
        names="incident_type",
        title="Incident Types",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(fig1)

    # ---------------- Chart 3: Monthly timeline
    st.subheader("📅 Monthly Incident Timeline")
    st.write("""
    Timeline shows how the number of incidents changes month by month.
    Useful to spot **attack waves**, **seasonal patterns**, or **increases in threat activity**.
    """)

    timeline = df_cs.set_index("date").resample("M").size()
    st.line_chart(timeline)


# ======================================================
#                     TAB 2 — DATASETS
# ======================================================
with tab2:
    st.header("📚 Dataset Metadata Overview")

    st.write("""
    This table summarises multiple datasets used across the platform.  
    Useful for understanding **dataset size**, **owner domain**, and **record counts**.
    """)

    st.subheader("📌 Raw Data Preview")
    st.dataframe(df_data, use_container_width=True)

    # ---------------- Chart: Dataset size
    st.subheader("📦 Dataset Sizes (Record Count)")
    st.write("""
    This bar chart shows how large each dataset is, based on number of records.
    """)

    fig2 = px.bar(
        df_data,
        x="dataset_name",
        y="records",
        title="Dataset Record Size",
        color="domain",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(fig2)


# ======================================================
#                     TAB 3 — IT TICKETS
# ======================================================
with tab3:
    st.header("🛠 IT Support Ticket Analytics")

    st.write("""
    This dashboard provides an overview of helpdesk activity.  
    You can analyse **ticket priorities**, **status distribution**, and **volume over time**.
    """)

    st.subheader("📌 Raw Data Preview")
    st.dataframe(df_it, use_container_width=True)

    # ---------------- Chart: Priority distribution
    st.subheader("⚡ Priority Levels")
    st.write("""
    Shows how many tickets fall under **Low**, **Medium**, **High**, or **Critical** priority levels.
    """)

    pr_counts = df_it["priority"].value_counts()
    st.bar_chart(pr_counts)

    # ---------------- Chart: Ticket Status
    st.subheader("📌 Ticket Status Overview")

    fig3 = px.pie(
        df_it,
        names="status",
        title="Ticket Resolution Status",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    st.plotly_chart(fig3)

    # ---------------- Chart: Timeline
    st.subheader("📅 Ticket Timeline")
    st.write("""
    This timeline illustrates how many IT support requests are created each month.
    This helps identify peak workload periods for IT teams.
    """)

    timeline_it = df_it.set_index("created_at").resample("M").size()
    st.line_chart(timeline_it)
