import pandas as pd
from app.data.db import connect_database

def insert_dataset(name, source, category, size):
    """Insert new dataset."""
    #connect to database
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO datasets_metadata 
        (name, source, category, size)
        VALUES (?, ?, ?, ?)
    """, (name, source, category, size))
    conn.commit()
    dataset_id = cursor.lastrowid
    conn.close()
    return dataset_id

def get_dataset_by_name(name):
    """Retrieve dataset by name."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM datasets_metadata WHERE name = ?",
        (name,)
    )
    dataset = cursor.fetchone()
    conn.close()
    return dataset

def get_datasets_by_source(source):
    """Retrieve dataset by source."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM datasets_metadata WHERE source = ?",
        (source,)
    )
    datasets = cursor.fetchall()
    conn.close()
    return datasets

def get_datasets_by_category(category):
    """Retrieve dataset by category."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM datasets_metadata WHERE category = ?",
        (category,)
    )
    datasets = cursor.fetchall()
    conn.close()
    return datasets

def update_dataset_size(name, size):
    """Update dataset size."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE datasets_metadata SET size = ? WHERE name = ?""",
        (size, name)
    )
    conn.commit()
    conn.close()
    return cursor.rowcount

def delete_dataset(name):
    """Delete dataset by name."""
    conn= connect_database()
    cursor = conn.cursor()
    cursor.execute(
        """DELETE FROM datasets_metadata WHERE name = ?""", (name,)
    )
    conn.commit()
    conn.close()
    return cursor.rowcount

def get_all_datasets():
    """Get all datasets as DataFrame."""
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM datasets_metadata ORDER BY id DESC",
        conn
    )
    conn.close()
    return df

def load_dataset_data_to_sql():
    """Loading sample data from dataset metadata csv to sql database."""
    df = pd.read_csv('app/data/datasets_metadata.csv')
    conn = connect_database()
    df.to_sql('datasets_metadata', conn, if_exists='replace', index=False)
    conn.close()