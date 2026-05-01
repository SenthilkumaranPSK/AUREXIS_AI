"""
Recommendation Service
Generate and manage financial recommendations for users
"""

from typing import List, Dict, Optional
from datetime import datetime
import logging
from database.db_utils import get_db

logger = logging.getLogger(__name__)


class RecommendationService:
    """Generate personalized financial recommendations"""
    
    @staticmethod
    def get_stored_recommendations(
        user_id: str,
        status: Optional[str] = None
    ) -> List[Dict]:
        """
        Get stored recommendations for a user
        
        Args:
            user_id: User identifier
            status: Filter by status (pending, accepted, rejected)
            
        Returns:
            List of recommendation dictionaries
        """
        try:
            with get_db() as conn:
                cursor = conn.cursor()
                
                if status:
                    cursor.execute("""
                        SELECT id, user_id, category, title, description,
                               priority, impact, status, created_at
                        FROM recommendations
                        WHERE user_id = ? AND status = ?
                        ORDER BY created_at DESC
                    """, (user_id, status))
                else:
                    cursor.execute("""
                        SELECT id, user_id, category, title, description,
                               priority, impact, status, created_at
                        FROM recommendations
                        WHERE user_id = ?
                        ORDER BY created_at DESC
                    """, (user_id,))
                
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error fetching recommendations: {e}")
            return []
    
    @staticmethod
    def get_recommendation_by_id(rec_id: int) -> Optional[Dict]:
        """Get a single recommendation by ID"""
        try:
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, user_id, category, title, description,
                           priority, impact, status, created_at
                    FROM recommendations
                    WHERE id = ?
                """, (rec_id,))
                row = cursor.fetchone()
                return dict(row) if row else None
        except Exception as e:
            logger.error(f"Error fetching recommendation: {e}")
            return None
    
    @staticmethod
    def generate_recommendations(user_id: str) -> List[Dict]:
        """
        Generate new recommendations based on user's financial data
        
        Args:
            user_id: User identifier
            
        Returns:
            List of generated recommendations
        """
        recommendations = []
        
        try:
            with get_db() as conn:
                cursor = conn.cursor()
                
                # Get user's financial data
                cursor.execute("""
                    SELECT SUM(amount) as total_expenses
                    FROM expenses
                    WHERE user_id = ? AND date >= date('now', '-30 days')
                """, (user_id,))
                expense_data = cursor.fetchone()
                total_expenses = expense_data['total_expenses'] if expense_data else 0
                
                cursor.execute("""
                    SELECT amount as monthly_income
                    FROM monthly_income
                    WHERE user_id = ?
                    ORDER BY month DESC
                    LIMIT 1
                """, (user_id,))
                income_data = cursor.fetchone()
                monthly_income = income_data['monthly_income'] if income_data else 0
                
                # Generate recommendations based on spending patterns
                if monthly_income > 0:
                    savings_rate = ((monthly_income - total_expenses) / monthly_income) * 100
                    
                    if savings_rate < 20:
                        recommendations.append({
                            "category": "savings",
                            "title": "Increase Your Savings Rate",
                            "description": f"Your current savings rate is {savings_rate:.1f}%. Aim for at least 20% to build financial security.",
                            "priority": "high",
                            "impact": "high"
                        })
                    
                    if total_expenses > monthly_income:
                        recommendations.append({
                            "category": "budget",
                            "title": "Reduce Monthly Expenses",
                            "description": "Your expenses exceed your income. Review your spending categories and identify areas to cut back.",
                            "priority": "critical",
                            "impact": "high"
                        })
                
                # Check for emergency fund
                cursor.execute("""
                    SELECT COUNT(*) as goal_count
                    FROM goals
                    WHERE user_id = ? AND name LIKE '%emergency%' AND status = 'active'
                """, (user_id,))
                emergency_goal = cursor.fetchone()
                
                if emergency_goal['goal_count'] == 0:
                    recommendations.append({
                        "category": "emergency_fund",
                        "title": "Build an Emergency Fund",
                        "description": "Set up an emergency fund covering 3-6 months of expenses for financial security.",
                        "priority": "high",
                        "impact": "high"
                    })
                
                # Store recommendations in database
                for rec in recommendations:
                    cursor.execute("""
                        INSERT INTO recommendations 
                        (user_id, category, title, description, priority, impact, status)
                        VALUES (?, ?, ?, ?, ?, ?, 'pending')
                    """, (
                        user_id,
                        rec['category'],
                        rec['title'],
                        rec['description'],
                        rec['priority'],
                        rec['impact']
                    ))
                
                conn.commit()
                logger.info(f"Generated {len(recommendations)} recommendations for user {user_id}")
                
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
        
        return recommendations
    
    @staticmethod
    def update_recommendation_status(rec_id: int, status: str) -> bool:
        """
        Update recommendation status
        
        Args:
            rec_id: Recommendation ID
            status: New status (pending, accepted, rejected)
            
        Returns:
            True if successful
        """
        try:
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE recommendations
                    SET status = ?
                    WHERE id = ?
                """, (status, rec_id))
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error updating recommendation status: {e}")
            return False
    
    @staticmethod
    def create_recommendation(
        user_id: str,
        category: str,
        title: str,
        description: str,
        priority: str = "medium",
        impact: str = "medium"
    ) -> Optional[Dict]:
        """Create a new recommendation"""
        try:
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO recommendations 
                    (user_id, category, title, description, priority, impact, status)
                    VALUES (?, ?, ?, ?, ?, ?, 'pending')
                """, (user_id, category, title, description, priority, impact))
                
                rec_id = cursor.lastrowid
                conn.commit()
                
                return {
                    "id": rec_id,
                    "user_id": user_id,
                    "category": category,
                    "title": title,
                    "description": description,
                    "priority": priority,
                    "impact": impact,
                    "status": "pending",
                    "created_at": datetime.now().isoformat()
                }
        except Exception as e:
            logger.error(f"Error creating recommendation: {e}")
            return None
