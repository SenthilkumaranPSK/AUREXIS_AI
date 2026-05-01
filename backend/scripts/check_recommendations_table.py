"""Check if recommendations table exists and has data"""
from database.db_utils import get_db

with get_db() as conn:
    cursor = conn.cursor()
    
    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='recommendations'")
    result = cursor.fetchone()
    print(f"✓ Recommendations table exists: {result is not None}")
    
    if result:
        # Check table structure
        cursor.execute("PRAGMA table_info(recommendations)")
        columns = cursor.fetchall()
        print(f"\n✓ Table has {len(columns)} columns:")
        for col in columns:
            print(f"  - {col['name']} ({col['type']})")
        
        # Check data count
        cursor.execute("SELECT COUNT(*) as count FROM recommendations")
        count = cursor.fetchone()['count']
        print(f"\n✓ Recommendations in database: {count}")
        
        # Show sample data
        if count > 0:
            cursor.execute("SELECT * FROM recommendations LIMIT 3")
            rows = cursor.fetchall()
            print(f"\n✓ Sample recommendations:")
            for row in rows:
                print(f"  - {dict(row)}")
    else:
        print("\n✗ Table does not exist! Need to create it.")
