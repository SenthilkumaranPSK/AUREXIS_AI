"""
Initialize AUREXIS AI Database
Run this once to create all tables
"""

from database.connection import init_database

if __name__ == "__main__":
    print("🔧 Initializing AUREXIS AI database...")
    print("=" * 50)
    
    try:
        init_database()
        
        print("\n✅ Database initialized successfully!")
        print("\n📊 Tables created:")
        print("   1. users - User accounts")
        print("   2. monthly_income - Income records")
        print("   3. expenses - Expense transactions")
        print("   4. goals - Financial goals")
        print("   5. alerts - User alerts")
        print("   6. recommendations - Financial recommendations")
        print("   7. chat_sessions - Chat sessions")
        print("   8. chat_messages - Chat message history")
        print("   9. health_history - Financial health score history")
        print("   10. reports - Generated reports")
        print("   11. refresh_tokens - JWT token management")
        
        print("\n" + "=" * 50)
        print("✅ Ready to start server!")
        print("   Run: python server.py")
        
    except Exception as e:
        print(f"\n❌ Error initializing database: {e}")
        import traceback
        traceback.print_exc()
