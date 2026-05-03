"""
Financial Schemas
"""

from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime, date


# ==================== EXPENSES ====================

class ExpenseCreate(BaseModel):
    date: date
    amount: float = Field(..., gt=0)
    category: str = Field(..., min_length=1, max_length=50)
    description: str = Field(..., min_length=1, max_length=500)
    merchant: Optional[str] = Field(None, max_length=100)


class ExpenseUpdate(BaseModel):
    date: Optional[date] = None
    amount: Optional[float] = Field(None, gt=0)
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = Field(None, min_length=1, max_length=500)
    merchant: Optional[str] = Field(None, max_length=100)


class ExpenseResponse(BaseModel):
    id: int
    user_id: str
    date: date
    amount: float
    category: str
    description: str
    merchant: Optional[str]
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ==================== INCOME ====================

class IncomeCreate(BaseModel):
    month: date
    amount: float = Field(..., gt=0)
    source: str = Field(..., min_length=1, max_length=100)


class IncomeResponse(BaseModel):
    id: int
    user_id: str
    month: date
    amount: float
    source: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ==================== GOALS ====================

class GoalCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    target_amount: float = Field(..., gt=0)
    deadline: date
    category: str = Field(..., min_length=1, max_length=50)


class GoalUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    target_amount: Optional[float] = Field(None, gt=0)
    current_amount: Optional[float] = Field(None, ge=0)
    deadline: Optional[date] = None
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    status: Optional[str] = Field(None, pattern="^(active|completed|paused)$")


class GoalResponse(BaseModel):
    id: int
    user_id: str
    name: str
    target_amount: float
    current_amount: float
    deadline: date
    category: str
    status: str
    progress: float  # Calculated field
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ==================== ALERTS ====================

class AlertResponse(BaseModel):
    id: int
    user_id: str
    type: str
    title: str
    message: str
    severity: str
    is_read: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ==================== RECOMMENDATIONS ====================

class RecommendationResponse(BaseModel):
    id: int
    user_id: str
    category: str
    title: str
    description: str
    priority: str
    impact: Optional[str]
    status: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
