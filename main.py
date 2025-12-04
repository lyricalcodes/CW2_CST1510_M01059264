from app.data.db import connect_database
from app.data.schema import create_all_tables
from app.services.user_service import register_user, login_user, migrate_users_from_file
from app.data.incidents import insert_incident, get_all_incidents_df

def main():
    print("=" * 60)
    print("Week 8: Database")
    print("=" * 60)
    
    # 1. Setup database
    conn = connect_database()
    create_all_tables(conn)
    conn.close()
    
    # 2. Migrate users
    migrate_users_from_file('DATA/users.txt')
    
    # 3. Test authentication
    success, msg = register_user("alice", "SecurePass123!", "analyst")
    print(msg)
    
    success, msg = login_user("alice", "SecurePass123!")
    print(msg)
    
    # 4. Test CRUD
    incident_id = insert_incident(
        "Phishing",
        "High",
        "Open",
        "2024-11-05"
    )
    print(f"Created incident #{incident_id}")
    
    # 5. Query data
    df = get_all_incidents_df()
    print(f"Total incidents: {len(df)}")

if __name__ == "__main__":
    main()