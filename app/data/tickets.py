import pandas as pd
from app.data.db import get_connection

# -------------------------
# CREATE (Add IT ticket)
# -------------------------
def add_ticket(ticket_id, category, priority, status, created_at):
    conn = get_connection()
    curr = conn.cursor()

    sql = """INSERT INTO it_tickets
             (ticket_id, category, priority, status, created_at)
             VALUES (?, ?, ?, ?, ?)"""

    curr.execute(sql, (ticket_id, category, priority, status, created_at))

    conn.commit()
    conn.close()


# -------------------------
# READ (Get all tickets)
# -------------------------
def get_all_tickets():
    conn = get_connection()
    curr = conn.cursor()

    curr.execute("SELECT * FROM it_tickets")
    rows = curr.fetchall()

    conn.close()
    return rows


# -------------------------
# LOAD CSV → Using pandas
# -------------------------
def load_tickets_csv():
    """
    Loads it_tickets.csv from DATA folder using pandas.
    """
    df = pd.read_csv("DATA/it_tickets.csv")
    return df


# -------------------------
# MIGRATE CSV → Into DB
# -------------------------
def migrate_tickets_csv_to_db():
    df = load_tickets_csv()

    # Drop columns not needed
    drop_cols = ["description", "assigned_to", "resolution_time_hours"]
    df = df.drop(columns=[c for c in drop_cols if c in df.columns])

    # Add a category placeholder because DB expects one
    df["category"] = "General"

    # Reorder columns to match database
    df = df[["ticket_id", "category", "priority", "status", "created_at"]]

    conn = get_connection()
    df.to_sql("it_tickets", conn, if_exists="append", index=False)
    conn.close()

