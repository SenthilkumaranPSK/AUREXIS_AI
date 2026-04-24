"""
Health Check Module

Provides comprehensive health check functionality for monitoring system status.
"""

import psutil
import time
from datetime import datetime
from typing import Dict, Any
import sys
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from database.connection import SessionLocal, engine
from config import settings


class HealthChecker:
    """Health check manager"""
    
    def __init__(self):
        self.start_time = time.time()
    
    def check_database(self) -> Dict[str, Any]:
        """Check database connectivity"""
        try:
            db = SessionLocal()
            # Try a simple query
            db.execute("SELECT 1")
            db.close()
            
            return {
                "status": "healthy",
                "message": "Database connection successful",
                "response_time_ms": 0
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "message": f"Database connection failed: {str(e)}",
                "error": str(e)
            }
    
    def check_redis(self) -> Dict[str, Any]:
        """Check Redis connectivity"""
        try:
            # Import here to avoid circular dependency
            from cache import cache
            
            if cache.redis_client:
                cache.redis_client.ping()
                return {
                    "status": "healthy",
                    "message": "Redis connection successful"
                }
            else:
                return {
                    "status": "degraded",
                    "message": "Redis not configured, using in-memory cache"
                }
        except Exception as e:
            return {
                "status": "degraded",
                "message": f"Redis unavailable: {str(e)}, using in-memory cache"
            }
    
    def check_ollama(self) -> Dict[str, Any]:
        """Check Ollama service"""
        try:
            import requests
            
            ollama_url = settings.OLLAMA_BASE_URL
            response = requests.get(f"{ollama_url}/api/tags", timeout=5)
            
            if response.status_code == 200:
                return {
                    "status": "healthy",
                    "message": "Ollama service available",
                    "model": settings.OLLAMA_MODEL
                }
            else:
                return {
                    "status": "unhealthy",
                    "message": f"Ollama service returned status {response.status_code}"
                }
        except Exception as e:
            return {
                "status": "unhealthy",
                "message": f"Ollama service unavailable: {str(e)}"
            }
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """Get system resource metrics"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return {
                "cpu": {
                    "usage_percent": cpu_percent,
                    "count": psutil.cpu_count()
                },
                "memory": {
                    "total_gb": round(memory.total / (1024**3), 2),
                    "used_gb": round(memory.used / (1024**3), 2),
                    "available_gb": round(memory.available / (1024**3), 2),
                    "usage_percent": memory.percent
                },
                "disk": {
                    "total_gb": round(disk.total / (1024**3), 2),
                    "used_gb": round(disk.used / (1024**3), 2),
                    "free_gb": round(disk.free / (1024**3), 2),
                    "usage_percent": disk.percent
                }
            }
        except Exception as e:
            return {
                "error": f"Failed to get system metrics: {str(e)}"
            }
    
    def get_uptime(self) -> Dict[str, Any]:
        """Get application uptime"""
        uptime_seconds = time.time() - self.start_time
        
        days = int(uptime_seconds // 86400)
        hours = int((uptime_seconds % 86400) // 3600)
        minutes = int((uptime_seconds % 3600) // 60)
        seconds = int(uptime_seconds % 60)
        
        return {
            "uptime_seconds": int(uptime_seconds),
            "uptime_formatted": f"{days}d {hours}h {minutes}m {seconds}s",
            "started_at": datetime.fromtimestamp(self.start_time).isoformat()
        }
    
    def get_comprehensive_health(self) -> Dict[str, Any]:
        """Get comprehensive health status"""
        database_health = self.check_database()
        redis_health = self.check_redis()
        ollama_health = self.check_ollama()
        system_metrics = self.get_system_metrics()
        uptime = self.get_uptime()
        
        # Determine overall status
        statuses = [
            database_health["status"],
            redis_health["status"],
            ollama_health["status"]
        ]
        
        if all(s == "healthy" for s in statuses):
            overall_status = "healthy"
        elif any(s == "unhealthy" for s in statuses):
            overall_status = "unhealthy"
        else:
            overall_status = "degraded"
        
        return {
            "status": overall_status,
            "timestamp": datetime.now().isoformat(),
            "version": settings.APP_VERSION,
            "environment": settings.ENVIRONMENT,
            "uptime": uptime,
            "components": {
                "database": database_health,
                "redis": redis_health,
                "ollama": ollama_health
            },
            "system": system_metrics
        }
    
    def get_readiness(self) -> Dict[str, Any]:
        """Check if application is ready to serve requests"""
        database_health = self.check_database()
        
        is_ready = database_health["status"] == "healthy"
        
        return {
            "ready": is_ready,
            "timestamp": datetime.now().isoformat(),
            "checks": {
                "database": database_health
            }
        }
    
    def get_liveness(self) -> Dict[str, Any]:
        """Check if application is alive"""
        return {
            "alive": True,
            "timestamp": datetime.now().isoformat()
        }


# Global health checker instance
health_checker = HealthChecker()


def get_health_status() -> Dict[str, Any]:
    """Get comprehensive health status"""
    return health_checker.get_comprehensive_health()


def get_readiness_status() -> Dict[str, Any]:
    """Get readiness status"""
    return health_checker.get_readiness()


def get_liveness_status() -> Dict[str, Any]:
    """Get liveness status"""
    return health_checker.get_liveness()
