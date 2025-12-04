import pandas as pd
from app.data.db import connect_database

def insert_user(username, password_hash, role='user'):
    """Insert new user."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
        (username, password_hash, role)
    )
    conn.commit()
    conn.close()

def get_user_by_username(username):
    """Retrieve user by username."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    )
    user = cursor.fetchone()
    conn.close()
    return user

def get_users_by_role(role):
    """Retrieve users by role."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT username, role FROM users WHERE role = ?",
        (role,)
    )
    users = cursor.fetchall()
    conn.close()
    return users

def get_all_users():
    """Retrieve all users."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    all_users = cursor.fetchall()
    conn.close()
    return all_users

def update_user_role(username, role):
    """Update user role."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE users SET role = ? WHERE username = ?""",
        (role, username)
    )
    conn.commit()
    conn.close()
    return cursor.rowcount

def delete_user(username):
    """Delete user by username."""
    conn= connect_database()
    cursor = conn.cursor()
    cursor.execute(
        """DELETE FROM users WHERE username = ?""", (username,)
    )
    conn.commit()
    conn.close()
    return cursor.rowcount