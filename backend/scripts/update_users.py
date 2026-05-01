"""
Update users with the new user data provided
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from user_manager_secure import UserManager
from database.db_utils import get_db
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def update_users():
    """Update database with new user data"""
    
    # New user data from the provided table
    new_users = [
        {
            "id": "22243045",
            "name": "Senthilkumaran", 
            "user_number": "22243045",
            "email": "sk@gmail.com",
            "password": "Senthilkumaran@123",
            "occupation": "Software Engineer",
            "age": 24,
            "location": "Salem"
        },
        {
            "id": "22243017",
            "name": "Imayavarman",
            "user_number": "22243017", 
            "email": "imi@gmail.com",
            "password": "Imayavarman@123",
            "occupation": "Doctor",
            "age": 32,
            "location": "Erode"
        },
        {
            "id": "22243050",
            "name": "Srivarshan",
            "user_number": "22243050",
            "email": "sri@gmail.com", 
            "password": "Srivarshan@123",
            "occupation": "Business Owner",
            "age": 40,
            "location": "Theni"
        },
        {
            "id": "22243040",
            "name": "Rahulprasath",
            "user_number": "22243040",
            "email": "rp@gmail.com",
            "password": "Rahulprasath@123", 
            "occupation": "Teacher",
            "age": 30,
            "location": "Omalur"
        },
        {
            "id": "22243055",
            "name": "Magudesh",
            "user_number": "22243055",
            "email": "magu@gmail.com",
            "password": "Magudesh@123",
            "occupation": "Freelancer", 
            "age": 28,
            "location": "Bangalore"
        },
        {
            "id": "22243009",
            "name": "Deepak",
            "user_number": "22243009",
            "email": "dee@gmail.com",
            "password": "Deepak@123",
            "occupation": "CA",
            "age": 29,
            "location": "Chennai"
        },
        {
            "id": "22243060", 
            "name": "Mani",
            "user_number": "22243060",
            "email": "mani@gmail.com",
            "password": "Mani@123",
            "occupation": "Government Employee",
            "age": 38,
            "location": "Edapadi"
        },
        {
            "id": "22243012",
            "name": "Dineshkumar",
            "user_number": "22243012", 
            "email": "dk@gmail.com",
            "password": "Dineshkumar@123",
            "occupation": "Lawyer",
            "age": 52,
            "location": "Sangagari"
        },
        {
            "id": "22243007",
            "name": "Avinash",
            "user_number": "22243007",
            "email": "avi@gmail.com",
            "password": "Avinash@123",
            "occupation": "IPS",
            "age": 28,
            "location": "Ambur"
        },
        {
            "id": "22243020",
            "name": "Kumar", 
            "user_number": "22243020",
            "email": "kum@gmail.com",
            "password": "Kumar@123",
            "occupation": "Content Creator",
            "age": 23,
            "location": "Coimbatore"
        },
        {
            "id": "22243016",
            "name": "Hari",
            "user_number": "22243016",
            "email": "hari@gmail.com",
            "password": "Hari@123", 
            "occupation": "Startup Founder",
            "age": 44,
            "location": "Karur"
        },
        {
            "id": "22243019",
            "name": "Janakrishnan",
            "user_number": "22243019",
            "email": "jk@gmail.com",
            "password": "Janakrishnan@123",
            "occupation": "Government Employee",
            "age": 22,
            "location": "Rasipuram"
        }
    ]
    
    try:
        # First, clear existing users
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users")
            conn.commit()
            logger.info("Cleared existing users")
        
        # Add new users
        created_count = 0
        for user_data in new_users:
            try:
                UserManager.create_user(user_data)
                created_count += 1
                logger.info(f"Created user: {user_data['name']} ({user_data['email']})")
            except Exception as e:
                logger.error(f"Failed to create user {user_data['name']}: {e}")
        
        logger.info(f"Successfully created {created_count} users")
        
        # Verify users were created
        users = UserManager.get_all_users()
        logger.info(f"Total users in database: {len(users)}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error updating users: {e}")
        return False

if __name__ == "__main__":
    print("🔄 Updating users...")
    print("=" * 50)
    
    if update_users():
        print("\n✅ Users updated successfully!")
        print("\n📊 New user credentials:")
        print("   Username formats: name, email, or user_number")
        print("   Password format: [Name]@123")
        print("\n🔐 Example logins:")
        print("   - Senthilkumaran / Senthilkumaran@123")
        print("   - sk@gmail.com / Senthilkumaran@123") 
        print("   - 22243045 / Senthilkumaran@123")
        print("\n" + "=" * 50)
    else:
        print("\n❌ Failed to update users")