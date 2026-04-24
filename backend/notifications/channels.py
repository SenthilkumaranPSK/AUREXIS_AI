"""
Notification Channels
Handles delivery through different channels
"""

from typing import Dict, Optional
from abc import ABC, abstractmethod


class NotificationChannel(ABC):
    """Base class for notification channels"""
    
    @abstractmethod
    def send(self, notification: Dict) -> Dict:
        """Send notification through this channel"""
        pass
    
    @abstractmethod
    def validate_config(self) -> bool:
        """Validate channel configuration"""
        pass


class InAppChannel(NotificationChannel):
    """In-app notification channel"""
    
    def send(self, notification: Dict) -> Dict:
        """
        Send in-app notification
        In production, this would store in database and use WebSocket
        """
        return {
            "success": True,
            "channel": "in_app",
            "notification_id": notification["id"],
            "message": "Notification stored for in-app display"
        }
    
    def validate_config(self) -> bool:
        return True


class PushChannel(NotificationChannel):
    """Push notification channel (Firebase, OneSignal, etc.)"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
    
    def send(self, notification: Dict) -> Dict:
        """
        Send push notification
        
        In production, integrate with:
        - Firebase Cloud Messaging (FCM)
        - Apple Push Notification Service (APNS)
        - OneSignal
        - Pusher
        """
        if not self.validate_config():
            return {
                "success": False,
                "error": "Push notifications not configured"
            }
        
        # Simulate push notification
        push_payload = {
            "title": notification["title"],
            "body": notification["message"],
            "data": notification.get("data", {}),
            "priority": "high" if notification["priority"] >= 3 else "normal",
            "badge": 1,
            "sound": "default"
        }
        
        return {
            "success": True,
            "channel": "push",
            "notification_id": notification["id"],
            "payload": push_payload,
            "message": "Push notification sent"
        }
    
    def validate_config(self) -> bool:
        # In production, check if API key is configured
        return True


class EmailChannel(NotificationChannel):
    """Email notification channel"""
    
    def __init__(
        self,
        smtp_host: Optional[str] = None,
        smtp_port: Optional[int] = None,
        smtp_user: Optional[str] = None,
        smtp_password: Optional[str] = None
    ):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
    
    def send(self, notification: Dict) -> Dict:
        """
        Send email notification
        
        In production, integrate with:
        - SendGrid
        - AWS SES
        - Mailgun
        - Postmark
        """
        if not self.validate_config():
            return {
                "success": False,
                "error": "Email not configured"
            }
        
        # Simulate email sending
        email_data = {
            "to": notification.get("data", {}).get("email", "user@example.com"),
            "subject": notification["title"],
            "body": notification["message"],
            "html": self._generate_html_email(notification),
            "priority": notification["priority"]
        }
        
        return {
            "success": True,
            "channel": "email",
            "notification_id": notification["id"],
            "email_data": email_data,
            "message": "Email sent"
        }
    
    def validate_config(self) -> bool:
        # In production, check SMTP configuration
        return True
    
    def _generate_html_email(self, notification: Dict) -> str:
        """Generate HTML email template"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #4F46E5; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background: #f9fafb; }}
                .footer {{ padding: 20px; text-align: center; color: #6b7280; font-size: 12px; }}
                .button {{ background: #4F46E5; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>AUREXIS AI</h1>
                </div>
                <div class="content">
                    <h2>{notification['title']}</h2>
                    <p>{notification['message']}</p>
                    <p><a href="https://aurexis.ai/notifications" class="button">View in App</a></p>
                </div>
                <div class="footer">
                    <p>You received this email because you have notifications enabled.</p>
                    <p><a href="https://aurexis.ai/settings/notifications">Manage Preferences</a></p>
                </div>
            </div>
        </body>
        </html>
        """


class SMSChannel(NotificationChannel):
    """SMS notification channel"""
    
    def __init__(
        self,
        account_sid: Optional[str] = None,
        auth_token: Optional[str] = None,
        from_number: Optional[str] = None
    ):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.from_number = from_number
    
    def send(self, notification: Dict) -> Dict:
        """
        Send SMS notification
        
        In production, integrate with:
        - Twilio
        - AWS SNS
        - Nexmo/Vonage
        - MessageBird
        """
        if not self.validate_config():
            return {
                "success": False,
                "error": "SMS not configured"
            }
        
        # Simulate SMS sending
        phone = notification.get("data", {}).get("phone", "+1234567890")
        message = f"{notification['title']}: {notification['message']}"
        
        # Truncate to SMS length
        if len(message) > 160:
            message = message[:157] + "..."
        
        sms_data = {
            "to": phone,
            "from": self.from_number or "+1234567890",
            "body": message
        }
        
        return {
            "success": True,
            "channel": "sms",
            "notification_id": notification["id"],
            "sms_data": sms_data,
            "message": "SMS sent"
        }
    
    def validate_config(self) -> bool:
        # In production, check Twilio/SMS configuration
        return True


class WebSocketChannel(NotificationChannel):
    """WebSocket channel for real-time notifications"""
    
    def __init__(self):
        self.connections: Dict[str, list] = {}  # user_id -> [websocket connections]
    
    def send(self, notification: Dict) -> Dict:
        """
        Send notification via WebSocket
        
        In production, integrate with:
        - Socket.IO
        - WebSocket native
        - Pusher
        - Ably
        """
        user_id = notification["user_id"]
        
        # Get user's active connections
        connections = self.connections.get(user_id, [])
        
        if not connections:
            return {
                "success": False,
                "channel": "websocket",
                "error": "No active connections for user"
            }
        
        # Simulate sending to all connections
        sent_count = len(connections)
        
        return {
            "success": True,
            "channel": "websocket",
            "notification_id": notification["id"],
            "connections_count": sent_count,
            "message": f"Sent to {sent_count} active connection(s)"
        }
    
    def validate_config(self) -> bool:
        return True
    
    def add_connection(self, user_id: str, connection):
        """Add a WebSocket connection for a user"""
        if user_id not in self.connections:
            self.connections[user_id] = []
        self.connections[user_id].append(connection)
    
    def remove_connection(self, user_id: str, connection):
        """Remove a WebSocket connection"""
        if user_id in self.connections:
            self.connections[user_id] = [
                c for c in self.connections[user_id]
                if c != connection
            ]


class NotificationChannels:
    """Manages all notification channels"""
    
    def __init__(self):
        self.channels = {
            "in_app": InAppChannel(),
            "push": PushChannel(),
            "email": EmailChannel(),
            "sms": SMSChannel(),
            "websocket": WebSocketChannel()
        }
    
    def get_channel(self, channel_name: str) -> Optional[NotificationChannel]:
        """Get a notification channel by name"""
        return self.channels.get(channel_name)
    
    def send(self, notification: Dict, channel_name: str) -> Dict:
        """Send notification through a specific channel"""
        channel = self.get_channel(channel_name)
        
        if not channel:
            return {
                "success": False,
                "error": f"Channel '{channel_name}' not found"
            }
        
        try:
            return channel.send(notification)
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def validate_all(self) -> Dict[str, bool]:
        """Validate all channel configurations"""
        return {
            name: channel.validate_config()
            for name, channel in self.channels.items()
        }


# Global instance
notification_channels = NotificationChannels()
