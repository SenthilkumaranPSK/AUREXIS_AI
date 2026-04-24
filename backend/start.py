"""
AUREXIS AI Backend Startup Script
Initializes database and starts the server
"""

import sys
import os
from pathlib import Path

# Add backend directory to path
sys.path.insert(0, str(Path(__file__).parent))

def main():
    print("\n" + "=" * 60)
    print("🚀 AUREXIS AI Backend - Starting Up")
    print("=" * 60 + "\n")
    
    # Step 1: Initialize Database
    print("📊 Step 1: Initializing Database...")
    try:
        from database.connection import init_database
        init_database()
        print("✅ Database initialized successfully\n")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        print("⚠️  Continuing anyway (database might already exist)\n")
    
    # Step 2: Verify Routes
    print("🔧 Step 2: Verifying Routes...")
    try:
        from routes import (
            auth_router,
            financial_router,
            forecast_router,
            chat_router,
            reports_router
        )
        print("✅ All route modules loaded successfully\n")
    except Exception as e:
        print(f"❌ Route loading failed: {e}")
        print("Please check that all route files exist\n")
        return
    
    # Step 3: Start Server
    print("🌐 Step 3: Starting FastAPI Server...")
    print("=" * 60)
    print()
    
    try:
        import uvicorn
        uvicorn.run(
            "server:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server failed to start: {e}")

if __name__ == "__main__":
    main()
