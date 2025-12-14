import pandas as pd
from pathlib import Path
from app.data.db import connect_database

def insert_ticket(conn, priority, description, status, assigned_to, created_at, resolution_time_hours):
    """Insert a new ticket into it_tickets and return its row ticket_id."""

    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO it_tickets  
        (priority, description, status, assigned_to, created_at, resolution_time_hours)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (priority, description, status, assigned_to, created_at, resolution_time_hours))
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
        "SELECT * FROM it_tickets ORDER BY ticket_id DESC",
        conn
    )

    return df


def load_it_ticket_data_to_sql(conn, csv_path, table_name="it_tickets"):
    """Loading sample data from IT Tickets csv to sql database."""
    
    csv_path = Path(csv_path)

    if not csv_path.exists():
        print(f"⚠️ CSV file not found: {csv_path}")
        return 0
    
    #reading csv using pandas
    df = pd.read_csv(csv_path)
    
    #drop ticket_id if present, since it's autoincrement
    if "ticket_id" in df.columns:
        df = df.drop(columns=["ticket_id"])
    
    #insert data into IT Tickets table
    df.to_sql(name=table_name, con=conn, if_exists='append', index=False)
    row_count = len(df)
    print(f"✅ Successfully loaded {row_count} rows into '{table_name}'.")
    return row_count
