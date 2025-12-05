import pandas as pd
from pathlib import Path
from app.data.db import connect_database

def insert_dataset(conn, dataset_name, category, source, last_updated, record_count, file_size_mb, created_at):
    """Insert a new dataset into datasets metadata and return its row ID."""

    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO datasets_metadata  
        (dataset_name, category, source, last_updated, record_count, file_size_mb, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (dataset_name, category, source, last_updated, record_count, file_size_mb, created_at))
    conn.commit()
    dataset_id = cursor.lastrowid

    return dataset_id

def update_dataset_size(conn, dataset_name, file_size_mb):
    """Update dataset size and return the number of rows updated."""

    cursor = conn.cursor()
    cursor.execute(
        """UPDATE datasets_metadata SET file_size_mb = ? WHERE dataset_name = ?""",
        (file_size_mb, dataset_name)
    )
    conn.commit()

    return cursor.rowcount

def delete_dataset(conn, id):
    """Delete dataset by name."""

    cursor = conn.cursor()
    cursor.execute(
        """DELETE FROM datasets_metadata WHERE id = ?""", (id,)
    )
    conn.commit()

    return cursor.rowcount

def get_all_datasets(conn):
    """Get all datasets as DataFrame."""

    df = pd.read_sql_query(
        "SELECT * FROM datasets_metadata ORDER BY id DESC",
        conn
    )

    return df

def load_dataset_data_to_sql(conn, csv_path, table_name):
    """Loading sample data from datasets metadata csv to sql database."""

    if not csv_path.exists():
        print(f"⚠️ CSV file not found: {csv_path}")
        return 0
    
    # Reading csv using pandas
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"⚠️ Failed to read CSV: {e}")
        return 0
    
    # Insert data into datasets metadata table
    try:
        df.to_sql(name=table_name, con=conn, if_exists='append', index=False)
        row_count = len(df)
        print(f"✅ Successfully loaded {row_count} rows into '{table_name}'.")
        return row_count
    except Exception as e:
        print(f"⚠️ Failed to load data into table: {e}")
        return 0
