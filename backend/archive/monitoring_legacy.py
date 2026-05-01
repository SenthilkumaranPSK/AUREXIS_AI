"""
AUREXIS AI — Monitoring & Metrics
Prometheus metrics and health checks
"""

from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response
from typing import Dict, Any
import psutil
import time
from datetime import datetime, timezone

from config import settings
from logger import logger


# ── Prometheus Metrics ─────────────────────────────────────────────────────

# Request metrics
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

# Application metrics
active_users = Gauge(
    'active_users_total',
    'Number of active users'
)

chat_requests_total = Counter(
    'chat_requests_total',
    'Total chat requests',
    ['user_id', 'model']
)

chat_response_duration_seconds = Histogram(
    'chat_response_duration_seconds',
    'Chat response duration in seconds',
    ['model']
)

ml_forecast_requests_total = Counter(
    'ml_forecast_requests_total',
    'Total ML forecast requests',
    ['model_type']
)

ml_forecast_duration_seconds = Histogram(
    'ml_forecast_duration_seconds',
    'ML forecast computation duration',
    ['model_type']
)

# Cache metrics
cache_hits_total = Counter(
    'cache_hits_total',
    'Total cache hits',
    ['cache_type']
)

cache_misses_total = Counter(
    'cache_misses_total',
    'Total cache misses',
    ['cache_type']
)

# Database metrics
db_queries_total = Counter(
    'db_queries_total',
    'Total database queries',
    ['operation']
)

db_query_duration_seconds = Histogram(
    'db_query_duration_seconds',
    'Database query duration',
    ['operation']
)

# Error metrics
errors_total = Counter(
    'errors_total',
    'Total errors',
    ['error_type', 'endpoint']
)

# System metrics
system_cpu_usage = Gauge(
    'system_cpu_usage_percent',
    'System CPU usage percentage'
)

system_memory_usage = Gauge(
    'system_memory_usage_percent',
    'System memory usage percentage'
)

system_disk_usage = Gauge(
    'system_disk_usage_percent',
    'System disk usage percentage'
)


# ── Metrics Collection ─────────────────────────────────────────────────────

def collect_system_metrics():
    """Collect system resource metrics"""
    try:
        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        system_cpu_usage.set(cpu_percent)
        
        # Memory usage
        memory = psutil.virtual_memory()
        system_memory_usage.set(memory.percent)
        
        # Disk usage
        disk = psutil.disk_usage('/')
        system_disk_usage.set(disk.percent)
        
    except Exception as e:
        logger.error(f"Error collecting system metrics: {e}")


def record_request_metrics(method: str, endpoint: str, status: int, duration: float):
    """Record HTTP request metrics"""
    http_requests_total.labels(method=method, endpoint=endpoint, status=status).inc()
    http_request_duration_seconds.labels(method=method, endpoint=endpoint).observe(duration)


def record_chat_metrics(user_id: str, model: str, duration: float):
    """Record chat request metrics"""
    chat_requests_total.labels(user_id=user_id, model=model).inc()
    chat_response_duration_seconds.labels(model=model).observe(duration)


def record_ml_metrics(model_type: str, duration: float):
    """Record ML forecast metrics"""
    ml_forecast_requests_total.labels(model_type=model_type).inc()
    ml_forecast_duration_seconds.labels(model_type=model_type).observe(duration)


def record_cache_hit(cache_type: str = "redis"):
    """Record cache hit"""
    cache_hits_total.labels(cache_type=cache_type).inc()


def record_cache_miss(cache_type: str = "redis"):
    """Record cache miss"""
    cache_misses_total.labels(cache_type=cache_type).inc()


def record_error(error_type: str, endpoint: str):
    """Record error"""
    errors_total.labels(error_type=error_type, endpoint=endpoint).inc()


# ── Health Checks ──────────────────────────────────────────────────────────

async def check_database_health() -> Dict[str, Any]:
    """Check database connectivity"""
    try:
        from database import SessionLocal
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        return {"status": "healthy", "message": "Database connection OK"}
    except Exception as e:
        return {"status": "unhealthy", "message": f"Database error: {str(e)}"}


async def check_redis_health() -> Dict[str, Any]:
    """Check Redis connectivity"""
    try:
        from cache import cache
        cache.backend.client.ping()
        return {"status": "healthy", "message": "Redis connection OK"}
    except Exception as e:
        return {"status": "unhealthy", "message": f"Redis error: {str(e)}"}


async def check_ollama_health() -> Dict[str, Any]:
    """Check Ollama service"""
    try:
        import httpx
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{settings.OLLAMA_BASE_URL}/api/tags")
            if response.status_code == 200:
                return {"status": "healthy", "message": "Ollama service OK"}
            else:
                return {"status": "unhealthy", "message": f"Ollama returned {response.status_code}"}
    except Exception as e:
        return {"status": "unhealthy", "message": f"Ollama error: {str(e)}"}


async def get_health_status() -> Dict[str, Any]:
    """Get comprehensive health status"""
    
    # Collect system metrics
    collect_system_metrics()
    
    # Check components
    db_health = await check_database_health()
    redis_health = await check_redis_health()
    ollama_health = await check_ollama_health()
    
    # Overall status
    all_healthy = all(
        check["status"] == "healthy"
        for check in [db_health, redis_health, ollama_health]
    )
    
    return {
        "status": "healthy" if all_healthy else "degraded",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "components": {
            "database": db_health,
            "redis": redis_health,
            "ollama": ollama_health,
        },
        "system": {
            "cpu_percent": psutil.cpu_percent(),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage('/').percent,
        }
    }


# ── Metrics Endpoint ───────────────────────────────────────────────────────

async def metrics_endpoint() -> Response:
    """Prometheus metrics endpoint"""
    if not settings.METRICS_ENABLED:
        return Response(content="Metrics disabled", status_code=404)
    
    # Collect latest system metrics
    collect_system_metrics()
    
    # Generate Prometheus format
    metrics_output = generate_latest()
    
    return Response(
        content=metrics_output,
        media_type=CONTENT_TYPE_LATEST
    )


# ── Performance Monitoring ─────────────────────────────────────────────────

class PerformanceMonitor:
    """Context manager for monitoring operation performance"""
    
    def __init__(self, operation_name: str):
        self.operation_name = operation_name
        self.start_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = time.time() - self.start_time
        
        if exc_type is not None:
            # Operation failed
            logger.error(f"{self.operation_name} failed after {duration:.2f}s: {exc_val}")
            record_error(error_type=exc_type.__name__, endpoint=self.operation_name)
        else:
            # Operation succeeded
            logger.debug(f"{self.operation_name} completed in {duration:.2f}s")
        
        return False  # Don't suppress exceptions


# ── Usage Examples ─────────────────────────────────────────────────────────

"""
# In your endpoints:

from monitoring_legacy import record_request_metrics, record_chat_metrics, PerformanceMonitor

@app.get("/api/user/{user_id}/metrics")
async def get_metrics(user_id: str):
    with PerformanceMonitor("get_metrics"):
        # Your logic here
        result = compute_metrics(user_id)
        return result

@app.post("/api/chat")
async def chat(request: ChatMessage):
    start_time = time.time()
    
    response = await call_ollama(...)
    
    duration = time.time() - start_time
    record_chat_metrics(
        user_id=request.user_id,
        model=settings.OLLAMA_MODEL,
        duration=duration
    )
    
    return response
"""
