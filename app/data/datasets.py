import pandas as pd
from app.data.db import get_connection

def add_dataset(dataset_name, domain, records):
    conn = get_connection()
    curr = conn.cursor()

    sql = """INSERT INTO datasets_metadata
             (dataset_name, domain, records)
             VALUES (?, ?, ?)"""

    curr.execute(sql, (dataset_name, domain, records))

    conn.commit()
    conn.close()


def get_all_datasets():
    conn = get_connection()
    curr = conn.cursor()

    curr.execute("SELECT * FROM datasets_metadata")
    rows = curr.fetchall()

    conn.close()
    return rows


def load_metadata_csv():
    df = pd.read_csv("DATA/datasets_metadata.csv")
    return df


def migrate_metadata_csv_to_db():
    df = load_metadata_csv()

    # 1. Drop unwanted columns
    unwanted_columns = ["dataset_id", "columns", "upload_date"]
    df = df.drop(columns=[col for col in unwanted_columns if col in df.columns])

    # 2. Rename columns to match DB schema
    df = df.rename(columns={
        "name": "dataset_name",
        "uploaded_by": "domain",
        "rows": "records"
    })

    # 3. Keep only the valid final DB columns
    df = df[["dataset_name", "domain", "records"]]

    # 4. Insert into DB
    conn = get_connection()
    df.to_sql("datasets_metadata", conn, if_exists="append", index=False)
    conn.close()

