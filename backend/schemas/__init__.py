"""
Pydantic Schemas
Request and response validation models
"""

from .auth import (
    SignupRequest,
    LoginRequest,
    LoginResponse,
    TokenResponse,
    RefreshTokenRequest,
    ChangePasswordRequest,
    UserResponse
)

from .financial import (
    ExpenseCreate,
    ExpenseUpdate,
    ExpenseResponse,
    IncomeCreate,
    IncomeResponse,
    GoalCreate,
    GoalUpdate,
    GoalResponse,
    AlertResponse,
    RecommendationResponse
)

from .chat import (
    ChatRequest,
    ChatResponse,
    ChatHistoryResponse
)

from .report import (
    ReportRequest,
    ReportResponse
)

__all__ = [
    # Auth
    "SignupRequest",
    "LoginRequest",
    "LoginResponse",
    "TokenResponse",
    "RefreshTokenRequest",
    "ChangePasswordRequest",
    "UserResponse",
    # Financial
    "ExpenseCreate",
    "ExpenseUpdate",
    "ExpenseResponse",
    "IncomeCreate",
    "IncomeResponse",
    "GoalCreate",
    "GoalUpdate",
    "GoalResponse",
    "AlertResponse",
    "RecommendationResponse",
    # Chat
    "ChatRequest",
    "ChatResponse",
    "ChatHistoryResponse",
    # Report
    "ReportRequest",
    "ReportResponse",
]
