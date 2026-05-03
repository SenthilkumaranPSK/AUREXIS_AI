"""
Automated Backup System for User Data
"""
import os
import json
import shutil
import zipfile
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
import logging
import asyncio

logger = logging.getLogger(__name__)


class BackupManager:
    """Manage automated backups of user data"""
    
    def __init__(self, data_dir: str = "./backend/user_data", backup_dir: str = "./backups"):
        self.data_dir = Path(data_dir)
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    async def create_backup(self, backup_name: Optional[str] = None) -> str:
        """
        Create a full backup of all user data
        
        Returns:
            Path to created backup file
        """
        if not backup_name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"aurexis_backup_{timestamp}"
        
        backup_path = self.backup_dir / f"{backup_name}.zip"
        
        try:
            logger.info(f"Creating backup: {backup_path}")
            
            with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Backup all user data
                for user_dir in self.data_dir.iterdir():
                    if user_dir.is_dir():
                        for file_path in user_dir.rglob('*.json'):
                            arcname = file_path.relative_to(self.data_dir.parent)
                            zipf.write(file_path, arcname)
                
                # Add metadata
                metadata = {
                    "backup_name": backup_name,
                    "created_at": datetime.now().isoformat(),
                    "version": "2.0.0",
                    "user_count": len(list(self.data_dir.iterdir()))
                }
                zipf.writestr("backup_metadata.json", json.dumps(metadata, indent=2))
            
            logger.info(f"Backup created successfully: {backup_path}")
            return str(backup_path)
            
        except Exception as e:
            logger.error(f"Backup failed: {e}")
            if backup_path.exists():
                backup_path.unlink()
            raise
    
    async def restore_backup(self, backup_path: str, overwrite: bool = False) -> bool:
        """
        Restore data from backup
        
        Args:
            backup_path: Path to backup zip file
            overwrite: Whether to overwrite existing data
            
        Returns:
            True if successful
        """
        backup_file = Path(backup_path)
        
        if not backup_file.exists():
            raise FileNotFoundError(f"Backup file not found: {backup_path}")
        
        try:
            logger.info(f"Restoring backup: {backup_path}")
            
            # Create temporary restore directory
            temp_dir = self.backup_dir / "temp_restore"
            temp_dir.mkdir(exist_ok=True)
            
            # Extract backup
            with zipfile.ZipFile(backup_file, 'r') as zipf:
                zipf.extractall(temp_dir)
            
            # Read metadata
            metadata_path = temp_dir / "backup_metadata.json"
            if metadata_path.exists():
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)
                logger.info(f"Restoring backup from {metadata['created_at']}")
            
            # Restore user data
            user_data_path = temp_dir / "backend" / "user_data"
            if user_data_path.exists():
                if overwrite:
                    # Backup current data before overwriting
                    await self.create_backup(f"pre_restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
                    
                    # Remove existing data
                    if self.data_dir.exists():
                        shutil.rmtree(self.data_dir)
                
                # Copy restored data
                shutil.copytree(user_data_path, self.data_dir, dirs_exist_ok=not overwrite)
            
            # Cleanup temp directory
            shutil.rmtree(temp_dir)
            
            logger.info("Backup restored successfully")
            return True
            
        except Exception as e:
            logger.error(f"Restore failed: {e}")
            raise
    
    async def list_backups(self) -> List[Dict]:
        """
        List all available backups
        
        Returns:
            List of backup information dictionaries
        """
        backups = []
        
        for backup_file in self.backup_dir.glob("*.zip"):
            try:
                stat = backup_file.stat()
                
                # Try to read metadata
                metadata = {}
                try:
                    with zipfile.ZipFile(backup_file, 'r') as zipf:
                        if "backup_metadata.json" in zipf.namelist():
                            metadata = json.loads(zipf.read("backup_metadata.json"))
                except:
                    pass
                
                backups.append({
                    "name": backup_file.stem,
                    "path": str(backup_file),
                    "size": stat.st_size,
                    "size_mb": round(stat.st_size / (1024 * 1024), 2),
                    "created_at": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                    "metadata": metadata
                })
            except Exception as e:
                logger.warning(f"Error reading backup {backup_file}: {e}")
        
        return sorted(backups, key=lambda x: x["created_at"], reverse=True)
    
    async def delete_backup(self, backup_name: str) -> bool:
        """Delete a specific backup"""
        backup_path = self.backup_dir / f"{backup_name}.zip"
        
        if not backup_path.exists():
            raise FileNotFoundError(f"Backup not found: {backup_name}")
        
        try:
            backup_path.unlink()
            logger.info(f"Deleted backup: {backup_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete backup: {e}")
            raise
    
    async def cleanup_old_backups(self, retention_days: int = 30) -> int:
        """
        Delete backups older than retention period
        
        Args:
            retention_days: Number of days to keep backups
            
        Returns:
            Number of backups deleted
        """
        cutoff_date = datetime.now() - timedelta(days=retention_days)
        deleted_count = 0
        
        for backup_file in self.backup_dir.glob("*.zip"):
            try:
                created_at = datetime.fromtimestamp(backup_file.stat().st_ctime)
                
                if created_at < cutoff_date:
                    backup_file.unlink()
                    deleted_count += 1
                    logger.info(f"Deleted old backup: {backup_file.name}")
            except Exception as e:
                logger.warning(f"Error deleting backup {backup_file}: {e}")
        
        logger.info(f"Cleaned up {deleted_count} old backups")
        return deleted_count
    
    async def verify_backup(self, backup_path: str) -> Dict:
        """
        Verify backup integrity
        
        Returns:
            Verification results dictionary
        """
        backup_file = Path(backup_path)
        
        if not backup_file.exists():
            return {"valid": False, "error": "Backup file not found"}
        
        try:
            with zipfile.ZipFile(backup_file, 'r') as zipf:
                # Test zip integrity
                bad_file = zipf.testzip()
                if bad_file:
                    return {"valid": False, "error": f"Corrupted file: {bad_file}"}
                
                # Check for metadata
                has_metadata = "backup_metadata.json" in zipf.namelist()
                
                # Count files
                file_count = len(zipf.namelist())
                
                return {
                    "valid": True,
                    "has_metadata": has_metadata,
                    "file_count": file_count,
                    "size_mb": round(backup_file.stat().st_size / (1024 * 1024), 2)
                }
        except Exception as e:
            return {"valid": False, "error": str(e)}


# Background backup task
class BackupScheduler:
    """Schedule automated backups"""
    
    def __init__(self, backup_manager: BackupManager, interval_hours: int = 24):
        self.backup_manager = backup_manager
        self.interval_hours = interval_hours
        self.running = False
        self.task = None
    
    async def start(self):
        """Start automated backup schedule"""
        if self.running:
            logger.warning("Backup scheduler already running")
            return
        
        self.running = True
        self.task = asyncio.create_task(self._backup_loop())
        logger.info(f"Backup scheduler started (interval: {self.interval_hours}h)")
    
    async def stop(self):
        """Stop automated backup schedule"""
        self.running = False
        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
        logger.info("Backup scheduler stopped")
    
    async def _backup_loop(self):
        """Background backup loop"""
        while self.running:
            try:
                # Create backup
                await self.backup_manager.create_backup()
                
                # Cleanup old backups
                from config_manager import get_settings
                settings = get_settings()
                await self.backup_manager.cleanup_old_backups(settings.backup_retention_days)
                
                # Wait for next interval
                await asyncio.sleep(self.interval_hours * 3600)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Backup loop error: {e}")
                await asyncio.sleep(300)  # Wait 5 minutes on error


# Global backup manager instance
_backup_manager: Optional[BackupManager] = None
_backup_scheduler: Optional[BackupScheduler] = None


def get_backup_manager() -> BackupManager:
    """Get global backup manager instance"""
    global _backup_manager
    if _backup_manager is None:
        from config_manager import get_settings
        settings = get_settings()
        _backup_manager = BackupManager(backup_dir=settings.backup_dir)
    return _backup_manager


async def start_backup_scheduler():
    """Start automated backup scheduler"""
    global _backup_scheduler
    
    from config_manager import get_settings
    settings = get_settings()
    
    if not settings.backup_enabled:
        logger.info("Automated backups disabled")
        return
    
    if _backup_scheduler is None:
        backup_manager = get_backup_manager()
        _backup_scheduler = BackupScheduler(
            backup_manager,
            interval_hours=settings.auto_backup_interval_hours
        )
    
    await _backup_scheduler.start()


async def stop_backup_scheduler():
    """Stop automated backup scheduler"""
    global _backup_scheduler
    if _backup_scheduler:
        await _backup_scheduler.stop()
