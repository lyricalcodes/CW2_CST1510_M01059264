import pandas as pd
from pathlib import Path
from app.data.db import connect_database

def insert_incident(conn, timestamp, severity, category, status, description):
    """Insert a new incident into cyber_incidents and return its row incident_id."""
    
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO cyber_incidents 
        (timestamp, severity, category, status, description)
        VALUES (?, ?, ?, ?, ?)
    """, (timestamp, severity, category, status, description))
    conn.commit()

    return cursor.lastrowid

def update_incident_status(conn, incident_id, new_status):
    """Update the status of an incident and returns the number of rows updated."""

    cursor = conn.cursor()
    cursor.execute(
        """UPDATE cyber_incidents SET status = ? WHERE incident_id = ?""",
        (new_status, incident_id)
    )
    conn.commit()

    return cursor.rowcount

def delete_incident(conn, incident_id):
    """Delete an incident by its incident_id and returning the number of rows deleted."""

    cursor = conn.cursor()
    cursor.execute(
        """DELETE FROM cyber_incidents WHERE incident_id = ?""", (incident_id,)
    )
    conn.commit()

    return cursor.rowcount

def get_all_incidents(conn):
    """Get all incidents as DataFrame."""

    df = pd.read_sql_query(
        "SELECT * FROM cyber_incidents ORDER BY incident_id DESC",
        conn
    )
    return df

def load_incident_data_to_sql(conn, csv_path, table_name="cyber_incidents"):
    """Loading sample data from cyberincidents csv to sql database."""

    csv_path = Path(csv_path)

    if not csv_path.exists():
        print(f"⚠️ CSV file not found: {csv_path}")
        return 0
    
    #Reading csv using pandas
    df = pd.read_csv(csv_path)
    
    # Drop incident_id if present, since it's autoincrement
    if "incident_id" in df.columns:
        df = df.drop(columns=["incident_id"])

    #Insert data into cyber incidents table
    df.to_sql(name=table_name, con=conn, if_exists='append', index=False)
    row_count = len(df)
    print(f"✅ Successfully loaded {row_count} rows into '{table_name}'.")
    return row_count

def get_incidents_by_type_count(conn):
    """Get count of incidents by category."""
    df = pd.read_sql_query(
        "SELECT category, COUNT(*) as count FROM cyber_incidents GROUP BY category",
        conn
    )
    return df

def get_high_severity_by_status(conn):
    """Get high severity incidents by status."""
    df = pd.read_sql_query(
        "SELECT status, COUNT(*) as count FROM cyber_incidents WHERE severity = 'High' GROUP BY status",
        conn
    )
    return df

