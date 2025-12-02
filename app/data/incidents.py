import pandas as pd
from app.data.db import get_connection

def load_all_incidents():
    """
    Loads all cyber incidents from the database
    into a pandas DataFrame.
    Expected columns: id, incident_type, severity, date, description
    """
    conn = get_connection()
    df = pd.read_sql_query(
        "SELECT id, incident_type, severity, date, description FROM cyber_incidents",
        conn
    )
    conn.close()
    return df
