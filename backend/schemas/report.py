"""
Report Schemas
"""

from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime


class ReportRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    report_type: str = Field(..., pattern="^(monthly|quarterly|annual|custom)$")
    format: str = Field(..., pattern="^(pdf|csv|json)$")
    start_date: Optional[str] = None
    end_date: Optional[str] = None


class ReportResponse(BaseModel):
    id: str
    user_id: str
    name: str
    type: str
    format: str
    file_path: Optional[str]
    size: Optional[str]
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
