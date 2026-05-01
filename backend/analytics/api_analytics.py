"""
API Analytics and Usage Tracking for AUREXIS AI
Comprehensive monitoring of API usage, performance, and user behavior
"""

import time
import uuid
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from collections import defaultdict, deque
from fastapi import Request, Response
import logging
import asyncio
from contextlib import asynccontextmanager

from database.connection_enhanced import DatabaseManager, get_async_db
from exceptions import DatabaseError
from config_enhanced import settings

logger = logging.getLogger(__name__)


@dataclass
class APIRequest:
    """API request data structure"""
    request_id: str
    timestamp: datetime
    method: str
    path: str
    query_params: Dict[str, Any]
    user_id: Optional[str]
    session_id: Optional[str]
    ip_address: str
    user_agent: str
    response_status: Optional[int] = None
    response_time_ms: Optional[float] = None
    error_code: Optional[str] = None
    endpoint_category: Optional[str] = None


@dataclass
class APIUsageMetrics:
    """API usage metrics"""
    total_requests: int
    requests_per_minute: float
    requests_per_hour: float
    requests_per_day: float
    error_rate: float
    avg_response_time: float
    top_endpoints: List[Dict[str, Any]]
    top_users: List[Dict[str, Any]]
    status_codes: Dict[int, int]
    error_codes: Dict[str, int]


class APIAnalytics:
    """Main API analytics class"""
    
    def __init__(self):
        # In-memory storage for recent requests (circular buffer)
        self.recent_requests: deque = deque(maxlen=10000)
        self.request_counts: defaultdict = defaultdict(int)
        self.error_counts: defaultdict = defaultdict(int)
        self.response_times: deque = deque(maxlen=1000)
        self.user_requests: defaultdict = defaultdict(int)
        self.endpoint_requests: defaultdict = defaultdict(int)
        
        # Performance metrics
        self.start_time = datetime.now()
        self.total_requests = 0
        self.total_errors = 0
        
        # Rate limiting data
        self.rate_limits: Dict[str, List[datetime]] = defaultdict(list)
        
        # Background task for periodic cleanup
        self.cleanup_task: Optional[asyncio.Task] = None
    
    async def start_background_tasks(self):
        """Start background analytics tasks"""
        if not self.cleanup_task:
            self.cleanup_task = asyncio.create_task(self.periodic_cleanup())
    
    async def stop_background_tasks(self):
        """Stop background analytics tasks"""
        if self.cleanup_task:
            self.cleanup_task.cancel()
            try:
                await self.cleanup_task
            except asyncio.CancelledError:
                pass
    
    @asynccontextmanager
    async def track_request(self, request: Request):
        """Context manager for tracking API requests"""
        start_time = time.time()
        request_id = str(uuid.uuid4())
        
        # Extract request information
        request_data = APIRequest(
            request_id=request_id,
            timestamp=datetime.now(),
            method=request.method,
            path=request.url.path,
            query_params=dict(request.query_params),
            user_id=self._extract_user_id(request),
            session_id=self._extract_session_id(request),
            ip_address=self._get_client_ip(request),
            user_agent=request.headers.get("user-agent", ""),
            endpoint_category=self._categorize_endpoint(request.url.path)
        )
        
        try:
            yield request_data
            
            # Record successful request
            response_time = (time.time() - start_time) * 1000
            request_data.response_time_ms = response_time
            
            await self.record_request(request_data)
            
        except Exception as e:
            # Record error
            request_data.error_code = getattr(e, 'error_code', 'INTERNAL_ERROR')
            request_data.response_time_ms = (time.time() - start_time) * 1000
            
            await self.record_request(request_data)
            raise
    
    async def record_request(self, request_data: APIRequest):
        """Record API request data"""
        try:
            # Update in-memory metrics
            self.recent_requests.append(request_data)
            self.request_counts[request_data.path] += 1
            self.user_requests[request_data.user_id or "anonymous"] += 1
            self.endpoint_requests[request_data.endpoint_category or "other"] += 1
            
            if request_data.response_time_ms:
                self.response_times.append(request_data.response_time_ms)
            
            self.total_requests += 1
            
            if request_data.error_code:
                self.error_counts[request_data.error_code] += 1
                self.total_errors += 1
            
            # Update rate limiting data
            if request_data.user_id:
                self.rate_limits[request_data.user_id].append(datetime.now())
            
            # Periodically save to database (every 100 requests)
            if self.total_requests % 100 == 0:
                await self.save_to_database()
                
        except Exception as e:
            logger.error(f"Error recording request: {e}")
    
    async def save_to_database(self):
        """Save analytics data to database"""
        try:
            # Save recent requests to database
            requests_to_save = list(self.recent_requests)[-100:]  # Last 100 requests
            
            for request_data in requests_to_save:
                await self._save_request_to_db(request_data)
            
            logger.debug(f"Saved {len(requests_to_save)} requests to database")
            
        except Exception as e:
            logger.error(f"Error saving to database: {e}")
    
    async def _save_request_to_db(self, request_data: APIRequest):
        """Save individual request to database"""
        try:
            query = """
                INSERT INTO api_analytics (
                    request_id, timestamp, method, path, query_params,
                    user_id, session_id, ip_address, user_agent,
                    response_status, response_time_ms, error_code,
                    endpoint_category
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            params = (
                request_data.request_id,
                request_data.timestamp.isoformat(),
                request_data.method,
                request_data.path,
                str(request_data.query_params),
                request_data.user_id,
                request_data.session_id,
                request_data.ip_address,
                request_data.user_agent,
                request_data.response_status,
                request_data.response_time_ms,
                request_data.error_code,
                request_data.endpoint_category
            )
            
            await DatabaseManager.execute_async_update(query, params)
            
        except Exception as e:
            logger.error(f"Error saving request to database: {e}")
    
    def get_real_time_metrics(self) -> APIUsageMetrics:
        """Get real-time API usage metrics"""
        now = datetime.now()
        
        # Calculate time-based request rates
        requests_last_minute = 0
        requests_last_hour = 0
        requests_last_day = 0
        
        for request in self.recent_requests:
            time_diff = now - request.timestamp
            
            if time_diff.total_seconds() <= 60:
                requests_last_minute += 1
            if time_diff.total_seconds() <= 3600:
                requests_last_hour += 1
            if time_diff.total_seconds() <= 86400:
                requests_last_day += 1
        
        # Calculate average response time
        avg_response_time = 0
        if self.response_times:
            avg_response_time = sum(self.response_times) / len(self.response_times)
        
        # Calculate error rate
        error_rate = 0
        if self.total_requests > 0:
            error_rate = (self.total_errors / self.total_requests) * 100
        
        # Get top endpoints
        top_endpoints = [
            {"path": path, "count": count}
            for path, count in sorted(
                self.request_counts.items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:10]
        ]
        
        # Get top users
        top_users = [
            {"user_id": user_id, "count": count}
            for user_id, count in sorted(
                self.user_requests.items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:10]
        ]
        
        # Get status codes distribution
        status_codes = defaultdict(int)
        for request in self.recent_requests:
            if request.response_status:
                status_codes[request.response_status] += 1
        
        return APIUsageMetrics(
            total_requests=self.total_requests,
            requests_per_minute=requests_last_minute,
            requests_per_hour=requests_last_hour,
            requests_per_day=requests_last_day,
            error_rate=error_rate,
            avg_response_time=avg_response_time,
            top_endpoints=top_endpoints,
            top_users=top_users,
            status_codes=dict(status_codes),
            error_codes=dict(self.error_counts)
        )
    
    async def get_historical_metrics(
        self, 
        start_date: datetime, 
        end_date: datetime
    ) -> Dict[str, Any]:
        """Get historical metrics from database"""
        try:
            query = """
                SELECT 
                    DATE(timestamp) as date,
                    COUNT(*) as total_requests,
                    AVG(response_time_ms) as avg_response_time,
                    COUNT(CASE WHEN error_code IS NOT NULL THEN 1 END) as error_count,
                    endpoint_category,
                    response_status
                FROM api_analytics
                WHERE timestamp BETWEEN ? AND ?
                GROUP BY DATE(timestamp), endpoint_category, response_status
                ORDER BY date DESC
            """
            
            results = await DatabaseManager.execute_async_query(
                query, 
                (start_date.isoformat(), end_date.isoformat()),
                fetch_all=True
            )
            
            # Process results
            daily_metrics = defaultdict(lambda: {
                "total_requests": 0,
                "avg_response_time": 0,
                "error_count": 0,
                "categories": defaultdict(int),
                "status_codes": defaultdict(int)
            })
            
            for row in results:
                date = row["date"]
                daily_metrics[date]["total_requests"] += row["total_requests"]
                daily_metrics[date]["avg_response_time"] = max(
                    daily_metrics[date]["avg_response_time"], 
                    row["avg_response_time"] or 0
                )
                daily_metrics[date]["error_count"] += row["error_count"]
                daily_metrics[date]["categories"][row["endpoint_category"]] += row["total_requests"]
                daily_metrics[date]["status_codes"][row["response_status"]] += row["total_requests"]
            
            return dict(daily_metrics)
            
        except Exception as e:
            logger.error(f"Error getting historical metrics: {e}")
            return {}
    
    def check_rate_limit(self, user_id: str, limit: int = 100, window_minutes: int = 1) -> bool:
        """Check if user exceeds rate limit"""
        now = datetime.now()
        window_start = now - timedelta(minutes=window_minutes)
        
        # Clean old entries
        self.rate_limits[user_id] = [
            timestamp for timestamp in self.rate_limits[user_id]
            if timestamp > window_start
        ]
        
        return len(self.rate_limits[user_id]) < limit
    
    def get_user_analytics(self, user_id: str) -> Dict[str, Any]:
        """Get analytics for specific user"""
        user_requests = [
            req for req in self.recent_requests 
            if req.user_id == user_id
        ]
        
        if not user_requests:
            return {"error": "No data found for user"}
        
        # Calculate user metrics
        total_requests = len(user_requests)
        avg_response_time = 0
        if user_requests:
            response_times = [req.response_time_ms for req in user_requests if req.response_time_ms]
            if response_times:
                avg_response_time = sum(response_times) / len(response_times)
        
        # Get user's top endpoints
        endpoint_usage = defaultdict(int)
        for req in user_requests:
            endpoint_usage[req.path] += 1
        
        top_endpoints = [
            {"path": path, "count": count}
            for path, count in sorted(
                endpoint_usage.items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:10]
        ]
        
        # Get error rate
        error_count = sum(1 for req in user_requests if req.error_code)
        error_rate = (error_count / total_requests) * 100 if total_requests > 0 else 0
        
        return {
            "user_id": user_id,
            "total_requests": total_requests,
            "avg_response_time_ms": avg_response_time,
            "error_rate": error_rate,
            "top_endpoints": top_endpoints,
            "last_request": max(req.timestamp for req in user_requests).isoformat()
        }
    
    def get_endpoint_analytics(self, endpoint_path: str) -> Dict[str, Any]:
        """Get analytics for specific endpoint"""
        endpoint_requests = [
            req for req in self.recent_requests 
            if req.path == endpoint_path
        ]
        
        if not endpoint_requests:
            return {"error": "No data found for endpoint"}
        
        total_requests = len(endpoint_requests)
        avg_response_time = 0
        if endpoint_requests:
            response_times = [req.response_time_ms for req in endpoint_requests if req.response_time_ms]
            if response_times:
                avg_response_time = sum(response_times) / len(response_times)
        
        # Get unique users
        unique_users = len(set(req.user_id for req in endpoint_requests if req.user_id))
        
        # Get error rate
        error_count = sum(1 for req in endpoint_requests if req.error_code)
        error_rate = (error_count / total_requests) * 100 if total_requests > 0 else 0
        
        return {
            "endpoint": endpoint_path,
            "total_requests": total_requests,
            "unique_users": unique_users,
            "avg_response_time_ms": avg_response_time,
            "error_rate": error_rate,
            "last_request": max(req.timestamp for req in endpoint_requests).isoformat()
        }
    
    async def generate_analytics_report(
        self, 
        report_type: str = "daily"
    ) -> Dict[str, Any]:
        """Generate comprehensive analytics report"""
        now = datetime.now()
        
        if report_type == "daily":
            start_date = now - timedelta(days=1)
        elif report_type == "weekly":
            start_date = now - timedelta(weeks=1)
        elif report_type == "monthly":
            start_date = now - timedelta(days=30)
        else:
            start_date = now - timedelta(days=1)
        
        # Get real-time metrics
        real_time = self.get_real_time_metrics()
        
        # Get historical data
        historical = await self.get_historical_metrics(start_date, now)
        
        # Get system health
        uptime = (now - self.start_time).total_seconds()
        
        return {
            "report_type": report_type,
            "generated_at": now.isoformat(),
            "period": {
                "start_date": start_date.isoformat(),
                "end_date": now.isoformat()
            },
            "real_time_metrics": asdict(real_time),
            "historical_data": historical,
            "system_health": {
                "uptime_seconds": uptime,
                "uptime_hours": uptime / 3600,
                "total_requests_processed": self.total_requests,
                "memory_usage_mb": self._get_memory_usage(),
                "database_status": "healthy"  # Would check actual DB status
            },
            "top_performers": {
                "fastest_endpoints": self._get_fastest_endpoints(),
                "most_active_users": real_time.top_users[:5],
                "popular_endpoints": real_time.top_endpoints[:5]
            }
        }
    
    def _extract_user_id(self, request: Request) -> Optional[str]:
        """Extract user ID from request"""
        # Try session ID first
        session_id = request.headers.get("X-Session-ID")
        if session_id:
            # Extract user ID from session ID (format: session_{user_id}_{timestamp})
            parts = session_id.split("_")
            if len(parts) >= 2:
                return parts[1]
        
        # Try Authorization header
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            # Would decode JWT token to get user ID
            pass
        
        return None
    
    def _extract_session_id(self, request: Request) -> Optional[str]:
        """Extract session ID from request"""
        return request.headers.get("X-Session-ID")
    
    def _get_client_ip(self, request: Request) -> str:
        """Get client IP address"""
        # Check for forwarded headers
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        return request.client.host if request.client else "unknown"
    
    def _categorize_endpoint(self, path: str) -> str:
        """Categorize API endpoint"""
        if "/auth/" in path:
            return "authentication"
        elif "/users/" in path:
            return "user_management"
        elif "/financial/" in path or "/analytics/" in path:
            return "financial_data"
        elif "/chat/" in path:
            return "chat"
        elif "/reports/" in path:
            return "reports"
        elif "/alerts/" in path:
            return "alerts"
        elif "/ws/" in path:
            return "websocket"
        elif "/health" in path or "/status" in path:
            return "health"
        else:
            return "other"
    
    def _get_memory_usage(self) -> float:
        """Get current memory usage in MB"""
        try:
            import psutil
            process = psutil.Process()
            return process.memory_info().rss / 1024 / 1024
        except ImportError:
            return 0
    
    def _get_fastest_endpoints(self) -> List[Dict[str, Any]]:
        """Get endpoints with fastest response times"""
        endpoint_times = defaultdict(list)
        
        for request in self.recent_requests:
            if request.response_time_ms and request.response_status == 200:
                endpoint_times[request.path].append(request.response_time_ms)
        
        fastest = []
        for endpoint, times in endpoint_times.items():
            if times:
                avg_time = sum(times) / len(times)
                fastest.append({"endpoint": endpoint, "avg_response_time_ms": avg_time})
        
        return sorted(fastest, key=lambda x: x["avg_response_time_ms"])[:10]
    
    async def periodic_cleanup(self):
        """Periodic cleanup of old data"""
        while True:
            try:
                await asyncio.sleep(3600)  # Run every hour
                
                # Clean old rate limit data
                cutoff_time = datetime.now() - timedelta(hours=1)
                for user_id in list(self.rate_limits.keys()):
                    self.rate_limits[user_id] = [
                        timestamp for timestamp in self.rate_limits[user_id]
                        if timestamp > cutoff_time
                    ]
                    
                    if not self.rate_limits[user_id]:
                        del self.rate_limits[user_id]
                
                logger.info("Analytics cleanup completed")
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in periodic cleanup: {e}")


# Global analytics instance
analytics = APIAnalytics()


async def init_analytics_database():
    """Initialize analytics database tables"""
    try:
        with get_async_db() as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS api_analytics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    request_id TEXT UNIQUE NOT NULL,
                    timestamp TIMESTAMP NOT NULL,
                    method TEXT NOT NULL,
                    path TEXT NOT NULL,
                    query_params TEXT,
                    user_id TEXT,
                    session_id TEXT,
                    ip_address TEXT,
                    user_agent TEXT,
                    response_status INTEGER,
                    response_time_ms REAL,
                    error_code TEXT,
                    endpoint_category TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create indexes for performance
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_analytics_timestamp ON api_analytics(timestamp)")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_analytics_user_id ON api_analytics(user_id)")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_analytics_path ON api_analytics(path)")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_analytics_endpoint_category ON api_analytics(endpoint_category)")
            
            logger.info("Analytics database initialized")
            
    except Exception as e:
        logger.error(f"Error initializing analytics database: {e}")


# Middleware function for FastAPI
async def analytics_middleware(request: Request, call_next):
    """FastAPI middleware for API analytics"""
    if not settings.METRICS_ENABLED:
        return await call_next(request)
    
    async with analytics.track_request(request) as request_data:
        response = await call_next(request)
        
        # Update request data with response info
        request_data.response_status = response.status_code
        
        # Extract error code from response if available
        if response.status_code >= 400:
            try:
                body = response.body
                if body:
                    import json
                    error_data = json.loads(body)
                    request_data.error_code = error_data.get("error_code", "HTTP_ERROR")
            except:
                request_data.error_code = "HTTP_ERROR"
        
        return response
