"""
Chat Schemas
"""

from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=5000)
    session_id: Optional[str] = None
    use_memory: bool = True


class ChatResponse(BaseModel):
    success: bool
    response: Dict[str, Any]
    session_id: str
    timestamp: datetime


class ChatHistoryResponse(BaseModel):
    id: int
    session_id: str
    role: str
    content: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class ChatSessionResponse(BaseModel):
    id: str
    user_id: str
    title: Optional[str]
    message_count: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
