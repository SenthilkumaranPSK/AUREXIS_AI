"""
Notification Templates
Pre-defined templates for common notifications
"""

from typing import Dict, Any
from .notification_manager import NotificationType, NotificationPriority


class NotificationTemplates:
    """Pre-defined notification templates"""
    
    def __init__(self):
        self.templates = {
            # Budget warnings
            "budget_exceeded": {
                "type": NotificationType.BUDGET_WARNING,
                "priority": NotificationPriority.HIGH,
                "title": "Budget Exceeded",
                "message": "You've exceeded your {category} budget by ₹{amount}",
                "channels": ["in_app", "push", "email"]
            },
            "budget_warning": {
                "type": NotificationType.BUDGET_WARNING,
                "priority": NotificationPriority.MEDIUM,
                "title": "Budget Warning",
                "message": "You've used {percentage}% of your {category} budget",
                "channels": ["in_app", "push"]
            },
            
            # Goal progress
            "goal_achieved": {
                "type": NotificationType.GOAL_PROGRESS,
                "priority": NotificationPriority.HIGH,
                "title": "🎉 Goal Achieved!",
                "message": "Congratulations! You've achieved your goal: {goal_name}",
                "channels": ["in_app", "push", "email"]
            },
            "goal_milestone": {
                "type": NotificationType.GOAL_PROGRESS,
                "priority": NotificationPriority.MEDIUM,
                "title": "Goal Milestone",
                "message": "You're {percentage}% towards your {goal_name} goal!",
                "channels": ["in_app", "push"]
            },
            "goal_behind": {
                "type": NotificationType.GOAL_PROGRESS,
                "priority": NotificationPriority.MEDIUM,
                "title": "Goal Update",
                "message": "You need to save ₹{amount}/month to reach {goal_name} on time",
                "channels": ["in_app", "push"]
            },
            
            # Transactions
            "large_transaction": {
                "type": NotificationType.TRANSACTION,
                "priority": NotificationPriority.HIGH,
                "title": "Large Transaction",
                "message": "₹{amount} {transaction_type} detected in {category}",
                "channels": ["in_app", "push", "sms"]
            },
            "unusual_transaction": {
                "type": NotificationType.ALERT,
                "priority": NotificationPriority.URGENT,
                "title": "⚠️ Unusual Transaction",
                "message": "Unusual transaction of ₹{amount} detected. Please verify.",
                "channels": ["in_app", "push", "email", "sms"]
            },
            "recurring_payment": {
                "type": NotificationType.TRANSACTION,
                "priority": NotificationPriority.LOW,
                "title": "Recurring Payment",
                "message": "Upcoming payment: {description} - ₹{amount} on {date}",
                "channels": ["in_app"]
            },
            
            # Insights
            "spending_spike": {
                "type": NotificationType.INSIGHT,
                "priority": NotificationPriority.MEDIUM,
                "title": "Spending Spike",
                "message": "Your {category} spending increased by {percentage}% this month",
                "channels": ["in_app", "push"]
            },
            "savings_opportunity": {
                "type": NotificationType.INSIGHT,
                "priority": NotificationPriority.MEDIUM,
                "title": "💡 Savings Opportunity",
                "message": "You could save ₹{amount}/month by {action}",
                "channels": ["in_app", "push"]
            },
            "pattern_detected": {
                "type": NotificationType.INSIGHT,
                "priority": NotificationPriority.LOW,
                "title": "Pattern Detected",
                "message": "{pattern_description}",
                "channels": ["in_app"]
            },
            
            # Recommendations
            "new_recommendation": {
                "type": NotificationType.RECOMMENDATION,
                "priority": NotificationPriority.MEDIUM,
                "title": "New Recommendation",
                "message": "{recommendation_title}",
                "channels": ["in_app", "push"]
            },
            "urgent_recommendation": {
                "type": NotificationType.RECOMMENDATION,
                "priority": NotificationPriority.HIGH,
                "title": "⚡ Urgent Recommendation",
                "message": "{recommendation_title}",
                "channels": ["in_app", "push", "email"]
            },
            
            # Alerts
            "low_balance": {
                "type": NotificationType.ALERT,
                "priority": NotificationPriority.HIGH,
                "title": "Low Balance Alert",
                "message": "Your balance is low: ₹{balance}. Consider transferring funds.",
                "channels": ["in_app", "push", "email"]
            },
            "emergency_fund_low": {
                "type": NotificationType.ALERT,
                "priority": NotificationPriority.HIGH,
                "title": "Emergency Fund Alert",
                "message": "Your emergency fund covers only {months} months of expenses",
                "channels": ["in_app", "push", "email"]
            },
            "debt_warning": {
                "type": NotificationType.ALERT,
                "priority": NotificationPriority.HIGH,
                "title": "Debt Warning",
                "message": "Your debt-to-income ratio is {ratio}%. Consider debt reduction.",
                "channels": ["in_app", "push", "email"]
            },
            
            # Investment
            "rebalance_needed": {
                "type": NotificationType.RECOMMENDATION,
                "priority": NotificationPriority.MEDIUM,
                "title": "Portfolio Rebalancing",
                "message": "Your portfolio has drifted {percentage}% from target allocation",
                "channels": ["in_app", "push"]
            },
            "investment_opportunity": {
                "type": NotificationType.RECOMMENDATION,
                "priority": NotificationPriority.MEDIUM,
                "title": "Investment Opportunity",
                "message": "{opportunity_description}",
                "channels": ["in_app", "push"]
            },
            "market_alert": {
                "type": NotificationType.ALERT,
                "priority": NotificationPriority.MEDIUM,
                "title": "Market Alert",
                "message": "{market_update}",
                "channels": ["in_app", "push"]
            },
            
            # Reports
            "report_ready": {
                "type": NotificationType.REPORT_READY,
                "priority": NotificationPriority.LOW,
                "title": "Report Ready",
                "message": "Your {report_type} report is ready to download",
                "channels": ["in_app", "email"]
            },
            "monthly_summary": {
                "type": NotificationType.REPORT_READY,
                "priority": NotificationPriority.MEDIUM,
                "title": "Monthly Summary",
                "message": "Your financial summary for {month} is ready",
                "channels": ["in_app", "email"]
            },
            
            # System
            "welcome": {
                "type": NotificationType.SYSTEM,
                "priority": NotificationPriority.MEDIUM,
                "title": "Welcome to AUREXIS AI! 🎉",
                "message": "Get started by adding your first transaction or setting a financial goal",
                "channels": ["in_app", "email"]
            },
            "security_alert": {
                "type": NotificationType.SYSTEM,
                "priority": NotificationPriority.URGENT,
                "title": "🔒 Security Alert",
                "message": "{security_message}",
                "channels": ["in_app", "push", "email", "sms"]
            },
            "password_changed": {
                "type": NotificationType.SYSTEM,
                "priority": NotificationPriority.HIGH,
                "title": "Password Changed",
                "message": "Your password was changed. If this wasn't you, contact support immediately.",
                "channels": ["in_app", "email", "sms"]
            }
        }
    
    def get_template(self, template_name: str) -> Dict:
        """Get a notification template"""
        return self.templates.get(template_name, {})
    
    def render_template(
        self,
        template_name: str,
        variables: Dict[str, Any]
    ) -> Dict:
        """
        Render a template with variables
        
        Args:
            template_name: Name of the template
            variables: Variables to substitute
            
        Returns:
            Rendered notification data
        """
        template = self.get_template(template_name)
        
        if not template:
            raise ValueError(f"Template '{template_name}' not found")
        
        # Render title and message
        title = template["title"].format(**variables)
        message = template["message"].format(**variables)
        
        return {
            "type": template["type"],
            "priority": template["priority"],
            "title": title,
            "message": message,
            "channels": template["channels"],
            "data": variables
        }
    
    def list_templates(self) -> Dict[str, Dict]:
        """List all available templates"""
        return {
            name: {
                "type": template["type"].value,
                "priority": template["priority"].value,
                "title": template["title"],
                "message": template["message"],
                "channels": template["channels"]
            }
            for name, template in self.templates.items()
        }
    
    def add_custom_template(
        self,
        name: str,
        template: Dict
    ) -> None:
        """Add a custom notification template"""
        self.templates[name] = {
            "type": NotificationType(template["type"]),
            "priority": NotificationPriority(template["priority"]),
            "title": template["title"],
            "message": template["message"],
            "channels": template.get("channels", ["in_app"])
        }


# Global instance
notification_templates = NotificationTemplates()
