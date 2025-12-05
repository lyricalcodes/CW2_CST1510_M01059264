import bcrypt
import sqlite3
from pathlib import Path
from app.data.db import connect_database

def migrate_users_from_file(conn, filepath='DATA/users.txt'):
    """Migrate users from text file to database."""
    file_path = Path(filepath)

    if not file_path.exists():
        print(f"⚠️ File not found: {file_path}")
        print("   No users to migrate.")
        return 0  # No users migrated

    cursor = conn.cursor()
    migrated_count = 0

    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            # Parse line: username,password_hash
            parts = line.split(',')
            if len(parts) >= 2:
                username = parts[0]
                password_hash = parts[1]
                # Insert user (ignore if already exists)
                try:
                    cursor.execute(
                        "INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                        (username, password_hash, 'user')
                    )
                    if cursor.rowcount > 0:
                        migrated_count += 1
                except sqlite3.Error as e:
                    print(f"Error migrating user {username}: {e}")
    
    conn.commit()
    print(f"✅ Migrated {migrated_count} users from {file_path.name}")

# Verify users were migrated
conn = connect_database()
cursor = conn.cursor()

# Query all users
cursor.execute("SELECT id, username, role FROM users")
users = cursor.fetchall()

print(" Users in database:")
print(f"{'ID':<5} {'Username':<15} {'Role':<10}")
print("-" * 35)
for user in users:
    print(f"{user[0]:<5} {user[1]:<15} {user[2]:<10}")

print(f"\nTotal users: {len(users)}")
conn.close()

def register_user(username, password, role='user'):
    """Register new user with password hashing."""

    conn = connect_database()
    cursor = conn.cursor()

    # Check if user already exists
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return False, f"Username '{username}' already exists."

    # Hash password
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    password_hash = hashed.decode('utf-8')
    
    # Insert new user
    cursor.execute(
        "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
        (username, password_hash, role)
    )
    conn.commit()
    conn.close()

    return True, f"User '{username}' registered successfully!"

def login_user(username, password):
    """Authenticate user."""

    conn = connect_database()
    cursor = conn.cursor()

    # Find user
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    # Verify password (user[2] is password_hash column)
    stored_hash = user[2]
    password_bytes = password.encode('utf-8')
    hash_bytes = stored_hash.encode('utf-8')
    
    if bcrypt.checkpw(password_bytes, hash_bytes):
        return True, f"Welcome, {username}!"
    else:
        return False, "Invalid password."