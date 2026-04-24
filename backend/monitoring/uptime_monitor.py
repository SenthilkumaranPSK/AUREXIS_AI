"""
Uptime Monitoring Script

Checks if the server is running and sends alerts if down.
Can be run as a cron job or scheduled task.
"""

import requests
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import json
from pathlib import Path

# Configuration
SERVER_URL = "http://localhost:8000/health"
ALERT_EMAIL = "admin@example.com"  # Change this
CHECK_INTERVAL = 60  # seconds
LOG_FILE = Path(__file__).parent.parent / "logs" / "uptime.log"


def check_server():
    """Check if server is responding"""
    try:
        response = requests.get(SERVER_URL, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            status = data.get("status", "unknown")
            
            if status == "healthy":
                log_status("UP", "Server is healthy")
                return True
            else:
                log_status("DEGRADED", f"Server status: {status}")
                send_alert(f"Server degraded: {status}")
                return False
        else:
            log_status("DOWN", f"HTTP {response.status_code}")
            send_alert(f"Server returned HTTP {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        log_status("DOWN", "Request timeout")
        send_alert("Server timeout - not responding")
        return False
        
    except requests.exceptions.ConnectionError:
        log_status("DOWN", "Connection error")
        send_alert("Cannot connect to server")
        return False
        
    except Exception as e:
        log_status("ERROR", str(e))
        send_alert(f"Monitoring error: {str(e)}")
        return False


def log_status(status: str, message: str):
    """Log status to file"""
    timestamp = datetime.now().isoformat()
    log_entry = f"[{timestamp}] {status}: {message}\n"
    
    # Create logs directory if it doesn't exist
    LOG_FILE.parent.mkdir(exist_ok=True)
    
    # Append to log file
    with open(LOG_FILE, "a") as f:
        f.write(log_entry)
    
    print(log_entry.strip())


def send_alert(message: str):
    """Send alert email (configure SMTP settings)"""
    # TODO: Configure your SMTP settings
    # For now, just log the alert
    log_status("ALERT", message)
    
    # Example SMTP configuration (uncomment and configure):
    """
    try:
        msg = MIMEText(f"AUREXIS AI Alert\n\n{message}\n\nTime: {datetime.now()}")
        msg['Subject'] = 'AUREXIS AI Server Alert'
        msg['From'] = 'alerts@aurexis.ai'
        msg['To'] = ALERT_EMAIL
        
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login('your-email@gmail.com', 'your-app-password')
            server.send_message(msg)
    except Exception as e:
        log_status("ALERT_FAILED", f"Could not send email: {e}")
    """


def get_uptime_stats():
    """Calculate uptime statistics from log file"""
    if not LOG_FILE.exists():
        return {"uptime": 0, "total_checks": 0}
    
    with open(LOG_FILE, "r") as f:
        lines = f.readlines()
    
    total_checks = len(lines)
    up_count = sum(1 for line in lines if "UP" in line or "DEGRADED" in line)
    
    uptime_percentage = (up_count / total_checks * 100) if total_checks > 0 else 0
    
    return {
        "uptime_percentage": round(uptime_percentage, 2),
        "total_checks": total_checks,
        "up_count": up_count,
        "down_count": total_checks - up_count
    }


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "stats":
        # Show uptime statistics
        stats = get_uptime_stats()
        print("\n📊 Uptime Statistics:")
        print(f"  Uptime: {stats['uptime_percentage']}%")
        print(f"  Total checks: {stats['total_checks']}")
        print(f"  Up: {stats['up_count']}")
        print(f"  Down: {stats['down_count']}\n")
    else:
        # Run health check
        check_server()
