import pandas as pd
from pathlib import Path
from app.data.db import connect_database

def load_datasets_metadata_to_sql(conn, csv_path, table_name="datasets_metadata"):
    """Load dataset metadata CSV into the SQLite table."""
    
    csv_path = Path(csv_path)
    
    if not csv_path.exists():
        print(f"CSV file not found: {csv_path}")
        return 0
        
    df = pd.read_csv(csv_path)

    # Drop dataset_id if present, since it's autoincrement
    if "dataset_id" in df.columns:
        df = df.drop(columns=["dataset_id"])

    df.to_sql(name=table_name, con=conn, if_exists='append', index=False)
    row_count = len(df)
    print(f"Successfully loaded {row_count} rows into '{table_name}'.")
    return row_count


def get_all_datasets(conn):
    """Get all datasets as DataFrame."""

    df = pd.read_sql_query(
        "SELECT * FROM datasets_metadata ORDER BY dataset_id DESC",
        conn
    )
    return df

def insert_dataset(conn, name, rows, columns, uploaded_by, upload_date):
    """Insert a new dataset into datasets metadata and return its row dataset_id."""

    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO datasets_metadata  
        (name, rows, columns, uploaded_by, upload_date)
        VALUES (?, ?, ?, ?, ?)
    """, (name, rows, columns, uploaded_by, upload_date))
    conn.commit()
    dataset_id = cursor.lastrowid

    return cursor.lastrowid

def update_dataset(conn, dataset_id, **kwargs):
    """Update a dataset record by dataset_id. Accepts column=value pairs."""
    if not kwargs:
        return 0
    
    columns = ", ".join([f"{k} = ?" for k in kwargs])
    values = list(kwargs.values())
    values.append(dataset_id)
    
    cursor = conn.cursor()
    cursor.execute(f"UPDATE datasets_metadata SET {columns} WHERE dataset_id = ?", values)
    conn.commit()
    return cursor.rowcount

def delete_dataset(conn, dataset_id):
    """Delete dataset by name."""

    cursor = conn.cursor()
    cursor.execute(
        """DELETE FROM datasets_metadata WHERE dataset_id = ?""", (dataset_id,)
    )
    conn.commit()

    return cursor.rowcount

