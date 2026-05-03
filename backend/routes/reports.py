"""
Reports Routes
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict
from datetime import datetime
import uuid
from schemas.report import ReportRequest, ReportResponse
from auth.dependencies import get_current_user
from user_manager_json import UserManagerJSON
from report import generate_report

reports_router = APIRouter(tags=["Reports"])


@reports_router.post("/generate", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
async def generate_new_report(
    request: ReportRequest,
    current_user: Dict = Depends(get_current_user)
):
    """Generate a new financial report"""
    try:
        user_id = current_user.get("sub")
        user = UserManagerJSON.get_user_by_id(user_id) or {"name": "User", "number": user_id}      
        data = UserManagerJSON.get_all_user_data(user_id)

        # Generate report
        report_data = generate_report(user, data)

        # Create report ID
        report_id = str(uuid.uuid4())

        # Store report metadata in database
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO reports (id, user_id, name, type, format)
                VALUES (?, ?, ?, ?, ?)
            """, (
                report_id,
                user_id,
                request.name,
                request.report_type,
                request.format
            ))

        # Get the created report
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM reports WHERE id = ?", (report_id,))     
            row = cursor.fetchone()
            report = dict(row) if row else None

        if not report:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create report"
            )

        return ReportResponse(**report)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate report: {str(e)}"
        )


@reports_router.get("/list")
async def list_reports(current_user: Dict = Depends(get_current_user)):
    """Get list of user reports"""
    try:
        user_id = current_user.get("sub")

        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM reports
                WHERE user_id = ?
                ORDER BY created_at DESC
            """, (user_id,))

            reports = [dict(row) for row in cursor.fetchall()]

        return {
            "user_id": user_id,
            "reports": reports,
            "count": len(reports)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch reports: {str(e)}"
        )


@reports_router.get("/{report_id}", response_model=ReportResponse)
async def get_report(
    report_id: str,
    current_user: Dict = Depends(get_current_user)
):
    """Get a specific report"""
    try:
        user_id = current_user.get("sub")

        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM reports
                WHERE id = ? AND user_id = ?
            """, (report_id, user_id))

            row = cursor.fetchone()
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Report not found"
                )

            report = dict(row)

        return ReportResponse(**report)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch report: {str(e)}"
        )


@reports_router.delete("/{report_id}")
async def delete_report(
    report_id: str,
    current_user: Dict = Depends(get_current_user)
):
    """Delete a report"""
    try:
        user_id = current_user.get("sub")

        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM reports
                WHERE id = ? AND user_id = ?
            """, (report_id, user_id))

            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Report not found"
                )

        return {"success": True, "message": "Report deleted"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete report: {str(e)}"
        )


@reports_router.get("/download/{report_id}")
async def download_report(
    report_id: str,
    current_user: Dict = Depends(get_current_user)
):
    """Download a report file"""
    try:
        user_id = current_user.get("sub")

        # Get report metadata
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM reports
                WHERE id = ? AND user_id = ?
            """, (report_id, user_id))

            row = cursor.fetchone()
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Report not found"
                )

            report = dict(row)

        # For now, return report data as JSON
        # In production, this would return the actual file
        user = UserManagerJSON.get_user_by_id(user_id) or {"name": "User", "number": user_id}      
        data = UserManagerJSON.get_all_user_data(user_id)
        report_data = generate_report(user, data)

        return {
            "report_id": report_id,
            "name": report["name"],
            "format": report["format"],
            "data": report_data
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to download report: {str(e)}"
        )
