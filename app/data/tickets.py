import pandas as pd
from pathlib import Path
from app.data.db import connect_database

def insert_ticket(conn, ticket_id, priority, status, category, subject, description, created_date, resolved_date, assigned_to, created_at):
    """Insert a new ticket into it_tickets and return its row ID."""

    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO it_tickets  
        (ticket_id, priority, status, category, subject, description, created_date, resolved_date, assigned_to, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (ticket_id, priority, status, category, subject, description, created_date, resolved_date, assigned_to, created_at))
    conn.commit()
    new_id = cursor.lastrowid

    return new_id

def update_ticket_status(conn, ticket_id, status):
    """Update ticket status and return number of rows updated."""

    cursor = conn.cursor()
    cursor.execute(
        """UPDATE it_tickets SET status = ? WHERE ticket_id = ?""",
        (status, ticket_id)
    )
    conn.commit()

    return cursor.rowcount

def delete_ticket(conn, ticket_id):
    """Delete ticket by ticket_id and return number of deleted rows."""

    cursor = conn.cursor()
    cursor.execute(
        """DELETE FROM it_tickets WHERE ticket_id = ?""", (ticket_id,)
    )
    conn.commit()

    return cursor.rowcount

def get_all_tickets(conn):
    """Get all tickets as DataFrame."""

    df = pd.read_sql_query(
        "SELECT * FROM it_tickets ORDER BY id DESC",
        conn
    )

    return df


def load_it_ticket_data_to_sql(conn, csv_path, table_name):
    """Loading sample data from IT Tickets csv to sql database."""
    
    if not csv_path.exists():
        print(f"⚠️ CSV file not found: {csv_path}")
        return 0
    
    # Reading csv using pandas
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"⚠️ Failed to read CSV: {e}")
        return 0
    
    # Insert data into IT Tickets table
    try:
        df.to_sql(name=table_name, con=conn, if_exists='append', index=False)
        row_count = len(df)
        print(f"✅ Successfully loaded {row_count} rows into '{table_name}'.")
        return row_count
    except Exception as e:
        print(f"⚠️ Failed to load data into table: {e}")
        return 0