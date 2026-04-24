"""
Notification Manager
Manages notification creation, delivery, and tracking
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from enum import Enum
import uuid


class NotificationType(Enum):
    """Notification types"""
    ALERT = "alert"
    RECOMMENDATION = "recommendation"
    GOAL_PROGRESS = "goal_progress"
    BUDGET_WARNING = "budget_warning"
    TRANSACTION = "transaction"
    INSIGHT = "insight"
    REPORT_READY = "report_ready"
    SYSTEM = "system"


class NotificationPriority(Enum):
    """Notification priority levels"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4


class NotificationStatus(Enum):
    """Notification status"""
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"
    FAILED = "failed"


class NotificationManager:
    """Manage notifications across the system"""
    
    def __init__(self):
        # In-memory storage (in production, use database)
        self.notifications: Dict[str, Dict] = {}
        self.user_preferences: Dict[str, Dict] = {}
        self.notification_history: List[Dict] = []
    
    def create_notification(
        self,
        user_id: str,
        notification_type: NotificationType,
        title: str,
        message: str,
        priority: NotificationPriority = NotificationPriority.MEDIUM,
        data: Optional[Dict] = None,
        channels: Optional[List[str]] = None,
        expires_at: Optional[datetime] = None
    ) -> Dict:
        """
        Create a new notification
        
        Args:
            user_id: User ID
            notification_type: Type of notification
            title: Notification title
            message: Notification message
            priority: Priority level
            data: Additional data
            channels: Delivery channels
            expires_at: Expiration time
            
        Returns:
            Created notification
        """
        notification_id = str(uuid.uuid4())
        
        # Get user preferences
        preferences = self.user_preferences.get(user_id, {})
        
        # Determine channels based on preferences and priority
        if channels is None:
            channels = self._determine_channels(
                user_id,
                notification_type,
                priority,
                preferences
            )
        
        # Set expiration
        if expires_at is None:
            expires_at = datetime.now() + timedelta(days=7)
        
        notification = {
            "id": notification_id,
            "user_id": user_id,
            "type": notification_type.value,
            "title": title,
            "message": message,
            "priority": priority.value,
            "data": data or {},
            "channels": channels,
            "status": NotificationStatus.PENDING.value,
            "created_at": datetime.now().isoformat(),
            "expires_at": expires_at.isoformat(),
            "read_at": None,
            "delivered_at": None
        }
        
        self.notifications[notification_id] = notification
        
        return notification
    
    def send_notification(self, notification_id: str) -> Dict:
        """
        Send a notification through configured channels
        
        Args:
            notification_id: Notification ID
            
        Returns:
            Updated notification with delivery status
        """
        notification = self.notifications.get(notification_id)
        
        if not notification:
            raise ValueError(f"Notification {notification_id} not found")
        
        # Check if already sent
        if notification["status"] != NotificationStatus.PENDING.value:
            return notification
        
        # Send through each channel
        delivery_results = {}
        for channel in notification["channels"]:
            try:
                result = self._send_to_channel(notification, channel)
                delivery_results[channel] = result
            except Exception as e:
                delivery_results[channel] = {"success": False, "error": str(e)}
        
        # Update notification status
        all_success = all(r.get("success", False) for r in delivery_results.values())
        
        notification["status"] = (
            NotificationStatus.SENT.value if all_success
            else NotificationStatus.FAILED.value
        )
        notification["delivered_at"] = datetime.now().isoformat()
        notification["delivery_results"] = delivery_results
        
        # Add to history
        self.notification_history.append({
            "notification_id": notification_id,
            "timestamp": datetime.now().isoformat(),
            "action": "sent",
            "results": delivery_results
        })
        
        return notification
    
    def mark_as_read(self, notification_id: str) -> Dict:
        """Mark notification as read"""
        notification = self.notifications.get(notification_id)
        
        if not notification:
            raise ValueError(f"Notification {notification_id} not found")
        
        notification["status"] = NotificationStatus.READ.value
        notification["read_at"] = datetime.now().isoformat()
        
        return notification
    
    def get_user_notifications(
        self,
        user_id: str,
        unread_only: bool = False,
        notification_type: Optional[NotificationType] = None,
        limit: int = 50
    ) -> List[Dict]:
        """
        Get notifications for a user
        
        Args:
            user_id: User ID
            unread_only: Return only unread notifications
            notification_type: Filter by type
            limit: Maximum number of notifications
            
        Returns:
            List of notifications
        """
        notifications = [
            n for n in self.notifications.values()
            if n["user_id"] == user_id
        ]
        
        # Filter by read status
        if unread_only:
            notifications = [
                n for n in notifications
                if n["status"] != NotificationStatus.READ.value
            ]
        
        # Filter by type
        if notification_type:
            notifications = [
                n for n in notifications
                if n["type"] == notification_type.value
            ]
        
        # Remove expired
        now = datetime.now()
        notifications = [
            n for n in notifications
            if datetime.fromisoformat(n["expires_at"]) > now
        ]
        
        # Sort by priority and created_at
        notifications.sort(
            key=lambda x: (
                -x["priority"],
                x["created_at"]
            ),
            reverse=True
        )
        
        return notifications[:limit]
    
    def get_notification_stats(self, user_id: str) -> Dict:
        """Get notification statistics for a user"""
        user_notifications = [
            n for n in self.notifications.values()
            if n["user_id"] == user_id
        ]
        
        total = len(user_notifications)
        unread = sum(
            1 for n in user_notifications
            if n["status"] != NotificationStatus.READ.value
        )
        
        by_type = {}
        for n in user_notifications:
            n_type = n["type"]
            by_type[n_type] = by_type.get(n_type, 0) + 1
        
        by_priority = {}
        for n in user_notifications:
            priority = n["priority"]
            by_priority[priority] = by_priority.get(priority, 0) + 1
        
        return {
            "total": total,
            "unread": unread,
            "read": total - unread,
            "by_type": by_type,
            "by_priority": by_priority
        }
    
    def set_user_preferences(
        self,
        user_id: str,
        preferences: Dict
    ) -> Dict:
        """
        Set notification preferences for a user
        
        Args:
            user_id: User ID
            preferences: Notification preferences
            
        Returns:
            Updated preferences
        """
        self.user_preferences[user_id] = {
            "email_enabled": preferences.get("email_enabled", True),
            "push_enabled": preferences.get("push_enabled", True),
            "sms_enabled": preferences.get("sms_enabled", False),
            "in_app_enabled": preferences.get("in_app_enabled", True),
            "quiet_hours": preferences.get("quiet_hours", {
                "enabled": False,
                "start": "22:00",
                "end": "08:00"
            }),
            "notification_types": preferences.get("notification_types", {
                "alert": True,
                "recommendation": True,
                "goal_progress": True,
                "budget_warning": True,
                "transaction": True,
                "insight": True,
                "report_ready": True,
                "system": True
            }),
            "priority_threshold": preferences.get("priority_threshold", 1)
        }
        
        return self.user_preferences[user_id]
    
    def get_user_preferences(self, user_id: str) -> Dict:
        """Get notification preferences for a user"""
        return self.user_preferences.get(user_id, {
            "email_enabled": True,
            "push_enabled": True,
            "sms_enabled": False,
            "in_app_enabled": True,
            "quiet_hours": {"enabled": False},
            "notification_types": {},
            "priority_threshold": 1
        })
    
    def delete_notification(self, notification_id: str) -> bool:
        """Delete a notification"""
        if notification_id in self.notifications:
            del self.notifications[notification_id]
            return True
        return False
    
    def delete_user_notifications(
        self,
        user_id: str,
        older_than_days: Optional[int] = None
    ) -> int:
        """
        Delete notifications for a user
        
        Args:
            user_id: User ID
            older_than_days: Delete notifications older than X days
            
        Returns:
            Number of deleted notifications
        """
        to_delete = []
        
        for notification_id, notification in self.notifications.items():
            if notification["user_id"] != user_id:
                continue
            
            if older_than_days:
                created_at = datetime.fromisoformat(notification["created_at"])
                age = (datetime.now() - created_at).days
                if age > older_than_days:
                    to_delete.append(notification_id)
            else:
                to_delete.append(notification_id)
        
        for notification_id in to_delete:
            del self.notifications[notification_id]
        
        return len(to_delete)
    
    def _determine_channels(
        self,
        user_id: str,
        notification_type: NotificationType,
        priority: NotificationPriority,
        preferences: Dict
    ) -> List[str]:
        """Determine which channels to use based on preferences and priority"""
        channels = []
        
        # Check if notification type is enabled
        type_enabled = preferences.get("notification_types", {}).get(
            notification_type.value,
            True
        )
        
        if not type_enabled:
            return ["in_app"]  # Always show in-app
        
        # Check priority threshold
        priority_threshold = preferences.get("priority_threshold", 1)
        if priority.value < priority_threshold:
            return ["in_app"]
        
        # Check quiet hours
        quiet_hours = preferences.get("quiet_hours", {})
        if quiet_hours.get("enabled", False):
            now = datetime.now().time()
            start = datetime.strptime(quiet_hours.get("start", "22:00"), "%H:%M").time()
            end = datetime.strptime(quiet_hours.get("end", "08:00"), "%H:%M").time()
            
            if start <= now or now <= end:
                return ["in_app"]  # Only in-app during quiet hours
        
        # Add channels based on preferences
        if preferences.get("in_app_enabled", True):
            channels.append("in_app")
        
        if preferences.get("push_enabled", True):
            channels.append("push")
        
        if preferences.get("email_enabled", True) and priority.value >= 3:
            channels.append("email")
        
        if preferences.get("sms_enabled", False) and priority.value >= 4:
            channels.append("sms")
        
        return channels if channels else ["in_app"]
    
    def _send_to_channel(self, notification: Dict, channel: str) -> Dict:
        """
        Send notification to a specific channel
        
        In production, this would integrate with actual services:
        - Email: SendGrid, AWS SES, etc.
        - Push: Firebase Cloud Messaging, OneSignal, etc.
        - SMS: Twilio, AWS SNS, etc.
        """
        # Simulate sending
        if channel == "in_app":
            return {"success": True, "channel": "in_app"}
        elif channel == "push":
            return {"success": True, "channel": "push", "message": "Push notification sent"}
        elif channel == "email":
            return {"success": True, "channel": "email", "message": "Email sent"}
        elif channel == "sms":
            return {"success": True, "channel": "sms", "message": "SMS sent"}
        else:
            return {"success": False, "error": f"Unknown channel: {channel}"}
    
    def create_batch_notifications(
        self,
        notifications: List[Dict]
    ) -> List[Dict]:
        """Create multiple notifications at once"""
        created = []
        
        for notif_data in notifications:
            notification = self.create_notification(
                user_id=notif_data["user_id"],
                notification_type=NotificationType(notif_data["type"]),
                title=notif_data["title"],
                message=notif_data["message"],
                priority=NotificationPriority(notif_data.get("priority", 2)),
                data=notif_data.get("data"),
                channels=notif_data.get("channels")
            )
            created.append(notification)
        
        return created
    
    def send_batch_notifications(
        self,
        notification_ids: List[str]
    ) -> Dict[str, Dict]:
        """Send multiple notifications at once"""
        results = {}
        
        for notification_id in notification_ids:
            try:
                result = self.send_notification(notification_id)
                results[notification_id] = result
            except Exception as e:
                results[notification_id] = {"error": str(e)}
        
        return results


# Global instance
notification_manager = NotificationManager()
