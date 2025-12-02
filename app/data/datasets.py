import pandas as pd
from app.data.db import get_connection

def load_dataset_metadata():
    """
    Loads dataset metadata from the database.
    Expected columns: id, dataset_name, domain, records
    """
    conn = get_connection()
    df = pd.read_sql_query(
        "SELECT id, dataset_name, domain, records FROM datasets_metadata",
        conn
    )
    conn.close()
    return df
