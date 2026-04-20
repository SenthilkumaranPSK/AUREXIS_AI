"""
AUREXIS AI — Database Migration Script
Initialize database and migrate legacy users
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from database import init_db, drop_db
from user_manager_v2 import migrate_legacy_users_to_db
from logger import logger
from config import settings


def run_migrations(reset: bool = False):
    """
    Run database migrations
    
    Args:
        reset: If True, drop all tables before creating (DESTRUCTIVE!)
    """
    logger.info("=" * 60)
    logger.info("AUREXIS AI - Database Migration")
    logger.info("=" * 60)
    
    if reset:
        logger.warning("⚠️  RESET MODE: All existing data will be lost!")
        confirm = input("Type 'YES' to confirm: ")
        if confirm != "YES":
            logger.info("Migration cancelled")
            return
        
        logger.info("Dropping all tables...")
        drop_db()
        logger.info("✓ Tables dropped")
    
    # Create tables
    logger.info("Creating database tables...")
    init_db()
    logger.info("✓ Tables created")
    
    # Migrate legacy users
    logger.info("Migrating legacy users...")
    migrate_legacy_users_to_db()
    logger.info("✓ Users migrated")
    
    logger.info("=" * 60)
    logger.info("✅ Migration completed successfully!")
    logger.info("=" * 60)
    logger.info(f"Database: {settings.DATABASE_URL}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="AUREXIS AI Database Migration")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Reset database (drop all tables before creating)"
    )
    
    args = parser.parse_args()
    
    try:
        run_migrations(reset=args.reset)
    except Exception as e:
        logger.exception(f"Migration failed: {e}")
        sys.exit(1)
