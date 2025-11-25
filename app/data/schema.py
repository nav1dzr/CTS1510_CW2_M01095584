from app.data.db import get_connection

def create_tables():
    conn = get_connection()
    curr = conn.cursor()

    # USERS TABLE
    curr.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        );
    """)

    # CYBER INCIDENTS
    curr.execute("""
        CREATE TABLE IF NOT EXISTS cyber_incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            incident_type TEXT,
            severity TEXT,
            date TEXT,
            description TEXT
        );
    """)

    # DATASETS METADATA
    curr.execute("""
        CREATE TABLE IF NOT EXISTS datasets_metadata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dataset_name TEXT,
            domain TEXT,
            records INTEGER
        );
    """)

    # IT TICKETS
    curr.execute("""
        CREATE TABLE IF NOT EXISTS it_tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id TEXT,
            category TEXT,
            priority TEXT,
            status TEXT,
            created_at TEXT
        );
    """)

    conn.commit()
    conn.close()
