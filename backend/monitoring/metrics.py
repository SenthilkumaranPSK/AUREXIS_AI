"""
Metrics Collection Module

Collects and exposes application metrics for monitoring and observability.
"""

from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from functools import wraps
import time
from typing import Callable, Any
import psutil


# HTTP Metrics
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

http_requests_in_progress = Gauge(
    'http_requests_in_progress',
    'HTTP requests currently in progress',
    ['method', 'endpoint']
)

# Database Metrics
db_queries_total = Counter(
    'db_queries_total',
    'Total database queries',
    ['operation', 'table']
)

db_query_duration_seconds = Histogram(
    'db_query_duration_seconds',
    'Database query duration in seconds',
    ['operation', 'table']
)

db_connections_active = Gauge(
    'db_connections_active',
    'Active database connections'
)

# Cache Metrics
cache_hits_total = Counter(
    'cache_hits_total',
    'Total cache hits'
)

cache_misses_total = Counter(
    'cache_misses_total',
    'Total cache misses'
)

cache_operations_duration_seconds = Histogram(
    'cache_operations_duration_seconds',
    'Cache operation duration in seconds',
    ['operation']
)

# AI/ML Metrics
ml_predictions_total = Counter(
    'ml_predictions_total',
    'Total ML predictions',
    ['model_type']
)

ml_prediction_duration_seconds = Histogram(
    'ml_prediction_duration_seconds',
    'ML prediction duration in seconds',
    ['model_type']
)

chat_requests_total = Counter(
    'chat_requests_total',
    'Total chat requests',
    ['model']
)

chat_request_duration_seconds = Histogram(
    'chat_request_duration_seconds',
    'Chat request duration in seconds',
    ['model']
)

# Agent Metrics
agent_executions_total = Counter(
    'agent_executions_total',
    'Total agent executions',
    ['agent_name', 'status']
)

agent_execution_duration_seconds = Histogram(
    'agent_execution_duration_seconds',
    'Agent execution duration in seconds',
    ['agent_name']
)

# WebSocket Metrics
websocket_connections_active = Gauge(
    'websocket_connections_active',
    'Active WebSocket connections'
)

websocket_messages_total = Counter(
    'websocket_messages_total',
    'Total WebSocket messages',
    ['type', 'direction']
)

# System Metrics
system_cpu_usage_percent = Gauge(
    'system_cpu_usage_percent',
    'System CPU usage percentage'
)

system_memory_usage_bytes = Gauge(
    'system_memory_usage_bytes',
    'System memory usage in bytes'
)

system_memory_available_bytes = Gauge(
    'system_memory_available_bytes',
    'System memory available in bytes'
)

system_disk_usage_bytes = Gauge(
    'system_disk_usage_bytes',
    'System disk usage in bytes'
)

# Error Metrics
errors_total = Counter(
    'errors_total',
    'Total errors',
    ['type', 'endpoint']
)


class MetricsCollector:
    """Metrics collection manager"""
    
    @staticmethod
    def track_http_request(method: str, endpoint: str, status: int, duration: float):
        """Track HTTP request metrics"""
        http_requests_total.labels(method=method, endpoint=endpoint, status=status).inc()
        http_request_duration_seconds.labels(method=method, endpoint=endpoint).observe(duration)
    
    @staticmethod
    def track_db_query(operation: str, table: str, duration: float):
        """Track database query metrics"""
        db_queries_total.labels(operation=operation, table=table).inc()
        db_query_duration_seconds.labels(operation=operation, table=table).observe(duration)
    
    @staticmethod
    def track_cache_hit():
        """Track cache hit"""
        cache_hits_total.inc()
    
    @staticmethod
    def track_cache_miss():
        """Track cache miss"""
        cache_misses_total.inc()
    
    @staticmethod
    def track_cache_operation(operation: str, duration: float):
        """Track cache operation"""
        cache_operations_duration_seconds.labels(operation=operation).observe(duration)
    
    @staticmethod
    def track_ml_prediction(model_type: str, duration: float):
        """Track ML prediction"""
        ml_predictions_total.labels(model_type=model_type).inc()
        ml_prediction_duration_seconds.labels(model_type=model_type).observe(duration)
    
    @staticmethod
    def track_chat_request(model: str, duration: float):
        """Track chat request"""
        chat_requests_total.labels(model=model).inc()
        chat_request_duration_seconds.labels(model=model).observe(duration)
    
    @staticmethod
    def track_agent_execution(agent_name: str, status: str, duration: float):
        """Track agent execution"""
        agent_executions_total.labels(agent_name=agent_name, status=status).inc()
        agent_execution_duration_seconds.labels(agent_name=agent_name).observe(duration)
    
    @staticmethod
    def track_websocket_connection(delta: int):
        """Track WebSocket connection change"""
        websocket_connections_active.inc(delta)
    
    @staticmethod
    def track_websocket_message(msg_type: str, direction: str):
        """Track WebSocket message"""
        websocket_messages_total.labels(type=msg_type, direction=direction).inc()
    
    @staticmethod
    def track_error(error_type: str, endpoint: str):
        """Track error"""
        errors_total.labels(type=error_type, endpoint=endpoint).inc()
    
    @staticmethod
    def update_system_metrics():
        """Update system metrics"""
        try:
            # CPU
            cpu_percent = psutil.cpu_percent(interval=1)
            system_cpu_usage_percent.set(cpu_percent)
            
            # Memory
            memory = psutil.virtual_memory()
            system_memory_usage_bytes.set(memory.used)
            system_memory_available_bytes.set(memory.available)
            
            # Disk
            disk = psutil.disk_usage('/')
            system_disk_usage_bytes.set(disk.used)
        except Exception as e:
            print(f"Error updating system metrics: {e}")


def track_time(metric: Histogram, labels: dict = None):
    """Decorator to track execution time"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(*args, **kwargs) -> Any:
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                return result
            finally:
                duration = time.time() - start_time
                if labels:
                    metric.labels(**labels).observe(duration)
                else:
                    metric.observe(duration)
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs) -> Any:
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                duration = time.time() - start_time
                if labels:
                    metric.labels(**labels).observe(duration)
                else:
                    metric.observe(duration)
        
        # Return appropriate wrapper based on function type
        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator


def get_metrics() -> bytes:
    """Get Prometheus metrics"""
    # Update system metrics before generating output
    MetricsCollector.update_system_metrics()
    
    return generate_latest()


def get_metrics_content_type() -> str:
    """Get metrics content type"""
    return CONTENT_TYPE_LATEST


# Global metrics collector instance
metrics_collector = MetricsCollector()
