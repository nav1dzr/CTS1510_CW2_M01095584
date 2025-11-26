import pandas as pd
from app.data.db import get_connection

def load_datasets_metadata():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM datasets_metadata", conn)
    conn.close()
    return df
