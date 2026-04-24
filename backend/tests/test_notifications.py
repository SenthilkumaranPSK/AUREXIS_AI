"""
Tests for Notification System
"""

import pytest
from notifications.notification_manager import (
    notification_manager,
    NotificationType,
    NotificationPriority
)
from notifications.templates import notification_templates


class TestNotificationManager:
    """Test notification manager"""
    
    def test_create_notification(self):
        """Test creating a notification"""
        notification = notification_manager.create_notification(
            user_id="test_user",
            notification_type=NotificationType.ALERT,
            title="Test Alert",
            message="This is a test alert",
            priority=NotificationPriority.HIGH
        )
        
        assert notification["user_id"] == "test_user"
        assert notification["title"] == "Test Alert"
        assert notification["priority"] == 3
        assert notification["status"] == "pending"
    
    def test_send_notification(self):
        """Test sending a notification"""
        notification = notification_manager.create_notification(
            user_id="test_user",
            notification_type=NotificationType.ALERT,
            title="Test Alert",
            message="Test message",
            priority=NotificationPriority.MEDIUM
        )
        
        sent = notification_manager.send_notification(notification["id"])
        
        assert sent["status"] in ["sent", "failed"]
        assert "delivered_at" in sent
    
    def test_mark_as_read(self):
        """Test marking notification as read"""
        notification = notification_manager.create_notification(
            user_id="test_user",
            notification_type=NotificationType.ALERT,
            title="Test",
            message="Test",
            priority=NotificationPriority.LOW
        )
        
        read = notification_manager.mark_as_read(notification["id"])
        
        assert read["status"] == "read"
        assert read["read_at"] is not None
    
    def test_get_user_notifications(self):
        """Test getting user notifications"""
        # Create multiple notifications
        for i in range(3):
            notification_manager.create_notification(
                user_id="test_user_2",
                notification_type=NotificationType.ALERT,
                title=f"Test {i}",
                message=f"Message {i}",
                priority=NotificationPriority.MEDIUM
            )
        
        notifications = notification_manager.get_user_notifications(
            user_id="test_user_2",
            limit=10
        )
        
        assert len(notifications) >= 3
    
    def test_notification_stats(self):
        """Test notification statistics"""
        stats = notification_manager.get_notification_stats("test_user")
        
        assert "total" in stats
        assert "unread" in stats
        assert "by_type" in stats


class TestNotificationTemplates:
    """Test notification templates"""
    
    def test_get_template(self):
        """Test getting a template"""
        template = notification_templates.get_template("budget_exceeded")
        
        assert template is not None
        assert "type" in template
        assert "title" in template
    
    def test_render_template(self):
        """Test rendering a template"""
        rendered = notification_templates.render_template(
            "budget_exceeded",
            {"category": "Dining", "amount": "5000"}
        )
        
        assert "Dining" in rendered["title"] or "Dining" in rendered["message"]
        assert "5000" in rendered["message"]
    
    def test_list_templates(self):
        """Test listing all templates"""
        templates = notification_templates.list_templates()
        
        assert len(templates) > 20
        assert "budget_exceeded" in templates


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
