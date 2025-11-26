import streamlit as st
import pandas as pd
from app.data.db import get_connection
import plotly.express as px

import streamlit as st

# ACCESS CONTROL
if "user" not in st.session_state:
    st.error("You must log in to access the dashboard.")
    st.page_link("pages/1_Login.py", label="Go to Login", icon="🔑")
    st.stop()



# -----------------------------
# LOAD DATA FROM DATABASE
# -----------------------------
def load_incidents():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM cyber_incidents", conn)
    conn.close()
    return df

df = load_incidents()

# -----------------------------
# PAGE TITLE
# -----------------------------
st.title("📊 Dashboard")
st.write("### Sample Cyber Incidents")

# -----------------------------
# SUMMARY METRICS
# -----------------------------
total_incidents = len(df)
critical_count = (df["severity"] == "Critical").sum()
phishing_count = (df["incident_type"] == "Phishing").sum()

col1, col2, col3 = st.columns(3)
col1.metric("Total Incidents", total_incidents)
col2.metric("Critical Incidents", critical_count)
col3.metric("Phishing Incidents", phishing_count)

st.write("---")

# -----------------------------
# FILTERS
# -----------------------------
st.subheader("Filter Incidents")

severity_list = df["severity"].unique()
type_list = df["incident_type"].unique()

col1, col2 = st.columns(2)
selected_severity = col1.selectbox("Select Severity", ["All"] + list(severity_list))
selected_type = col2.selectbox("Select Incident Type", ["All"] + list(type_list))

filtered_df = df.copy()

if selected_severity != "All":
    filtered_df = filtered_df[filtered_df["severity"] == selected_severity]

if selected_type != "All":
    filtered_df = filtered_df[filtered_df["incident_type"] == selected_type]

st.write("### Filtered Results")
st.dataframe(filtered_df)

st.write("---")

# -----------------------------
# CHART 1: BAR CHART
# -----------------------------
st.subheader("Incidents by Severity")
severity_counts = df["severity"].value_counts()
st.bar_chart(severity_counts)

# -----------------------------
# CHART 2: PIE CHART
# -----------------------------
st.subheader("Incident Type Distribution")
fig = px.pie(
    df,
    names="incident_type",
    title="Incident Types",
    color_discrete_sequence=px.colors.qualitative.Pastel
)
st.plotly_chart(fig)

# -----------------------------
# CHART 3: TIMELINE
# -----------------------------
st.subheader("Incident Timeline")

df_sorted = df.sort_values("date")
df_sorted["date"] = pd.to_datetime(df_sorted["date"], errors="coerce")

timeline = df_sorted.set_index("date").resample("M").size()

st.line_chart(timeline)


if st.sidebar.button("Logout"):
    st.session_state.pop("user")
    st.rerun()
    st.success("You have been logged out.")