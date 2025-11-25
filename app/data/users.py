from app.data.db import get_connection

# -------------------------
# CREATE (Add user)
# -------------------------
def add_user(username, password_hash):
    conn = get_connection()
    curr = conn.cursor()

    sql = """INSERT INTO users (username, password_hash)
             VALUES (?, ?)"""

    try:
        curr.execute(sql, (username, password_hash))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error adding user: {e}")
        return False
    finally:
        conn.close()


# -------------------------
# READ (Get all users)
# -------------------------
def get_all_users():
    conn = get_connection()
    curr = conn.cursor()

    curr.execute("SELECT * FROM users")
    users = curr.fetchall()

    conn.close()
    return users


# -------------------------
# READ (Get one user)
# -------------------------
def get_user_by_username(username):
    conn = get_connection()
    curr = conn.cursor()

    sql = "SELECT * FROM users WHERE username = ?"
    curr.execute(sql, (username,))
    user = curr.fetchone()

    conn.close()
    return user


# -------------------------
# UPDATE (Change password)
# -------------------------
def update_user_password(username, new_hash):
    conn = get_connection()
    curr = conn.cursor()

    sql = """UPDATE users
             SET password_hash = ?
             WHERE username = ?"""

    curr.execute(sql, (new_hash, username))
    
    conn.commit()
    conn.close()


# -------------------------
# DELETE (Remove user)
# -------------------------
def delete_user(username):
    conn = get_connection()
    curr = conn.cursor()

    curr.execute("DELETE FROM users WHERE username = ?", (username,))
    conn.commit()
    conn.close()
