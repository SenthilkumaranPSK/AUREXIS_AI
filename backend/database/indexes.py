"""
Database Indexes for Performance Optimization
Create indexes on frequently queried columns
"""

import sqlite3
import logging
from database.connection_enhanced import get_db

logger = logging.getLogger(__name__)


INDEXES = [
    # Users table indexes
    "CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)",
    "CREATE INDEX IF NOT EXISTS idx_users_name ON users(name)",
    "CREATE INDEX IF NOT EXISTS idx_users_is_active ON users(is_active)",

    # Expenses table indexes
    "CREATE INDEX IF NOT EXISTS idx_expenses_user_id ON expenses(user_id)",
    "CREATE INDEX IF NOT EXISTS idx_expenses_date ON expenses(date)",
    "CREATE INDEX IF NOT EXISTS idx_expenses_category ON expenses(category)",
    "CREATE INDEX IF NOT EXISTS idx_expenses_user_date ON expenses(user_id, date)",

    # Monthly income table indexes
    "CREATE INDEX IF NOT EXISTS idx_monthly_income_user_id ON monthly_income(user_id)",
    "CREATE INDEX IF NOT EXISTS idx_monthly_income_month ON monthly_income(month)",
    "CREATE INDEX IF NOT EXISTS idx_monthly_income_user_month ON monthly_income(user_id, month)",

    # Goals table indexes
    "CREATE INDEX IF NOT EXISTS idx_goals_user_id ON goals(user_id)",
    "CREATE INDEX IF NOT EXISTS idx_goals_status ON goals(status)",
    "CREATE INDEX IF NOT EXISTS idx_goals_deadline ON goals(deadline)",

    # Alerts table indexes
    "CREATE INDEX IF NOT EXISTS idx_alerts_user_id ON alerts(user_id)",
    "CREATE INDEX IF NOT EXISTS idx_alerts_is_read ON alerts(is_read)",
    "CREATE INDEX IF NOT EXISTS idx_alerts_created_at ON alerts(created_at)",

    # Recommendations table indexes
    "CREATE INDEX IF NOT EXISTS idx_recommendations_user_id ON recommendations(user_id)",
    "CREATE INDEX IF NOT EXISTS idx_recommendations_status ON recommendations(status)",
    "CREATE INDEX IF NOT EXISTS idx_recommendations_category ON recommendations(category)",

    # Chat tables indexes
    "CREATE INDEX IF NOT EXISTS idx_chat_sessions_user_id ON chat_sessions(user_id)",
    "CREATE INDEX IF NOT EXISTS idx_chat_messages_session_id ON chat_messages(session_id)",
    "CREATE INDEX IF NOT EXISTS idx_chat_messages_created_at ON chat_messages(created_at)",

    # Health history indexes
    "CREATE INDEX IF NOT EXISTS idx_health_history_user_id ON health_history(user_id)",
    "CREATE INDEX IF NOT EXISTS idx_health_history_created_at ON health_history(created_at)",

    # Reports indexes
    "CREATE INDEX IF NOT EXISTS idx_reports_user_id ON reports(user_id)",
    "CREATE INDEX IF NOT EXISTS idx_reports_type ON reports(type)",

    # Refresh tokens indexes
    "CREATE INDEX IF NOT EXISTS idx_refresh_tokens_user_id ON refresh_tokens(user_id)",
    "CREATE INDEX IF NOT EXISTS idx_refresh_tokens_expires_at ON refresh_tokens(expires_at)",
    "CREATE INDEX IF NOT EXISTS idx_refresh_tokens_is_revoked ON refresh_tokens(is_revoked)",
]


def create_indexes():
    """Create all performance indexes"""
    conn = get_db_connection()
    cursor = conn.cursor()

    created = 0
    for index_sql in INDEXES:
        try:
            cursor.execute(index_sql)
            created += 1
        except sqlite3.Error as e:
            logger.warning(f"Index creation warning: {e}")

    conn.commit()
    conn.close()

    logger.info(f"Created/verified {created} database indexes")
    return created


def analyze_tables():
    """Run ANALYZE to update query planner statistics"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("ANALYZE")

    conn.commit()
    conn.close()

    logger.info("Database tables analyzed - query planner statistics updated")


if __name__ == "__main__":
    print("Creating database indexes...")
    create_indexes()
    print("Analyzing tables...")
    analyze_tables()
    print("Done!")
