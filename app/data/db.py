import sqlite3
import os

DB_PATH = "DATA/telligence_platform.db"

def get_connection():
    """
    Opens a connection to the SQLite database.
    If the database file does not exist, it will be created.
    """
    # Make sure the DATA folder exists
    os.makedirs("DATA", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    return conn
