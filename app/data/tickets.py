import pandas as pd
from app.data.db import get_connection

def load_it_tickets():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM it_tickets", conn)
    conn.close()
    return df
