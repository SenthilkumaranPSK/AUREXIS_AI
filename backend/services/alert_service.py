"""
Alert Service
Business logic for generating and managing alerts
"""

from typing import List, Dict, Optional
from user_manager import get_all_user_data, get_user_by_id
from alerts import generate_alerts, generate_emis
from realtime_alerts import realtime_alert_system
from models.financial import FinancialModel


class AlertService:
    """Alert generation and management business logic"""
    
    @staticmethod
    def generate_alerts(user_id: str) -> Dict:
        """Generate alerts from data patterns"""
        data = get_all_user_data(user_id)
        alerts = generate_alerts(data)
        emis = generate_emis(data)
        
        # Store alerts in database
        for alert in alerts:
            try:
                FinancialModel.create_alert(
                    user_id=user_id,
                    alert_type=alert.get("type", "info"),
                    title=alert.get("title", "Alert"),
                    message=alert.get("message", ""),
                    severity=alert.get("severity", "info")
                )
            except Exception as e:
                print(f"Error storing alert: {e}")
        
        return {
            "alerts": alerts,
            "emis": emis,
            "count": len(alerts)
        }
    
    @staticmethod
    def generate_realtime_alerts(user_id: str) -> Dict:
        """Generate real-time financial alerts"""
        data = get_all_user_data(user_id)
        user_profile = get_user_by_id(user_id) or {}
        
        alerts = realtime_alert_system.generate_realtime_alerts(data, user_profile)
        summary = realtime_alert_system.get_alert_summary(alerts)
        
        # Store critical alerts in database
        for alert in alerts:
            if alert.get("severity") in ["critical", "high"]:
                try:
                    FinancialModel.create_alert(
                        user_id=user_id,
                        alert_type=alert.get("type", "info"),
                        title=alert.get("title", "Alert"),
                        message=alert.get("message", ""),
                        severity=alert.get("severity", "info")
                    )
                except Exception as e:
                    print(f"Error storing realtime alert: {e}")
        
        return {
            "alerts": alerts,
            "summary": summary,
            "user_id": user_id
        }
    
    @staticmethod
    def get_stored_alerts(user_id: str, is_read: Optional[bool] = None) -> List[Dict]:
        """Get alerts from database"""
        return FinancialModel.get_user_alerts(user_id, is_read)
    
    @staticmethod
    def mark_alert_read(alert_id: int) -> bool:
        """Mark alert as read"""
        return FinancialModel.mark_alert_as_read(alert_id)
    
    @staticmethod
    def get_unread_count(user_id: str) -> int:
        """Get count of unread alerts"""
        unread_alerts = FinancialModel.get_user_alerts(user_id, is_read=False)
        return len(unread_alerts)
