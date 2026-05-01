"""
API Versioning System for AUREXIS AI
Provides structured API versioning with backward compatibility
"""

from typing import List, Dict, Any
from fastapi import APIRouter, FastAPI
from fastapi.routing import APIRoute


class APIVersion:
    """API Version configuration"""
    
    def __init__(
        self,
        version: str,
        prefix: str,
        description: str,
        deprecated: bool = False,
        deprecation_message: str = None,
        sunset_date: str = None
    ):
        self.version = version
        self.prefix = prefix
        self.description = description
        self.deprecated = deprecated
        self.deprecation_message = deprecation_message
        self.sunset_date = sunset_date


# API Version configurations
API_VERSIONS = {
    "v1": APIVersion(
        version="v1",
        prefix="/api/v1",
        description="Current stable API version with comprehensive features",
        deprecated=False
    ),
    "v2": APIVersion(
        version="v2", 
        prefix="/api/v2",
        description="Next generation API with enhanced features",
        deprecated=False
    )
}

# Legacy API version (for backward compatibility)
LEGACY_VERSION = APIVersion(
    version="legacy",
    prefix="/api",
    description="Legacy API - please migrate to v1",
    deprecated=True,
    deprecation_message="This API version is deprecated. Please migrate to /api/v1",
    sunset_date="2025-12-31"
)


class VersionedAPIRouter(APIRouter):
    """Custom router that adds version information to responses"""
    
    def __init__(self, version: str, **kwargs):
        super().__init__(**kwargs)
        self.version = version
        self.api_version = API_VERSIONS.get(version, LEGACY_VERSION)


def create_versioned_router(version: str, prefix: str = None) -> VersionedAPIRouter:
    """Create a versioned API router"""
    api_version = API_VERSIONS.get(version, LEGACY_VERSION)
    router_prefix = prefix or api_version.prefix
    
    return VersionedAPIRouter(
        version=version,
        prefix=router_prefix,
        tags=[f"API {version.upper()}"]
    )


def register_versioned_routes(app: FastAPI):
    """Register all API versions with the FastAPI app"""
    
    # Import route modules that exist
    try:
        from routes import (
            financial_router,
            forecast_router,
            chat_router,
            reports_router
        )
    except ImportError as e:
        print(f"Warning: Could not import basic routes: {e}")
        return
    
    # Import optional advanced route modules
    try:
        from routes.advanced_analytics import router as advanced_analytics_router
    except ImportError:
        advanced_analytics_router = None
        
    try:
        from routes.ml_forecasting import router as ml_forecasting_router
    except ImportError:
        ml_forecasting_router = None
        
    try:
        from routes.investment_optimization import router as investment_optimization_router
    except ImportError:
        investment_optimization_router = None
        
    try:
        from routes.notifications import router as notifications_router
    except ImportError:
        notifications_router = None
        
    try:
        from routes.websocket_routes import router as websocket_router
    except ImportError:
        websocket_router = None
        
    try:
        from routes.agent_monitoring import router as agent_monitoring_router
    except ImportError:
        agent_monitoring_router = None
    
    # Create v1 routers
    # v1_auth = create_versioned_router("v1", "/api/v1/auth")  # Disabled - using simple login
    v1_financial = create_versioned_router("v1", "/api/v1/financial")
    v1_forecast = create_versioned_router("v1", "/api/v1/forecast")
    v1_chat = create_versioned_router("v1", "/api/v1/chat")
    v1_reports = create_versioned_router("v1", "/api/v1/reports")
    
    # Optional advanced routers
    if advanced_analytics_router:
        v1_analytics = create_versioned_router("v1", "/api/v1/analytics")
    if ml_forecasting_router:
        v1_ml = create_versioned_router("v1", "/api/v1/ml")
    if investment_optimization_router:
        v1_investments = create_versioned_router("v1", "/api/v1/investments")
    if notifications_router:
        v1_notifications = create_versioned_router("v1", "/api/v1/notifications")
    if websocket_router:
        v1_websocket = create_versioned_router("v1", "/ws/v1")
    if agent_monitoring_router:
        v1_agents = create_versioned_router("v1", "/api/v1/agents")
    
    # Include v1 routes
    # v1_auth.include_router(auth_router)  # Disabled - using simple login
    v1_financial.include_router(financial_router)
    v1_forecast.include_router(forecast_router)
    v1_chat.include_router(chat_router)
    v1_reports.include_router(reports_router)
    
    # Include optional routes
    if advanced_analytics_router:
        v1_analytics.include_router(advanced_analytics_router)
    if ml_forecasting_router:
        v1_ml.include_router(ml_forecasting_router)
    if investment_optimization_router:
        v1_investments.include_router(investment_optimization_router)
    if notifications_router:
        v1_notifications.include_router(notifications_router)
    if websocket_router:
        v1_websocket.include_router(websocket_router)
    if agent_monitoring_router:
        v1_agents.include_router(agent_monitoring_router)
    
    # Register v1 routers with app
    # app.include_router(v1_auth)  # Disabled - using simple login
    app.include_router(v1_financial)
    app.include_router(v1_forecast)
    app.include_router(v1_chat)
    app.include_router(v1_reports)
    
    # Include optional routers
    if advanced_analytics_router:
        app.include_router(v1_analytics)
    if ml_forecasting_router:
        app.include_router(v1_ml)
    if investment_optimization_router:
        app.include_router(v1_investments)
    if notifications_router:
        app.include_router(v1_notifications)
    if websocket_router:
        app.include_router(v1_websocket)
    if agent_monitoring_router:
        app.include_router(v1_agents)
    
    # Include the v1 router with simple login endpoint
    from routes.api_v1 import api_v1_router
    app.include_router(api_v1_router)
    
    # Create legacy router for backward compatibility
    legacy_router = VersionedAPIRouter(
        version="legacy",
        prefix="/api",
        tags=["Legacy API"]
    )
    
    # Include legacy routes with deprecation warnings
    # legacy_router.include_router(auth_router, prefix="/auth", tags=["Legacy - Auth"])  # Disabled
    legacy_router.include_router(financial_router, prefix="/financial", tags=["Legacy - Financial"])
    legacy_router.include_router(forecast_router, prefix="/forecast", tags=["Legacy - Forecast"])
    legacy_router.include_router(chat_router, prefix="/chat", tags=["Legacy - Chat"])
    legacy_router.include_router(reports_router, prefix="/reports", tags=["Legacy - Reports"])
    
    app.include_router(legacy_router)


def get_api_version_info() -> Dict[str, Any]:
    """Get information about all available API versions"""
    versions = {}
    
    for key, version in API_VERSIONS.items():
        versions[key] = {
            "version": version.version,
            "prefix": version.prefix,
            "description": version.description,
            "deprecated": version.deprecated,
            "deprecation_message": version.deprecation_message,
            "sunset_date": version.sunset_date
        }
    
    # Add legacy version info
    versions["legacy"] = {
        "version": LEGACY_VERSION.version,
        "prefix": LEGACY_VERSION.prefix,
        "description": LEGACY_VERSION.description,
        "deprecated": LEGACY_VERSION.deprecated,
        "deprecation_message": LEGACY_VERSION.deprecation_message,
        "sunset_date": LEGACY_VERSION.sunset_date
    }
    
    return {
        "versions": versions,
        "current_stable": "v1",
        "legacy_support_until": LEGACY_VERSION.sunset_date
    }


def add_version_middleware(app: FastAPI):
    """Add middleware to handle API versioning and deprecation warnings"""
    
    @app.middleware("http")
    async def version_middleware(request, call_next):
        response = await call_next(request)
        
        # Add version headers
        if request.url.path.startswith("/api/v1"):
            response.headers["X-API-Version"] = "v1"
        elif request.url.path.startswith("/api/v2"):
            response.headers["X-API-Version"] = "v2"
        elif request.url.path.startswith("/api/"):
            response.headers["X-API-Version"] = "legacy"
            response.headers["X-API-Deprecated"] = "true"
            response.headers["X-API-Sunset-Date"] = LEGACY_VERSION.sunset_date
            response.headers["X-API-Migration-Guide"] = "/api/v1/docs"
        
        return response
