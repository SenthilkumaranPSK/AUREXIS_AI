"""
AUREXIS AI - JSON-Based Server (No Database Required)
Simplified server that reads all data from JSON files
"""

import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the main server
from server import app
import uvicorn

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 AUREXIS AI - JSON-Based Financial Intelligence Platform")
    print("=" * 60)
    print("✅ No database required - Reading from JSON files")
    print("📁 User data location: backend/user_data/")
    print("🌐 Server starting on: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("=" * 60)
    print("\n👤 Test Users (Login with user_id or name):")
    print("   - 22243045 / Senthilkumaran : Senthilkumaran@2000")
    print("   - 22243017 / Imayavarman    : Imayavarman@2000")
    print("   - 22243050 / Srivarshan     : Srivarshan@2000")
    print("=" * 60)
    print()
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
