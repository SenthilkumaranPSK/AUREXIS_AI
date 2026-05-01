"""
Automated Database Backup Script

Run this script to backup the database.
Can be scheduled with cron (Linux) or Task Scheduler (Windows).
"""

import shutil
import os
from datetime import datetime
from pathlib import Path

# Configuration
DB_FILE = Path(__file__).parent / "aurexis.db"
BACKUP_DIR = Path(__file__).parent / "backups"
MAX_BACKUPS = 30  # Keep last 30 backups

def create_backup():
    """Create a database backup"""
    
    # Create backup directory if it doesn't exist
    BACKUP_DIR.mkdir(exist_ok=True)
    
    # Generate backup filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = BACKUP_DIR / f"aurexis_backup_{timestamp}.db"
    
    try:
        # Copy database file
        shutil.copy2(DB_FILE, backup_file)
        print(f"✅ Backup created: {backup_file}")
        
        # Clean old backups
        cleanup_old_backups()
        
        return True
    except Exception as e:
        print(f"❌ Backup failed: {e}")
        return False


def cleanup_old_backups():
    """Remove old backups, keep only MAX_BACKUPS most recent"""
    
    # Get all backup files
    backups = sorted(BACKUP_DIR.glob("aurexis_backup_*.db"))
    
    # Remove old backups if we have more than MAX_BACKUPS
    if len(backups) > MAX_BACKUPS:
        old_backups = backups[:-MAX_BACKUPS]
        for backup in old_backups:
            try:
                backup.unlink()
                print(f"🗑️  Removed old backup: {backup.name}")
            except Exception as e:
                print(f"⚠️  Could not remove {backup.name}: {e}")


def list_backups():
    """List all available backups"""
    backups = sorted(BACKUP_DIR.glob("aurexis_backup_*.db"), reverse=True)
    
    if not backups:
        print("No backups found")
        return
    
    print(f"\n📦 Available backups ({len(backups)}):")
    for i, backup in enumerate(backups, 1):
        size = backup.stat().st_size / 1024 / 1024  # MB
        mtime = datetime.fromtimestamp(backup.stat().st_mtime)
        print(f"  {i}. {backup.name} ({size:.2f} MB) - {mtime.strftime('%Y-%m-%d %H:%M:%S')}")


def restore_backup(backup_file: str):
    """Restore database from backup"""
    
    backup_path = BACKUP_DIR / backup_file
    
    if not backup_path.exists():
        print(f"❌ Backup file not found: {backup_file}")
        return False
    
    try:
        # Create a backup of current database before restoring
        current_backup = BACKUP_DIR / f"aurexis_before_restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        shutil.copy2(DB_FILE, current_backup)
        print(f"📦 Current database backed up to: {current_backup.name}")
        
        # Restore from backup
        shutil.copy2(backup_path, DB_FILE)
        print(f"✅ Database restored from: {backup_file}")
        
        return True
    except Exception as e:
        print(f"❌ Restore failed: {e}")
        return False


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "backup":
            create_backup()
        elif command == "list":
            list_backups()
        elif command == "restore" and len(sys.argv) > 2:
            restore_backup(sys.argv[2])
        else:
            print("Usage:")
            print("  python backup_database.py backup          - Create a backup")
            print("  python backup_database.py list            - List all backups")
            print("  python backup_database.py restore <file>  - Restore from backup")
    else:
        # Default: create backup
        create_backup()
