import sqlite3

DB_PATH = 'mental_health_app.db'

try:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = cursor.fetchall()
    
    print("=" * 50)
    print("SQLite Database Verification")
    print("=" * 50)
    print(f"\nDatabase File: {DB_PATH}")
    print(f"\nTables Found: {len(tables)}")
    print("\nTable Summary:")
    print("-" * 50)
    
    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"  {table_name}: {count} records")
    
    # Check specific data
    print("\n" + "-" * 50)
    print("\nSample Data:")
    print("-" * 50)
    
    # Users
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    print(f"✓ Users: {user_count} users found")
    
    # Questions
    cursor.execute("SELECT COUNT(*) FROM questions")
    question_count = cursor.fetchone()[0]
    print(f"✓ Questions: {question_count} questions found")
    
    # Messages
    cursor.execute("SELECT COUNT(*) FROM messages")
    message_count = cursor.fetchone()[0]
    print(f"✓ Messages: {message_count} messages found")
    
    print("\n" + "=" * 50)
    print("✓ Database is properly configured!")
    print("=" * 50)
    
    conn.close()
    
except Exception as e:
    print(f"Error: {e}")
