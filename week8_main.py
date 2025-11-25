from app.data.schema import create_tables
from app.data.migration import run_full_migration
from app.data.users import get_all_users
from app.data.incidents import get_all_incidents
from app.data.datasets import get_all_datasets
from app.data.tickets import get_all_tickets


def main():
    print("=== WEEK 8 DATABASE SETUP ===")

    # 1. Create tables
    create_tables()
    print("Tables created.\n")

    # 2. Run full migration (users.txt + all CSVs)
    run_full_migration()
    print("\nMigration completed.\n")

    # 3. Display data from each table
    print("=== Users in Database ===")
    print(get_all_users())
    print()

    print("=== Cyber Incidents ===")
    print(get_all_incidents())
    print()

    print("=== Dataset Metadata ===")
    print(get_all_datasets())
    print()

    print("=== IT Tickets ===")
    print(get_all_tickets())
    print()


if __name__ == "__main__":
    main()
