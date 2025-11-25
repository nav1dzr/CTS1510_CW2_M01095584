from app.data.schema import create_tables
from app.data.users import add_user
from app.data.incidents import migrate_cyber_csv_to_db
from app.data.datasets import migrate_metadata_csv_to_db
from app.data.tickets import migrate_tickets_csv_to_db
from app.data.db import get_connection

import os


# -------------------------
# MIGRATE USERS FROM TXT
# -------------------------
def migrate_users_txt():
    """
    Reads DATA/users.txt and inserts the users into the database.
    Each line must be in the format: username,hashed_password
    """
    path = "DATA/users.txt"

    if not os.path.exists(path):
        print("users.txt not found — skipping user migration.")
        return

    with open(path, "r") as f:
        lines = f.readlines()

    for line in lines:
        try:
            username, password_hash = line.strip().split(",")
            add_user(username, password_hash)
        except:
            print(f"Skipping invalid line: {line}")


# -------------------------
# FULL MIGRATION PROCESS
# -------------------------
def run_full_migration():
    print("Creating tables...")
    create_tables()
    print("Tables created.")

    print("Migrating users...")
    migrate_users_txt()
    print("Users migrated.")

    print("Migrating cyber incidents...")
    migrate_cyber_csv_to_db()
    print("Cyber dataset migrated.")

    print("Migrating dataset metadata...")
    migrate_metadata_csv_to_db()
    print("Metadata migrated.")

    print("Migrating IT tickets...")
    migrate_tickets_csv_to_db()
    print("Tickets migrated.")

    print("Migration completed successfully!")


# -------------------------
# Run only if executed directly
# -------------------------
if __name__ == "__main__":
    run_full_migration()
