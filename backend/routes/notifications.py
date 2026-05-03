"""
Notification Routes
API endpoints for notification management
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime

from auth.dependencies import get_current_user
from notifications.notification_manager import (
    notification_manager,
    NotificationType,
    NotificationPriority
)
from notifications.templates import notification_templates

router = APIRouter(tags=["Notifications"])


class CreateNotificationRequest(BaseModel):
    notification_type: str
    title: str
    message: str
    priority: int = 2
    data: Optional[Dict] = None
    channels: Optional[List[str]] = None


class NotificationPreferencesRequest(BaseModel):
    email_enabled: bool = True
    push_enabled: bool = True
    sms_enabled: bool = False
    in_app_enabled: bool = True
    quiet_hours: Optional[Dict] = None
    notification_types: Optional[Dict] = None
    priority_threshold: int = 1


class TemplateNotificationRequest(BaseModel):
    template_name: str
    variables: Dict


@router.get("/")
async def get_notifications(
    unread_only: bool = False,
    notification_type: Optional[str] = None,
    limit: int = 50,
    current_user: Dict = Depends(get_current_user)
):
    """
    Get user notifications
    
    Args:
        unread_only: Return only unread notifications
        notification_type: Filter by type
        limit: Maximum number of notifications
        current_user: Authenticated user
        
    Returns:
        List of notifications
    """
    try:
        # Convert type string to enum if provided
        type_filter = None
        if notification_type:
            try:
                type_filter = NotificationType(notification_type)
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid notification type: {notification_type}"
                )
        
        notifications = notification_manager.get_user_notifications(
            user_id=current_user.get("sub"),
            unread_only=unread_only,
            notification_type=type_filter,
            limit=limit
        )
        
        return {
            "success": True,
            "notifications": notifications,
            "count": len(notifications),
            "timestamp": datetime.now().isoformat()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/")
async def create_notification(
    request: CreateNotificationRequest,
    current_user: Dict = Depends(get_current_user)
):
    """
    Create a new notification
    
    Args:
        request: Notification data
        current_user: Authenticated user
        
    Returns:
        Created notification
    """
    try:
        # Validate notification type
        try:
            notif_type = NotificationType(request.notification_type)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid notification type: {request.notification_type}"
            )
        
        # Validate priority
        if request.priority < 1 or request.priority > 4:
            raise HTTPException(
                status_code=400,
                detail="Priority must be between 1 and 4"
            )
        
        priority = NotificationPriority(request.priority)
        
        # Create notification
        notification = notification_manager.create_notification(
            user_id=current_user.get("sub"),
            notification_type=notif_type,
            title=request.title,
            message=request.message,
            priority=priority,
            data=request.data,
            channels=request.channels
        )
        
        # Send notification
        notification = notification_manager.send_notification(notification["id"])
        
        return {
            "success": True,
            "notification": notification,
            "timestamp": datetime.now().isoformat()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/template")
async def create_from_template(
    request: TemplateNotificationRequest,
    current_user: Dict = Depends(get_current_user)
):
    """
    Create notification from template
    
    Args:
        request: Template name and variables
        current_user: Authenticated user
        
    Returns:
        Created notification
    """
    try:
        # Render template
        rendered = notification_templates.render_template(
            template_name=request.template_name,
            variables=request.variables
        )
        
        # Create notification
        notification = notification_manager.create_notification(
            user_id=current_user.get("sub"),
            notification_type=rendered["type"],
            title=rendered["title"],
            message=rendered["message"],
            priority=rendered["priority"],
            data=rendered["data"],
            channels=rendered["channels"]
        )
        
        # Send notification
        notification = notification_manager.send_notification(notification["id"])
        
        return {
            "success": True,
            "notification": notification,
            "timestamp": datetime.now().isoformat()
        }
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/templates")
async def list_templates(
    current_user: Dict = Depends(get_current_user)
):
    """
    List available notification templates
    
    Args:
        current_user: Authenticated user
        
    Returns:
        List of templates
    """
    try:
        templates = notification_templates.list_templates()
        
        return {
            "success": True,
            "templates": templates,
            "count": len(templates),
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{notification_id}/read")
async def mark_as_read(
    notification_id: str,
    current_user: Dict = Depends(get_current_user)
):
    """
    Mark notification as read
    
    Args:
        notification_id: Notification ID
        current_user: Authenticated user
        
    Returns:
        Updated notification
    """
    try:
        notification = notification_manager.mark_as_read(notification_id)
        
        # Verify ownership
        if notification["user_id"] != current_user.get("sub"):
            raise HTTPException(status_code=403, detail="Access denied")
        
        return {
            "success": True,
            "notification": notification,
            "timestamp": datetime.now().isoformat()
        }
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{notification_id}")
async def delete_notification(
    notification_id: str,
    current_user: Dict = Depends(get_current_user)
):
    """
    Delete a notification
    
    Args:
        notification_id: Notification ID
        current_user: Authenticated user
        
    Returns:
        Success status
    """
    try:
        # Get notification to verify ownership
        notifications = notification_manager.get_user_notifications(
            user_id=current_user.get("sub"),
            limit=1000
        )
        
        notification = next(
            (n for n in notifications if n["id"] == notification_id),
            None
        )
        
        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")
        
        # Delete notification
        success = notification_manager.delete_notification(notification_id)
        
        return {
            "success": success,
            "timestamp": datetime.now().isoformat()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/")
async def delete_all_notifications(
    older_than_days: Optional[int] = None,
    current_user: Dict = Depends(get_current_user)
):
    """
    Delete all notifications for user
    
    Args:
        older_than_days: Delete only notifications older than X days
        current_user: Authenticated user
        
    Returns:
        Number of deleted notifications
    """
    try:
        deleted_count = notification_manager.delete_user_notifications(
            user_id=current_user.get("sub"),
            older_than_days=older_than_days
        )
        
        return {
            "success": True,
            "deleted_count": deleted_count,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
async def get_notification_stats(
    current_user: Dict = Depends(get_current_user)
):
    """
    Get notification statistics
    
    Args:
        current_user: Authenticated user
        
    Returns:
        Notification statistics
    """
    try:
        stats = notification_manager.get_notification_stats(current_user.get("sub"))
        
        return {
            "success": True,
            "stats": stats,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/preferences")
async def get_preferences(
    current_user: Dict = Depends(get_current_user)
):
    """
    Get notification preferences
    
    Args:
        current_user: Authenticated user
        
    Returns:
        User notification preferences
    """
    try:
        preferences = notification_manager.get_user_preferences(current_user.get("sub"))
        
        return {
            "success": True,
            "preferences": preferences,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/preferences")
async def update_preferences(
    request: NotificationPreferencesRequest,
    current_user: Dict = Depends(get_current_user)
):
    """
    Update notification preferences
    
    Args:
        request: Notification preferences
        current_user: Authenticated user
        
    Returns:
        Updated preferences
    """
    try:
        preferences = notification_manager.set_user_preferences(
            user_id=current_user.get("sub"),
            preferences=request.dict()
        )
        
        return {
            "success": True,
            "preferences": preferences,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/batch")
async def create_batch_notifications(
    notifications: List[CreateNotificationRequest],
    current_user: Dict = Depends(get_current_user)
):
    """
    Create multiple notifications at once
    
    Args:
        notifications: List of notifications to create
        current_user: Authenticated user
        
    Returns:
        Created notifications
    """
    try:
        # Prepare notification data
        notif_data = []
        for notif in notifications:
            notif_data.append({
                "user_id": current_user.get("sub"),
                "type": notif.notification_type,
                "title": notif.title,
                "message": notif.message,
                "priority": notif.priority,
                "data": notif.data,
                "channels": notif.channels
            })
        
        # Create notifications
        created = notification_manager.create_batch_notifications(notif_data)
        
        # Send all notifications
        notification_ids = [n["id"] for n in created]
        results = notification_manager.send_batch_notifications(notification_ids)
        
        return {
            "success": True,
            "notifications": list(results.values()),
            "count": len(results),
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
