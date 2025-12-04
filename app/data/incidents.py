import pandas as pd
from app.data.db import connect_database

def insert_incident(title, severity, status, date):
    """Insert new incident."""
    #connect to database
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO cyber_incidents 
        (title, severity, status, date)
        VALUES (?, ?, ?, ?)
    """, (title, severity, status, date))
    conn.commit()
    incident_id = cursor.lastrowid
    conn.close()
    return incident_id

def get_incident_by_title(title):
    """Retrieve incident by title."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM cyber_incidents WHERE title = ?",
        (title,)
    )
    incident = cursor.fetchone()
    conn.close()
    return incident

def get_incidents_by_severity(severity):
    """Retrieve incident by severity."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM cyber_incidents WHERE severity = ?",
        (severity,)
    )
    severity_t = cursor.fetchall()
    conn.close()
    return severity_t

def get_incidents_by_status(status):
    """Retrieve incident by status."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM cyber_incidents WHERE status = ?",
        (status,)
    )
    status_t = cursor.fetchall()
    conn.close()
    return status_t

def update_incident_status(title, status):
    """Update incident status."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE cyber_incidents SET status = ? WHERE title = ?""",
        (status, title)
    )
    conn.commit()
    conn.close()
    return cursor.rowcount

def delete_incident(title):
    """Delete incident by title."""
    conn= connect_database()
    cursor = conn.cursor()
    cursor.execute(
        """DELETE FROM cyber_incidents WHERE title = ?""", (title,)
    )
    conn.commit()
    conn.close()
    return cursor.rowcount

def get_all_incidents_df():
    """Get all incidents as DataFrame."""
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM cyber_incidents ORDER BY id DESC",
        conn
    )
    conn.close()
    return df

def load_incident_data_to_sql():
    """Loading sample data from cyberincidents csv to sql database."""
    df = pd.read_csv('app/data/cyber_incidents.csv')
    conn = connect_database()
    df.to_sql('cyber_incidents', conn, if_exists='replace', index=False)
    conn.close()