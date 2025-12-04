import bcrypt
from pathlib import Path
from app.data.db import connect_database
from app.data.users import get_user_by_username, insert_user
from app.data.schema import create_users_table

def register_user(username, password, role='user'):
    """Register new user with password hashing."""
    # Hash password
    password_hash = bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')
    
    # Insert into database
    insert_user(username, password_hash, role)
    return True, f"User '{username}' registered successfully."

def login_user(username, password):
    """Authenticate user."""
    user = get_user_by_username(username)
    if not user:
        return False, "User not found."
    
    # Verify password
    stored_hash = user[2]  # password_hash column
    if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
        return True, f"Login successful!"
    return False, "Incorrect password."

def migrate_users_from_file(filepath='DATA/users.txt'):
    """Migrate users from text file to database."""
    file_path = Path(filepath)

    if not file_path.exists():
        print(f"File not found: {file_path}")
        return 0  # No users migrated

    migrated_count = 0

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            
            parts = line.split(',')
            
            # Extract username, password, role
            username = parts[0].strip()
            password_hash = parts[1].strip()
            role = parts[2].strip() if len(parts) > 2 else 'user'
            
            # Insert user into database
            try:
                insert_user(username, password_hash, role)
                migrated_count += 1
            except Exception as e:
                print(f"Failed to insert user {username}: {e}")

    print(f"Migrated {migrated_count} users successfully.")
    return migrated_count