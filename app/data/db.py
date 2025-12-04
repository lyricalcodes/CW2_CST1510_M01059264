import sqlite3
from pathlib import Path

# Define path
DB_PATH = Path("DATA") / "intelligence_platform.db"

# Create DATA folder if it doesn't exist
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def connect_database(db_path=DB_PATH):
    """Connect to SQLite database."""
    return sqlite3.connect(str(db_path))