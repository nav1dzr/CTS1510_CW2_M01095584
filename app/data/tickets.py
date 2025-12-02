import pandas as pd
from app.data.db import get_connection

# ----------------------------------------------------
# Load CSV (used for migration or testing)
# ----------------------------------------------------
def load_it_tickets_csv():
    return pd.read_csv("DATA/it_tickets.csv")

# ----------------------------------------------------
# Migrate CSV → DB
# ----------------------------------------------------
def migrate_it_tickets_to_db():
    df = load_it_tickets_csv()

    # Drop columns not used in DB
    unwanted = ["extra_notes", "assigned_engineer", "timestamp"]
    df = df.drop(columns=[c for c in unwanted if c in df.columns])

    # Rename columns if needed
    rename_map = {
        "ticket": "ticket_id",
        "issue": "issue_category"
    }
    df = df.rename(columns=rename_map)

    # Select final columns
    keep_cols = ["ticket_id", "issue_category", "priority", "status", "created"]
    df = df[[c for c in keep_cols if c in df.columns]]

    conn = get_connection()
    df.to_sql("it_tickets", conn, if_exists="append", index=False)
    conn.close()

# ----------------------------------------------------
# Load IT tickets from DB
# ----------------------------------------------------
def load_it_tickets():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM it_tickets", conn)
    conn.close()
    return df
