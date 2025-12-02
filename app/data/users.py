import bcrypt
from app.data.db import get_connection

def register_user(username, password):
    conn = get_connection()
    curr = conn.cursor()

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    curr.execute("""
        INSERT INTO users (username, password_hash)
        VALUES (?, ?)
    """, (username, hashed))

    conn.commit()
    conn.close()

def get_user_by_username(username):
    conn = get_connection()
    curr = conn.cursor()
    curr.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = curr.fetchone()
    conn.close()
    return user

def verify_password(plain, hashed):
    return bcrypt.checkpw(plain.encode(), hashed.encode())
