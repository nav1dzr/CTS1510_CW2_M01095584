import pandas as pd
from app.data.db import get_connection

def load_incidents():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM cyber_incidents", conn)
    conn.close()
    return df
