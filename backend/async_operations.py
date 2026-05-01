"""
Async Operations for AUREXIS AI
Ensures all I/O operations are properly async for better performance
"""

import asyncio
import aiofiles
import httpx
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
import logging

from database.connection_enhanced import get_async_db, DatabaseManager
from exceptions import DatabaseError, ExternalServiceError
from config_enhanced import settings

logger = logging.getLogger(__name__)


class AsyncUserManager:
    """Async user management operations"""
    
    @staticmethod
    async def get_user_by_id_async(user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID asynchronously"""
        try:
            query = "SELECT * FROM users WHERE id = ? AND is_active = 1"
            result = await DatabaseManager.execute_async_query(query, (user_id,), fetch_one=True)
            
            if result:
                result.pop("password_hash", None)  # Remove sensitive data
            return result
            
        except Exception as e:
            logger.error(f"Error getting user by ID async: {e}")
            raise DatabaseError("Failed to retrieve user")
    
    @staticmethod
    async def get_user_by_email_async(email: str) -> Optional[Dict[str, Any]]:
        """Get user by email asynchronously"""
        try:
            query = "SELECT * FROM users WHERE email = ? AND is_active = 1"
            result = await DatabaseManager.execute_async_query(query, (email,), fetch_one=True)
            
            if result:
                result.pop("password_hash", None)
            return result
            
        except Exception as e:
            logger.error(f"Error getting user by email async: {e}")
            raise DatabaseError("Failed to retrieve user")
    
    @staticmethod
    async def authenticate_user_async(username: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user asynchronously"""
        try:
            # Import here to avoid circular imports
            from user_manager_secure import UserManager
            
            user = await AsyncUserManager.get_user_by_email_async(username)
            if not user:
                user = await AsyncUserManager.get_user_by_id_async(username)
            
            if not user:
                return None
            
            # Verify password (this part remains sync for now)
            with DatabaseManager.get_db() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT password_hash FROM users WHERE id = ?", (user["id"],))
                row = cursor.fetchone()
                if not row:
                    return None
                
                if not UserManager.verify_password(password, row["password_hash"]):
                    return None
            
            # Update last login
            await AsyncUserManager.update_last_login_async(user["id"])
            
            # Add financial data
            user["financial_data"] = await AsyncUserManager.get_all_user_data_async(user["id"])
            
            return user
            
        except Exception as e:
            logger.error(f"Async authentication error: {e}")
            raise DatabaseError("Authentication failed")
    
    @staticmethod
    async def update_last_login_async(user_id: str) -> None:
        """Update last login asynchronously"""
        try:
            query = "UPDATE users SET last_login = ? WHERE id = ?"
            await DatabaseManager.execute_async_update(query, (datetime.now().isoformat(), user_id))
        except Exception as e:
            logger.error(f"Error updating last login async: {e}")
    
    @staticmethod
    async def get_all_users_async() -> List[Dict[str, Any]]:
        """Get all users asynchronously"""
        try:
            query = """
                SELECT id, name, email, occupation, age, location, user_number,
                       is_active, is_verified, created_at, last_login
                FROM users 
                WHERE is_active = 1
                ORDER BY created_at DESC
            """
            return await DatabaseManager.execute_async_query(query, fetch_all=True)
            
        except Exception as e:
            logger.error(f"Error getting all users async: {e}")
            raise DatabaseError("Failed to retrieve users")
    
    @staticmethod
    async def get_all_user_data_async(user_id: str) -> Dict[str, Any]:
        """Get all user data asynchronously"""
        try:
            # Load JSON data files asynchronously
            data_types = [
                "fetch_bank_transactions",
                "fetch_credit_report",
                "fetch_epf_details",
                "fetch_mf_transactions",
                "fetch_net_worth",
                "fetch_stock_transactions",
            ]
            
            result = {"user_id": user_id}
            tasks = []
            
            for data_type in data_types:
                task = asyncio.create_task(
                    AsyncUserManager.load_user_data_async(user_id, data_type)
                )
                tasks.append((data_type, task))
            
            # Wait for all tasks to complete
            for data_type, task in tasks:
                try:
                    data = await task
                    if data:
                        result[data_type] = data
                except Exception as e:
                    logger.warning(f"Failed to load {data_type} for user {user_id}: {e}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error getting all user data async: {e}")
            return {"user_id": user_id}
    
    @staticmethod
    async def load_user_data_async(user_id: str, data_type: str) -> Optional[Dict[str, Any]]:
        """Load user data file asynchronously"""
        try:
            from pathlib import Path
            import json
            
            data_file = Path(__file__).parent / "user_data" / user_id / f"{data_type}.json"
            
            if not data_file.exists():
                return None
            
            async with aiofiles.open(data_file, 'r') as f:
                content = await f.read()
                return json.loads(content)
                
        except Exception as e:
            logger.error(f"Error loading user data async: {e}")
            return None


class AsyncFinancialOperations:
    """Async financial data operations"""
    
    @staticmethod
    async def get_user_transactions_async(user_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get user transactions asynchronously"""
        try:
            query = """
                SELECT * FROM expenses 
                WHERE user_id = ? 
                ORDER BY date DESC 
                LIMIT ?
            """
            return await DatabaseManager.execute_async_query(query, (user_id, limit), fetch_all=True)
            
        except Exception as e:
            logger.error(f"Error getting transactions async: {e}")
            raise DatabaseError("Failed to retrieve transactions")
    
    @staticmethod
    async def get_user_income_async(user_id: str, months: int = 12) -> List[Dict[str, Any]]:
        """Get user income data asynchronously"""
        try:
            query = """
                SELECT * FROM monthly_income 
                WHERE user_id = ? 
                ORDER BY month DESC 
                LIMIT ?
            """
            return await DatabaseManager.execute_async_query(query, (user_id, months), fetch_all=True)
            
        except Exception as e:
            logger.error(f"Error getting income async: {e}")
            raise DatabaseError("Failed to retrieve income data")
    
    @staticmethod
    async def get_user_goals_async(user_id: str) -> List[Dict[str, Any]]:
        """Get user goals asynchronously"""
        try:
            query = "SELECT * FROM goals WHERE user_id = ? ORDER BY deadline ASC"
            return await DatabaseManager.execute_async_query(query, (user_id,), fetch_all=True)
            
        except Exception as e:
            logger.error(f"Error getting goals async: {e}")
            raise DatabaseError("Failed to retrieve goals")
    
    @staticmethod
    async def add_transaction_async(transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add transaction asynchronously"""
        try:
            query = """
                INSERT INTO expenses (user_id, date, amount, category, description, merchant, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            
            params = (
                transaction_data["user_id"],
                transaction_data["date"],
                float(transaction_data["amount"]),
                transaction_data["category"],
                transaction_data.get("description"),
                transaction_data.get("merchant"),
                datetime.now().isoformat()
            )
            
            await DatabaseManager.execute_async_update(query, params)
            
            # Return the created transaction
            return transaction_data
            
        except Exception as e:
            logger.error(f"Error adding transaction async: {e}")
            raise DatabaseError("Failed to add transaction")
    
    @staticmethod
    async def add_income_async(income_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add income asynchronously"""
        try:
            query = """
                INSERT INTO monthly_income (user_id, month, amount, source, created_at)
                VALUES (?, ?, ?, ?, ?)
            """
            
            params = (
                income_data["user_id"],
                income_data["month"],
                float(income_data["amount"]),
                income_data.get("source"),
                datetime.now().isoformat()
            )
            
            await DatabaseManager.execute_async_update(query, params)
            
            return income_data
            
        except Exception as e:
            logger.error(f"Error adding income async: {e}")
            raise DatabaseError("Failed to add income")
    
    @staticmethod
    async def update_goal_async(goal_id: int, updates: Dict[str, Any]) -> bool:
        """Update goal asynchronously"""
        try:
            set_clauses = []
            params = []
            
            for key, value in updates.items():
                set_clauses.append(f"{key} = ?")
                params.append(value)
            
            if not set_clauses:
                return False
            
            set_clauses.append("updated_at = ?")
            params.append(datetime.now().isoformat())
            params.append(goal_id)
            
            query = f"UPDATE goals SET {', '.join(set_clauses)} WHERE id = ?"
            rows_affected = await DatabaseManager.execute_async_update(query, tuple(params))
            
            return rows_affected > 0
            
        except Exception as e:
            logger.error(f"Error updating goal async: {e}")
            raise DatabaseError("Failed to update goal")


class AsyncChatOperations:
    """Async chat operations"""
    
    @staticmethod
    async def save_message_async(
        session_id: str,
        user_id: str,
        role: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Save chat message asynchronously"""
        try:
            import json
            
            query = """
                INSERT INTO chat_messages (session_id, role, content, metadata, created_at)
                VALUES (?, ?, ?, ?, ?)
            """
            
            metadata_json = json.dumps(metadata) if metadata else None
            
            params = (
                session_id,
                role,
                content,
                metadata_json,
                datetime.now().isoformat()
            )
            
            await DatabaseManager.execute_async_update(query, params)
            
            return {
                "session_id": session_id,
                "role": role,
                "content": content,
                "metadata": metadata,
                "created_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error saving message async: {e}")
            raise DatabaseError("Failed to save message")
    
    @staticmethod
    async def get_chat_history_async(
        session_id: str,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Get chat history asynchronously"""
        try:
            query = """
                SELECT * FROM chat_messages 
                WHERE session_id = ? 
                ORDER BY created_at ASC 
                LIMIT ?
            """
            messages = await DatabaseManager.execute_async_query(query, (session_id, limit), fetch_all=True)
            
            # Parse metadata JSON
            for message in messages:
                if message.get("metadata"):
                    try:
                        import json
                        message["metadata"] = json.loads(message["metadata"])
                    except:
                        message["metadata"] = None
            
            return messages
            
        except Exception as e:
            logger.error(f"Error getting chat history async: {e}")
            raise DatabaseError("Failed to retrieve chat history")
    
    @staticmethod
    async def create_session_async(
        user_id: str,
        title: Optional[str] = None
    ) -> str:
        """Create chat session asynchronously"""
        try:
            import uuid
            
            session_id = str(uuid.uuid4())
            
            query = """
                INSERT INTO chat_sessions (id, user_id, title, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
            """
            
            params = (
                session_id,
                user_id,
                title or f"Chat {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                datetime.now().isoformat(),
                datetime.now().isoformat()
            )
            
            await DatabaseManager.execute_async_update(query, params)
            
            return session_id
            
        except Exception as e:
            logger.error(f"Error creating session async: {e}")
            raise DatabaseError("Failed to create session")


class AsyncExternalServiceOperations:
    """Async operations for external services"""
    
    @staticmethod
    async def call_ollama_async(
        message: str,
        user_context: Dict[str, Any],
        financial_data: Dict[str, Any],
        model: Optional[str] = None
    ) -> Dict[str, Any]:
        """Call Ollama API asynchronously"""
        try:
            model = model or settings.OLLAMA_MODEL
            
            # Prepare prompt with user context
            prompt = f"""
            You are AUREXIS AI, a financial advisor assistant. 
            User: {user_context.get('name', 'User')}
            Financial Data Available: {bool(financial_data)}
            
            User Message: {message}
            
            Provide helpful financial advice based on the available data.
            """
            
            async with httpx.AsyncClient(timeout=settings.OLLAMA_TIMEOUT) as client:
                response = await client.post(
                    f"{settings.OLLAMA_BASE_URL}/api/generate",
                    json={
                        "model": model,
                        "prompt": prompt,
                        "stream": False
                    }
                )
                
                if response.status_code != 200:
                    raise ExternalServiceError(
                        "Ollama",
                        f"API returned status {response.status_code}"
                    )
                
                result = response.json()
                
                return {
                    "content": result.get("response", ""),
                    "model": model,
                    "confidence": 0.8,  # Placeholder confidence
                    "timestamp": datetime.now().isoformat()
                }
                
        except httpx.TimeoutException:
            raise ExternalServiceError("Ollama", "Request timeout")
        except httpx.RequestError as e:
            raise ExternalServiceError("Ollama", f"Request failed: {e}")
        except Exception as e:
            logger.error(f"Error calling Ollama async: {e}")
            raise ExternalServiceError("Ollama", "Service unavailable")
    
    @staticmethod
    async def send_email_async(
        to_email: str,
        subject: str,
        body: str,
        is_html: bool = False
    ) -> bool:
        """Send email asynchronously (placeholder implementation)"""
        try:
            # This would integrate with an email service like SendGrid, AWS SES, etc.
            # For now, just log the email
            logger.info(f"Email to {to_email}: {subject}")
            
            # Simulate async operation
            await asyncio.sleep(0.1)
            
            return True
            
        except Exception as e:
            logger.error(f"Error sending email async: {e}")
            return False
    
    @staticmethod
    async def generate_report_async(
        user_id: str,
        report_type: str,
        format_type: str = "pdf"
    ) -> Dict[str, Any]:
        """Generate report asynchronously"""
        try:
            # This would integrate with a report generation service
            # For now, simulate the operation
            
            await asyncio.sleep(1)  # Simulate processing time
            
            return {
                "user_id": user_id,
                "report_type": report_type,
                "format": format_type,
                "status": "completed",
                "file_path": f"/reports/{user_id}_{report_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format_type}",
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating report async: {e}")
            raise DatabaseError("Failed to generate report")


class AsyncCacheOperations:
    """Async cache operations"""
    
    @staticmethod
    async def get_cached_data_async(key: str) -> Optional[Any]:
        """Get cached data asynchronously"""
        try:
            # This would integrate with Redis or another cache system
            # For now, just return None (no cache)
            return None
            
        except Exception as e:
            logger.error(f"Error getting cached data async: {e}")
            return None
    
    @staticmethod
    async def set_cached_data_async(
        key: str,
        data: Any,
        ttl: int = 300
    ) -> bool:
        """Set cached data asynchronously"""
        try:
            # This would integrate with Redis or another cache system
            # For now, just return True (success)
            return True
            
        except Exception as e:
            logger.error(f"Error setting cached data async: {e}")
            return False
    
    @staticmethod
    async def delete_cached_data_async(key: str) -> bool:
        """Delete cached data asynchronously"""
        try:
            # This would integrate with Redis or another cache system
            # For now, just return True (success)
            return True
            
        except Exception as e:
            logger.error(f"Error deleting cached data async: {e}")
            return False


# Utility functions for batch operations
class AsyncBatchOperations:
    """Batch async operations for better performance"""
    
    @staticmethod
    async def process_multiple_users_async(
        user_ids: List[str],
        operation: str,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """Process operation for multiple users concurrently"""
        try:
            tasks = []
            
            for user_id in user_ids:
                if operation == "get_user_data":
                    task = AsyncUserManager.get_all_user_data_async(user_id)
                elif operation == "get_transactions":
                    task = AsyncFinancialOperations.get_user_transactions_async(
                        user_id, kwargs.get("limit", 100)
                    )
                elif operation == "get_goals":
                    task = AsyncFinancialOperations.get_user_goals_async(user_id)
                else:
                    continue
                
                tasks.append(task)
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Filter out exceptions and format results
            formatted_results = []
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    logger.error(f"Error processing user {user_ids[i]}: {result}")
                    formatted_results.append({"user_id": user_ids[i], "error": str(result)})
                else:
                    formatted_results.append(result)
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error in batch operation: {e}")
            raise DatabaseError("Batch operation failed")
    
    @staticmethod
    async def calculate_financial_metrics_async(
        user_id: str
    ) -> Dict[str, Any]:
        """Calculate financial metrics concurrently"""
        try:
            # Run multiple calculations concurrently
            tasks = [
                AsyncFinancialOperations.get_user_transactions_async(user_id, 1000),
                AsyncFinancialOperations.get_user_income_async(user_id, 24),
                AsyncFinancialOperations.get_user_goals_async(user_id),
            ]
            
            transactions, income, goals = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Calculate metrics
            total_expenses = sum(t["amount"] for t in transactions if isinstance(transactions, list))
            total_income = sum(i["amount"] for i in income if isinstance(income, list))
            active_goals = len([g for g in goals if isinstance(goals, list) and g.get("status") == "active"])
            
            return {
                "user_id": user_id,
                "total_expenses": total_expenses,
                "total_income": total_income,
                "net_income": total_income - total_expenses,
                "active_goals": active_goals,
                "calculated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error calculating financial metrics async: {e}")
            raise DatabaseError("Failed to calculate metrics")
