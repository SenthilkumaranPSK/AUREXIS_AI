"""
Update all 12 users with complete data for AUREXIS AI
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import sqlite3
import hashlib
import secrets
from datetime import datetime
from database.connection_enhanced import close_connection_pool


def hash_password(password: str) -> str:
    """Hash password using SHA-256 with salt"""
    salt = secrets.token_hex(32)
    password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    return f"{salt}:{password_hash}"


def update_database_schema(conn):
    """Update database schema to include additional user fields"""
    cursor = conn.cursor()
    
    # Check if columns exist
    cursor.execute("PRAGMA table_info(users)")
    existing_columns = [col[1] for col in cursor.fetchall()]
    
    # Add new columns if they don't exist
    new_columns = {
        'account_number': 'TEXT',
        'bank_name': 'TEXT',
        'account_type': 'TEXT',
        'bank_location': 'TEXT',
        'has_credit_card': 'INTEGER DEFAULT 0',
        'user_code': 'TEXT'
    }
    
    for col_name, col_type in new_columns.items():
        if col_name not in existing_columns:
            try:
                cursor.execute(f"ALTER TABLE users ADD COLUMN {col_name} {col_type}")
                print(f"✓ Added column: {col_name}")
            except sqlite3.OperationalError:
                print(f"Column {col_name} already exists or error adding")
    
    conn.commit()


def clear_existing_users(conn):
    """Clear all existing users"""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='users'")
    conn.commit()
    print("✓ Cleared existing users")


def insert_all_users(conn):
    """Insert all 12 users with complete data"""
    
    users_data = [
        {
            "id": "1010101010",
            "name": "Senthilkumaran",
            "user_code": "22243045",
            "email": "sk@gmail.com",
            "password": "Senthilkumaran@2000",
            "account_number": "1010101010",
            "bank_name": "Indian",
            "account_type": "Savings",
            "bank_location": "Salem",
            "has_credit_card": 1,
            "occupation": "Software Engineer",
            "age": 24,
            "location": "Salem"
        },
        {
            "id": "1111111111",
            "name": "Imayavarman",
            "user_code": "22243017",
            "email": "imi@gmail.com",
            "password": "Imayavarman@2000",
            "account_number": "1111111111",
            "bank_name": "KVB",
            "account_type": "Savings",
            "bank_location": "Erode",
            "has_credit_card": 1,
            "occupation": "Doctor",
            "age": 32,
            "location": "Erode"
        },
        {
            "id": "1212121212",
            "name": "Srivarshan",
            "user_code": "22243050",
            "email": "sri@gmail.com",
            "password": "Srivarshan@2000",
            "account_number": "1212121212",
            "bank_name": "Canara",
            "account_type": "Current",
            "bank_location": "Theni",
            "has_credit_card": 1,
            "occupation": "Business Owner",
            "age": 40,
            "location": "Theni"
        },
        {
            "id": "1313131313",
            "name": "Rahulprasath",
            "user_code": "22243040",
            "email": "rp@gmail.com",
            "password": "Rahulprasath@2000",
            "account_number": "1313131313",
            "bank_name": "AXIS",
            "account_type": "Savings",
            "bank_location": "Omalur",
            "has_credit_card": 0,
            "occupation": "Teacher",
            "age": 30,
            "location": "Omalur"
        },
        {
            "id": "1414141414",
            "name": "Magudesh",
            "user_code": "22243055",
            "email": "magu@gmail.com",
            "password": "Magudesh@2000",
            "account_number": "1414141414",
            "bank_name": "Canara",
            "account_type": "Savings",
            "bank_location": "Bangalore",
            "has_credit_card": 0,
            "occupation": "Freelancer",
            "age": 28,
            "location": "Bangalore"
        },
        {
            "id": "2020202020",
            "name": "Deepak",
            "user_code": "22243009",
            "email": "dee@gmail.com",
            "password": "Deepak@2000",
            "account_number": "2020202020",
            "bank_name": "KVB",
            "account_type": "Current",
            "bank_location": "Chennai",
            "has_credit_card": 0,
            "occupation": "CA",
            "age": 29,
            "location": "Chennai"
        },
        {
            "id": "2121212121",
            "name": "Mani",
            "user_code": "22243060",
            "email": "mani@gmail.com",
            "password": "Mani@2000",
            "account_number": "2121212121",
            "bank_name": "SBI",
            "account_type": "Savings",
            "bank_location": "Edapadi",
            "has_credit_card": 1,
            "occupation": "Government Employee",
            "age": 38,
            "location": "Edapadi"
        },
        {
            "id": "2222222222",
            "name": "Dineshkumar",
            "user_code": "22243012",
            "email": "dk@gmail.com",
            "password": "Dineshkumar@2000",
            "account_number": "2222222222",
            "bank_name": "Indian",
            "account_type": "Savings",
            "bank_location": "Sangagari",
            "has_credit_card": 1,
            "occupation": "Lawyer",
            "age": 52,
            "location": "Sangagari"
        },
        {
            "id": "2525252525",
            "name": "Avinash",
            "user_code": "22243007",
            "email": "avi@gmail.com",
            "password": "Avinash@2000",
            "account_number": "2525252525",
            "bank_name": "AXIS",
            "account_type": "Savings",
            "bank_location": "Ambur",
            "has_credit_card": 0,
            "occupation": "IPS",
            "age": 28,
            "location": "Ambur"
        },
        {
            "id": "3333333333",
            "name": "Kumar",
            "user_code": "22243020",
            "email": "kum@gamil.com",
            "password": "Kumar@2000",
            "account_number": "3333333333",
            "bank_name": "Indian",
            "account_type": "Current",
            "bank_location": "Coimbatore",
            "has_credit_card": 0,
            "occupation": "Content Creator",
            "age": 23,
            "location": "Coimbatore"
        },
        {
            "id": "4444444444",
            "name": "Hari",
            "user_code": "22243016",
            "email": "hari@gmail.com",
            "password": "Hari@2000",
            "account_number": "4444444444",
            "bank_name": "Canara",
            "account_type": "Current",
            "bank_location": "Karur",
            "has_credit_card": 1,
            "occupation": "Startup Founder",
            "age": 44,
            "location": "Karur"
        },
        {
            "id": "5555555555",
            "name": "Janakrishnan",
            "user_code": "22243019",
            "email": "jk@gmail.com",
            "password": "Janakrishnan@2000",
            "account_number": "5555555555",
            "bank_name": "SBI",
            "account_type": "Savings",
            "bank_location": "Rasipuram",
            "has_credit_card": 1,
            "occupation": "Government Employee",
            "age": 22,
            "location": "Rasipuram"
        }
    ]
    
    cursor = conn.cursor()
    current_time = datetime.now().isoformat()
    
    for user in users_data:
        password_hash = hash_password(user["password"])
        
        try:
            cursor.execute("""
                INSERT INTO users (
                    id, name, email, password_hash, user_number, occupation, age,
                    location, is_active, is_verified, created_at, updated_at,
                    account_number, bank_name, account_type, bank_location, 
                    has_credit_card, user_code
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                user["id"],
                user["name"],
                user["email"],
                password_hash,
                user["id"],  # user_number same as id
                user["occupation"],
                user["age"],
                user["location"],
                1,  # is_active
                1,  # is_verified
                current_time,
                current_time,
                user["account_number"],
                user["bank_name"],
                user["account_type"],
                user["bank_location"],
                user["has_credit_card"],
                user["user_code"]
            ))
            print(f"✓ Added user: {user['name']} ({user['email']})")
        except sqlite3.IntegrityError as e:
            print(f"✗ Error adding {user['name']}: {e}")
        except Exception as e:
            print(f"✗ Error adding {user['name']}: {e}")
    
    conn.commit()
    print(f"\n✅ Successfully added {len(users_data)} users")


def main():
    """Main function to update users"""
    db_path = "aurexis.db"
    
    # Close any existing connections
    close_connection_pool()
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    
    try:
        print("🔧 Updating database schema...")
        update_database_schema(conn)
        
        print("\n🗑️  Clearing existing users...")
        clear_existing_users(conn)
        
        print("\n👥 Inserting all 12 users with complete data...")
        insert_all_users(conn)
        
        # Verify
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        print(f"\n📊 Total users in database: {count}")
        
        # Show summary
        cursor.execute("SELECT name, email, occupation, location FROM users ORDER BY name")
        print("\n📋 User Summary:")
        print("-" * 60)
        for row in cursor.fetchall():
            print(f"  • {row['name']} | {row['occupation']} | {row['location']}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()
        print("\n✅ Database update completed!")


if __name__ == "__main__":
    main()
