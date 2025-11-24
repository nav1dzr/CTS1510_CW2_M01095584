import bcrypt
import os

# -------------------------------
# User Data File
# -------------------------------
USER_DATA_FILE = "DATA/users.txt"


# -------------------------------
# Hash Password
# -------------------------------
def hash_password(plain_text_password):
    """
    Hashes a password using bcrypt with automatic salt generation.
    """
    password_bytes = plain_text_password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


# -------------------------------
# Verify Password
# -------------------------------
def verify_password(plain_text_password, hashed_password):
    """
    Verifies a plaintext password against a stored bcrypt hash.
    """
    password_bytes = plain_text_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)


# -------------------------------
# Check if User Exists
# -------------------------------
def user_exists(username):
    """
    Checks if a username already exists in the user database.
    """
    if not os.path.exists(USER_DATA_FILE):
        return False

    with open(USER_DATA_FILE, "r") as f:
        for line in f:
            stored_user, _ = line.strip().split(",", 1)
            if stored_user == username:
                return True

    return False


# -------------------------------
# Register User
# -------------------------------
def register_user(username, password):
    """
    Registers a new user by hashing their password
    and storing credentials.
    """
    if user_exists(username):
        print("Error: Username already exists.")
        return False

    hashed_password = hash_password(password)

    with open(USER_DATA_FILE, "a") as f:
        f.write(f"{username},{hashed_password}\n")

    print(f"User '{username}' registered successfully!")
    return True


# -------------------------------
# Login User
# -------------------------------
def login_user(username, password):
    """
    Authenticates a user by verifying username and password.
    """
    if not os.path.exists(USER_DATA_FILE):
        print("No users registered yet.")
        return False

    with open(USER_DATA_FILE, "r") as f:
        for line in f:
            stored_user, hashed = line.strip().split(",", 1)

            if stored_user == username:
                return verify_password(password, hashed)

    return False


# -------------------------------
# Username Validation
# -------------------------------
def validate_username(username):
    """
    Validates username format.
    Returns (bool, error_message)
    """
    if len(username) < 3:
        return (False, "Username must be at least 3 characters long.")

    if " " in username:
        return (False, "Username cannot contain spaces.")

    return (True, "")


# -------------------------------
# Password Validation
# -------------------------------
def validate_password(password):
    """
    Validates password strength.
    Returns (bool, error_message)
    """
    if len(password) < 8:
        return (False, "Password must be at least 8 characters long.")

    if not any(c.isdigit() for c in password):
        return (False, "Password must contain at least one number.")

    if not any(c.isalpha() for c in password):
        return (False, "Password must contain at least one letter.")

    return (True, "")