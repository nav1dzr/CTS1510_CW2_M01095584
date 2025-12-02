from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import pandas as pd
from session_manager import is_logged_in, logout_user
from app.data.incidents import load_all_incidents
from app.data.datasets import load_dataset_metadata
from app.data.tickets import load_it_tickets

st.session_state["current_page"] = "home"

from components.ai_assistant import floating_ai_chat

# ---------------------------------
# PAGE CONFIG
# ---------------------------------
st.set_page_config(page_title="Cyber Intelligence Platform", page_icon="🛡️")


# ---------------------------------
# SIDEBAR (NAV + LOGOUT)
# ---------------------------------
with st.sidebar:
    st.title("🧭 Navigation")

    if is_logged_in():
        st.success(f"Logged in as **{st.session_state['user']}**")

        if st.button("🚪 Log out"):
            logout_user()
            st.rerun()
    else:
        st.info("You are not logged in.")
        st.page_link("pages/1_Login.py", label="🔑 Login")
        st.page_link("pages/2_Register.py", label="📝 Register")

    st.page_link("pages/3_Dashboard.py", label="📊 Dashboard")


# ---------------------------------
# MAIN: TITLE + INTRO
# ---------------------------------
st.title("🛡️ Cyber Intelligence Platform")

st.markdown("""
Welcome to your **Multi-Domain Intelligence Platform**.

This system brings together:

- 🛡️ **Cyber Security incidents**
- 📚 **Dataset metadata** (for Data Science & Analytics)
- 🛠️ **IT Support tickets**

Use the navigation on the left to **log in**, **register**, or open the **dashboard**.
Below, you can try the built-in **offline AI assistant** that analyses your data
without using any external API.
""")

# ------------- helpers to load data safely -------------
@st.cache_data
def get_cyber_df():
    df = load_all_incidents()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    return df


@st.cache_data
def get_datasets_df():
    return load_dataset_metadata()


@st.cache_data
def get_it_df():
    df = load_it_tickets()
    df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
    return df


# ------------- analysis helpers for each domain -------------
def analyse_cyber(question: str, df: pd.DataFrame) -> str:
    total = len(df)
    most_common_type = df["incident_type"].mode()[0]
    most_common_severity = df["severity"].mode()[0]

    text = [
        f"- There are **{total}** recorded cyber incidents.",
        f"- The most common incident type is **{most_common_type}**.",
        f"- The most frequent severity level is **{most_common_severity}**.",
    ]

    q = question.lower()

    # Extra logic based on keywords
    if "phishing" in q:
        phish_count = (df["incident_type"] == "Phishing").sum()
        text.append(f"- **{phish_count}** incidents are related to **Phishing** attacks.")
    if "trend" in q or "time" in q or "timeline" in q:
        by_month = df.set_index("date").resample("M").size()
        if len(by_month) > 0:
            peak_month = by_month.idxmax().strftime("%Y-%m")
            peak_val = by_month.max()
            text.append(
                f"- The busiest month for incidents was **{peak_month}** "
                f"with **{peak_val}** incidents."
            )

    text.append(
        "- Overall, you should monitor **high/critical severity** incidents closely "
        "and ensure phishing awareness training is in place."
    )

    return "\n".join(text)


def analyse_datasets(question: str, df: pd.DataFrame) -> str:
    total = len(df)
    largest_idx = df["records"].idxmax()
    largest_name = df.loc[largest_idx, "dataset_name"]
    largest_size = df.loc[largest_idx, "records"]

    text = [
        f"- There are **{total}** datasets registered in the platform.",
        f"- The largest dataset is **{largest_name}** with **{largest_size}** records.",
    ]

    # Domain distribution
    domain_counts = df["domain"].value_counts()
    top_domain = domain_counts.index[0]
    top_domain_val = domain_counts.iloc[0]
    text.append(
        f"- The most common domain is **{top_domain}** "
        f"with **{top_domain_val}** datasets."
    )

    q = question.lower()
    if "size" in q or "big" in q or "large" in q:
        text.append(
            "- You asked about size: consider focusing on the largest datasets when doing "
            "heavy analytics or performance testing."
        )
    if "domain" in q:
        text.append(
            "- You asked about domains: domains represent which team or use-case "
            "owns each dataset (e.g. *data_scientist*, *cyber_admin*, *it_admin*)."
        )

    return "\n".join(text)


def analyse_it(question: str, df: pd.DataFrame) -> str:
    total = len(df)
    open_tickets = (df["status"] == "Open").sum()
    critical = (df["priority"] == "Critical").sum()

    text = [
        f"- There are **{total}** IT support tickets in total.",
        f"- **{open_tickets}** tickets are currently **Open**.",
        f"- **{critical}** tickets are marked as **Critical** priority.",
    ]

    status_counts = df["status"].value_counts()
    top_status = status_counts.index[0]
    top_status_val = status_counts.iloc[0]
    text.append(
        f"- The most common ticket status is **{top_status}** "
        f"with **{top_status_val}** tickets."
    )

    q = question.lower()
    if "backlog" in q or "open" in q or "delay" in q:
        text.append(
            "- You mentioned backlog/open tickets: consider prioritising **Critical** and "
            "**High priority** tickets that are still open."
        )
    if "trend" in q or "time" in q or "timeline" in q:
        by_month = df.set_index("created_at").resample("M").size()
        if len(by_month) > 0:
            peak_month = by_month.idxmax().strftime("%Y-%m")
            peak_val = by_month.max()
            text.append(
                f"- Ticket trend: the busiest month for IT tickets was **{peak_month}** "
                f"with **{peak_val}** tickets created."
            )

    return "\n".join(text)


# ------------- UI for AI assistant -------------
if not is_logged_in():
    st.warning("You must be **logged in** to use the AI assistant with real data.")
else:
    st.subheader("Ask a question about your data")

    domain = st.selectbox(
        "Which area do you want to analyse?",
        ["Cyber Security Incidents", "Dataset Metadata", "IT Support Tickets"],
    )

    question = st.text_area(
        "Type your question (for example: 'What is the trend of high severity incidents?' )",
        height=80,
    )

    if st.button("🔍 Analyse"):
        if not question.strip():
            st.error("Please type a question first.")
        else:
            if domain == "Cyber Security Incidents":
                df = get_cyber_df()
                answer = analyse_cyber(question, df)
                st.markdown("### 🛡 Cyber Security Insight")
                st.markdown(answer)

            elif domain == "Dataset Metadata":
                df = get_datasets_df()
                answer = analyse_datasets(question, df)
                st.markdown("### 📚 Dataset Insight")
                st.markdown(answer)

            else:  # IT Support Tickets
                df = get_it_df()
                answer = analyse_it(question, df)
                st.markdown("### 🛠 IT Support Insight")
                st.markdown(answer)

            st.info("This response is generated using offline rules and statistics, not an external AI API.")

# Add AI assistant at the bottom of the page
floating_ai_chat()


