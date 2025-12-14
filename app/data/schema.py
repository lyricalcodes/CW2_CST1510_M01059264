def create_users_table(conn):
    """Create users table."""

    cursor = conn.cursor()

    #sql statement to create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    print("✅ Users table created successfully!")

def create_cyber_incidents_table(conn):
    """Create cyber incidents table."""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cyber_incidents (
            incident_id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            severity TEXT NOT NULL,
            category TEXT,
            status TEXT DEFAULT 'Open',
            description TEXT
        )
    """)
    conn.commit()
    print("✅ Cyber Incidents table created successfully!")

def create_datasets_metadata_table(conn):
    """Create dataset metadata table."""
    cursor = conn.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS datasets_metadata (
            dataset_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            rows INTEGER,
            columns INTEGER,
            uploaded_by TEXT,
            upload_date INTEGER
        )
    """)
    conn.commit()
    print("✅ Datasets table created successfully!")

def create_it_tickets_table(conn):
    """Create it tickets table."""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS it_tickets (
            ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
            priority TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'Open',
            assigned_to TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            resolution_time_hours INTEGER
        )
    """)
    conn.commit()
    print("✅ IT Tickets table created successfully!")

def create_all_tables(conn):
    """Create all tables."""
    # Drop tables if they exist to ensure clean slate
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("DROP TABLE IF EXISTS cyber_incidents")
    cursor.execute("DROP TABLE IF EXISTS datasets_metadata")
    cursor.execute("DROP TABLE IF EXISTS it_tickets")
    conn.commit()
    
    create_users_table(conn)
    create_cyber_incidents_table(conn)
    create_datasets_metadata_table(conn)
    create_it_tickets_table(conn)


#titles and names are unique as they are used are used in many crud operations