"""
Database Migration for Chat Memory
Adds conversations table to store chat history
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from database_legacy import engine, Base, SessionLocal
from chat_memory import Conversation
from logger import logger


def migrate_chat_memory():
    """Create conversations table"""
    
    logger.info("=" * 60)
    logger.info("AUREXIS AI - Chat Memory Migration")
    logger.info("=" * 60)
    
    try:
        # Create conversations table
        logger.info("Creating conversations table...")
        Conversation.__table__.create(engine, checkfirst=True)
        logger.info("✓ Conversations table created")
        
        # Verify table exists
        db = SessionLocal()
        try:
            count = db.query(Conversation).count()
            logger.info(f"✓ Table verified - {count} conversations")
        finally:
            db.close()
        
        logger.info("=" * 60)
        logger.info("✅ Chat Memory Migration completed successfully!")
        logger.info("=" * 60)
        logger.info("You can now use the chat memory features:")
        logger.info("- Persistent conversation history")
        logger.info("- Context-aware responses")
        logger.info("- User preferences tracking")
        logger.info("- Session management")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = migrate_chat_memory()
    sys.exit(0 if success else 1)
