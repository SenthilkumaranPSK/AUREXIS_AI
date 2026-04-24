"""
Data Export Routes

Allow users to export their financial data in various formats.
"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from typing import Literal
import csv
import json
import io
from datetime import datetime

router = APIRouter(prefix="/api/export", tags=["export"])


@router.get("/{user_id}/expenses")
async def export_expenses(
    user_id: str,
    format: Literal["csv", "json"] = "csv"
):
    """Export user expenses"""
    # TODO: Get actual data from database
    expenses = [
        {"date": "2026-04-01", "category": "Food", "amount": 1500, "description": "Groceries"},
        {"date": "2026-04-05", "category": "Transport", "amount": 500, "description": "Taxi"},
        {"date": "2026-04-10", "category": "Entertainment", "amount": 800, "description": "Movie"},
    ]
    
    if format == "csv":
        return _export_csv(expenses, "expenses")
    else:
        return _export_json(expenses, "expenses")


@router.get("/{user_id}/income")
async def export_income(
    user_id: str,
    format: Literal["csv", "json"] = "csv"
):
    """Export user income"""
    income = [
        {"date": "2026-04-01", "source": "Salary", "amount": 50000, "description": "Monthly salary"},
        {"date": "2026-04-15", "source": "Freelance", "amount": 10000, "description": "Project payment"},
    ]
    
    if format == "csv":
        return _export_csv(income, "income")
    else:
        return _export_json(income, "income")


@router.get("/{user_id}/goals")
async def export_goals(
    user_id: str,
    format: Literal["csv", "json"] = "csv"
):
    """Export user goals"""
    goals = [
        {"name": "Emergency Fund", "target": 100000, "current": 30000, "progress": 30},
        {"name": "Vacation", "target": 50000, "current": 15000, "progress": 30},
    ]
    
    if format == "csv":
        return _export_csv(goals, "goals")
    else:
        return _export_json(goals, "goals")


@router.get("/{user_id}/all")
async def export_all_data(
    user_id: str,
    format: Literal["json"] = "json"
):
    """Export all user data"""
    all_data = {
        "user_id": user_id,
        "export_date": datetime.now().isoformat(),
        "expenses": [],
        "income": [],
        "goals": [],
        "investments": [],
        "alerts": [],
        "recommendations": []
    }
    
    return _export_json(all_data, "all_data")


def _export_csv(data: list, filename: str) -> StreamingResponse:
    """Export data as CSV"""
    if not data:
        raise HTTPException(status_code=404, detail="No data to export")
    
    # Create CSV in memory
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)
    
    # Create response
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename={filename}_{datetime.now().strftime('%Y%m%d')}.csv"
        }
    )


def _export_json(data, filename: str) -> StreamingResponse:
    """Export data as JSON"""
    # Create JSON in memory
    json_str = json.dumps(data, indent=2)
    
    # Create response
    return StreamingResponse(
        iter([json_str]),
        media_type="application/json",
        headers={
            "Content-Disposition": f"attachment; filename={filename}_{datetime.now().strftime('%Y%m%d')}.json"
        }
    )
