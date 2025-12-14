import pandas as pd
from app.data.db import connect_database

def get_all_users(conn):
    """Fetch all users as a DataFrame."""
    df = pd.read_sql_query("SELECT * FROM users ORDER BY id DESC", conn)
    return df

def insert_user(conn, username, password_hash, role='user'):
    """Insert new user."""
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
        (username, password_hash, role)
    )
    conn.commit()
    return cursor.lastrowid

def update_user_role(conn, username, role):
    """Update user role."""
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE users SET role = ? WHERE username = ?""",
        (role, username)
    )
    conn.commit()
    return cursor.rowcount

def delete_user(conn, username):
    """Delete user by username."""
    cursor = conn.cursor()
    cursor.execute(
        """DELETE FROM users WHERE username = ?""", (username,)
    )
    conn.commit()
    return cursor.rowcount

def get_user_by_username(conn, username):
    """Retrieve user by username."""
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    )
    user = cursor.fetchone()
    return user