import pandas as pd
from pathlib import Path
from app.data.db import connect_database

def insert_incident(conn, date, incident_type, severity, status, description, reported_by=None):
    """Insert a new incident into cyber_incidents and return its row ID."""
    
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO cyber_incidents 
        (date, incident_type, severity, status, description, reported_by)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (date, incident_type, severity, status, description, reported_by))
    conn.commit()
    incident_id = cursor.lastrowid

    return incident_id

def update_incident_status(conn, id, new_status):
    """Update the status of an incident and returns the number of rows updated."""

    cursor = conn.cursor()
    cursor.execute(
        """UPDATE cyber_incidents SET status = ? WHERE id = ?""",
        (new_status, id)
    )
    conn.commit()

    return cursor.rowcount

def delete_incident(conn, id):
    """Delete an incident by its id and returning the number of rows deleted."""

    cursor = conn.cursor()
    cursor.execute(
        """DELETE FROM cyber_incidents WHERE id = ?""", (id,)
    )
    conn.commit()

    return cursor.rowcount

def get_all_incidents_df(conn):
    """Get all incidents as DataFrame."""

    df = pd.read_sql_query(
        "SELECT * FROM cyber_incidents ORDER BY id DESC",
        conn
    )

    return df

def load_incident_data_to_sql(conn, csv_path, table_name):
    """Loading sample data from cyberincidents csv to sql database."""

    if not csv_path.exists():
        print(f"⚠️ CSV file not found: {csv_path}")
        return 0
    
    # Reading csv using pandas
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"⚠️ Failed to read CSV: {e}")
        return 0
    
    # Insert data into cyber incidents table
    try:
        df.to_sql(name=table_name, con=conn, if_exists='append', index=False)
        row_count = len(df)
        print(f"✅ Successfully loaded {row_count} rows into '{table_name}'.")
        return row_count
    except Exception as e:
        print(f"⚠️ Failed to load data into table: {e}")
        return 0
