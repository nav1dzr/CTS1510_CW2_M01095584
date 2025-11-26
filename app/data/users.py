import bcrypt
from app.data.db import get_connection

# --------------------------
# Register new user
# --------------------------
def register_user(username: str, password: str):
    """
    Create a new user and store a hashed password.
    """
    conn = get_connection()
    curr = conn.cursor()

    # hash password
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    sql = """
        INSERT INTO users (username, password_hash)
        VALUES (?, ?)
    """

    curr.execute(sql, (username, hashed))
    conn.commit()
    conn.close()
# --------------------------
# Get user by username
# --------------------------
def get_user_by_username(username: str):
    """
    Return one row: (id, username, password_hash) or None.
    """
    conn = get_connection()
    curr = conn.cursor()

    sql = "SELECT id, username, password_hash FROM users WHERE username = ?"
    curr.execute(sql, (username,))
    user = curr.fetchone()

    conn.close()
    return user

# --------------------------
# Check password
# --------------------------
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Compare plain text password with the stored hash.
    """
    return bcrypt.checkpw(
        plain_password.encode(),
        hashed_password.encode()
    )

# --------------------------
# Helper for debugging / tests
# --------------------------
def get_all_users():
    conn = get_connection()
    curr = conn.cursor()

    sql = "SELECT id, username FROM users"
    curr.execute(sql)
    rows = curr.fetchall()

    conn.close()
    return rows
