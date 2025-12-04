import pandas as pd
from app.data.db import connect_database

def insert_ticket(title, priority, status, created_date):
    """Insert new ticket."""
    #connect to database
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO it_tickets 
        (title, priority, status, created_date)
        VALUES (?, ?, ?, ?)
    """, (title, priority, status, created_date))
    conn.commit()
    ticket_id = cursor.lastrowid
    conn.close()
    return ticket_id

def get_ticket_by_title(title):
    """Retrieve ticket by title."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM it_tickets WHERE title = ?",
        (title,)
    )
    ticket = cursor.fetchone()
    conn.close()
    return ticket

def get_tickets_by_priority(priority):
    """Retrieve ticket by priority."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM it_tickets WHERE priority = ?",
        (priority,)
    )
    tickets_t = cursor.fetchall()
    conn.close()
    return tickets_t

def get_tickets_by_status(status):
    """Retrieve ticket by status."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM it_tickets WHERE status = ?",
        (status,)
    )
    tickets_t = cursor.fetchall()
    conn.close()
    return tickets_t

def update_ticket_status(title, status):
    """Update ticket status."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE it_tickets SET status = ? WHERE title = ?""",
        (status, title)
    )
    conn.commit()
    conn.close()
    return cursor.rowcount

def delete_ticket(title):
    """Delete ticket by title."""
    conn= connect_database()
    cursor = conn.cursor()
    cursor.execute(
        """DELETE FROM it_tickets WHERE title = ?""", (title,)
    )
    conn.commit()
    conn.close()
    return cursor.rowcount

def get_all_tickets():
    """Get all tickets as DataFrame."""
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM it_tickets ORDER BY id DESC",
        conn
    )
    conn.close()
    return df

def load_ticket_data_to_sql():
    """Loading sample data from it tickets csv to sql database."""
    df = pd.read_csv('app/data/it_tickets.csv')
    conn = connect_database()
    df.to_sql('it_tickets', conn, if_exists='replace', index=False)
    conn.close()