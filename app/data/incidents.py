import pandas as pd
from app.data.db import get_connection

# -------------------------
# CREATE (Add incident)
# -------------------------
def add_incident(incident_type, severity, date, description):
    conn = get_connection()
    curr = conn.cursor()

    sql = """INSERT INTO cyber_incidents
             (incident_type, severity, date, description)
             VALUES (?, ?, ?, ?)"""

    curr.execute(sql, (incident_type, severity, date, description))

    conn.commit()
    conn.close()


# -------------------------
# READ (Get all incidents)
# -------------------------
def get_all_incidents():
    conn = get_connection()
    curr = conn.cursor()

    curr.execute("SELECT * FROM cyber_incidents")
    rows = curr.fetchall()

    conn.close()
    return rows


# -------------------------
# LOAD CSV → Using pandas (Week 8 requirement)
# -------------------------
def load_cyber_csv():
    """
    Loads cyber_incidents.csv from DATA folder using pandas
    and returns it as a DataFrame.
    """
    df = pd.read_csv("DATA/cyber_incidents.csv")
    return df


# -------------------------
# MIGRATE CSV → Into DB
# -------------------------
def migrate_cyber_csv_to_db():
    df = load_cyber_csv()

    # Drop columns not needed
    drop_cols = ["incident_id", "status"]
    df = df.drop(columns=[col for col in drop_cols if col in df.columns])

    # Rename CSV columns to match DB schema
    df = df.rename(columns={
        "category": "incident_type",
        "timestamp": "date"
    })

    # Keep only valid DB columns
    df = df[["incident_type", "severity", "date", "description"]]

    conn = get_connection()
    df.to_sql("cyber_incidents", conn, if_exists="append", index=False)
    conn.close()
