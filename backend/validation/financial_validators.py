"""
Financial Data Validation for AUREXIS AI
Comprehensive validation for all financial inputs and operations
"""

import re
from datetime import datetime, date
from typing import Dict, Any, List, Optional, Union
from decimal import Decimal, InvalidOperation
from pydantic import BaseModel, Field, validator
from enum import Enum

from exceptions import ValidationError


class TransactionType(str, Enum):
    """Transaction types"""
    DEBIT = "debit"
    CREDIT = "credit"


class ExpenseCategory(str, Enum):
    """Valid expense categories"""
    FOOD = "Food"
    TRANSPORTATION = "Transportation"
    HOUSING = "Housing"
    UTILITIES = "Utilities"
    HEALTHCARE = "Healthcare"
    ENTERTAINMENT = "Entertainment"
    SHOPPING = "Shopping"
    EDUCATION = "Education"
    INSURANCE = "Insurance"
    TAXES = "Taxes"
    DEBT_PAYMENT = "Debt Payment"
    SAVINGS = "Savings"
    INVESTMENT = "Investment"
    OTHER = "Other"


class GoalStatus(str, Enum):
    """Goal status values"""
    ACTIVE = "active"
    COMPLETED = "completed"
    PAUSED = "paused"


class AlertSeverity(str, Enum):
    """Alert severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class BaseFinancialValidator(BaseModel):
    """Base validator with common financial validations"""
    
    @validator('*', pre=True)
    def strip_strings(cls, v):
        """Strip whitespace from string inputs"""
        if isinstance(v, str):
            return v.strip()
        return v
    
    @validator('*', pre=True)
    def validate_none_values(cls, v):
        """Convert empty strings to None"""
        if isinstance(v, str) and v == "":
            return None
        return v


class TransactionValidator(BaseFinancialValidator):
    """Validator for financial transactions"""
    
    amount: Decimal = Field(..., gt=0, description="Transaction amount must be positive")
    date: date = Field(..., description="Transaction date")
    category: ExpenseCategory = Field(..., description="Expense category")
    description: Optional[str] = Field(None, min_length=2, max_length=500, description="Transaction description")
    merchant: Optional[str] = Field(None, min_length=2, max_length=200, description="Merchant name")
    transaction_type: TransactionType = Field(TransactionType.DEBIT, description="Transaction type")
    
    @validator('amount')
    def validate_amount_precision(cls, v):
        """Validate amount has reasonable precision"""
        if v.as_tuple().exponent < -2:  # More than 2 decimal places
            raise ValueError("Amount cannot have more than 2 decimal places")
        if v > 999999999.99:  # Reasonable upper limit
            raise ValueError("Amount exceeds maximum allowed value")
        return v
    
    @validator('date')
    def validate_date_range(cls, v):
        """Validate date is within reasonable range"""
        today = date.today()
        if v > today:
            raise ValueError("Transaction date cannot be in the future")
        min_date = date(1900, 1, 1)
        if v < min_date:
            raise ValueError("Transaction date is too far in the past")
        return v
    
    @validator('description')
    def validate_description_content(cls, v):
        """Validate description doesn't contain malicious content"""
        if v and any(char in v for char in ['<', '>', '{', '}', '[', ']', '|', '\\']):
            raise ValueError("Description contains invalid characters")
        return v


class IncomeValidator(BaseFinancialValidator):
    """Validator for income data"""
    
    amount: Decimal = Field(..., gt=0, description="Income amount must be positive")
    month: date = Field(..., description="Income month")
    source: Optional[str] = Field(None, min_length=2, max_length=100, description="Income source")
    
    @validator('amount')
    def validate_income_amount(cls, v):
        """Validate income amount"""
        if v > 100000000:  # $100M monthly income seems unreasonable
            raise ValueError("Income amount exceeds reasonable limits")
        return v
    
    @validator('month')
    def validate_income_month(cls, v):
        """Ensure month is first day of month"""
        if v.day != 1:
            raise ValueError("Income month must be the first day of the month")
        return v


class GoalValidator(BaseFinancialValidator):
    """Validator for financial goals"""
    
    name: str = Field(..., min_length=2, max_length=200, description="Goal name")
    target_amount: Decimal = Field(..., gt=0, description="Target amount")
    current_amount: Decimal = Field(0, ge=0, description="Current progress amount")
    deadline: Optional[date] = Field(None, description="Goal deadline")
    category: Optional[str] = Field(None, min_length=2, max_length=100, description="Goal category")
    status: GoalStatus = Field(GoalStatus.ACTIVE, description="Goal status")
    
    @validator('target_amount')
    def validate_target_amount(cls, v):
        """Validate target amount"""
        if v > 10000000000:  # $10B seems unreasonable for personal goals
            raise ValueError("Target amount exceeds reasonable limits")
        return v
    
    @validator('current_amount')
    def validate_current_amount(cls, v, values):
        """Validate current amount doesn't exceed target"""
        if 'target_amount' in values and v > values['target_amount']:
            raise ValueError("Current amount cannot exceed target amount")
        return v
    
    @validator('deadline')
    def validate_deadline(cls, v):
        """Validate deadline is in the future"""
        if v and v <= date.today():
            raise ValueError("Goal deadline must be in the future")
        return v
    
    @validator('name')
    def validate_goal_name(cls, v):
        """Validate goal name doesn't contain malicious content"""
        if any(char in v for char in ['<', '>', '{', '}', '[', ']', '|', '\\']):
            raise ValueError("Goal name contains invalid characters")
        return v


class AlertValidator(BaseFinancialValidator):
    """Validator for financial alerts"""
    
    type: str = Field(..., min_length=2, max_length=50, description="Alert type")
    title: str = Field(..., min_length=2, max_length=200, description="Alert title")
    message: str = Field(..., min_length=2, max_length=1000, description="Alert message")
    severity: AlertSeverity = Field(..., description="Alert severity")
    
    @validator('title', 'message')
    def validate_alert_content(cls, v):
        """Validate alert content doesn't contain malicious content"""
        if any(char in v for char in ['<', '>', '{', '}', '[', ']', '|', '\\']):
            raise ValueError("Alert content contains invalid characters")
        return v


class BudgetValidator(BaseFinancialValidator):
    """Validator for budget data"""
    
    category: ExpenseCategory = Field(..., description="Budget category")
    allocated_amount: Decimal = Field(..., gt=0, description="Allocated budget amount")
    period: str = Field(..., regex=r'^(weekly|monthly|quarterly|yearly)$', description="Budget period")
    
    @validator('allocated_amount')
    def validate_budget_amount(cls, v):
        """Validate budget amount"""
        if v > 10000000:  # $10M monthly budget seems unreasonable
            raise ValueError("Budget amount exceeds reasonable limits")
        return v


class InvestmentValidator(BaseFinancialValidator):
    """Validator for investment data"""
    
    symbol: str = Field(..., min_length=1, max_length=10, regex=r'^[A-Z]+$', description="Stock symbol")
    quantity: int = Field(..., gt=0, description="Number of shares")
    price_per_share: Decimal = Field(..., gt=0, description="Price per share")
    purchase_date: date = Field(..., description="Purchase date")
    
    @validator('symbol')
    def validate_symbol(cls, v):
        """Validate stock symbol format"""
        if not re.match(r'^[A-Z]{1,10}$', v):
            raise ValueError("Invalid stock symbol format")
        return v
    
    @validator('quantity')
    def validate_quantity(cls, v):
        """Validate share quantity"""
        if v > 1000000:  # 1M shares seems unreasonable for individual
            raise ValueError("Share quantity exceeds reasonable limits")
        return v
    
    @validator('price_per_share')
    def validate_share_price(cls, v):
        """Validate share price"""
        if v > 1000000:  # $1M per share seems unreasonable
            raise ValueError("Share price exceeds reasonable limits")
        return v
    
    @validator('purchase_date')
    def validate_purchase_date(cls, v):
        """Validate purchase date"""
        if v > date.today():
            raise ValueError("Purchase date cannot be in the future")
        return v


class UserRegistrationValidator(BaseFinancialValidator):
    """Validator for user registration"""
    
    username: str = Field(..., min_length=3, max_length=50, regex=r'^[a-zA-Z0-9_]+$', description="Username")
    email: str = Field(..., regex=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', description="Email address")
    password: str = Field(..., min_length=8, max_length=128, description="Password")
    name: str = Field(..., min_length=2, max_length=100, description="Full name")
    age: Optional[int] = Field(None, ge=18, le=120, description="Age")
    occupation: Optional[str] = Field(None, min_length=2, max_length=100, description="Occupation")
    location: Optional[str] = Field(None, min_length=2, max_length=200, description="Location")
    
    @validator('password')
    def validate_password_strength(cls, v):
        """Validate password strength"""
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r'[A-Z]', v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r'[a-z]', v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r'\d', v):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError("Password must contain at least one special character")
        return v
    
    @validator('username')
    def validate_username(cls, v):
        """Validate username doesn't contain offensive words"""
        offensive_words = ['admin', 'root', 'system', 'test', 'demo']
        if v.lower() in offensive_words:
            raise ValueError("Username is not allowed")
        return v


class ChatMessageValidator(BaseFinancialValidator):
    """Validator for chat messages"""
    
    message: str = Field(..., min_length=1, max_length=2000, description="Chat message")
    user_id: str = Field(..., min_length=1, max_length=50, description="User ID")
    session_id: Optional[str] = Field(None, min_length=10, max_length=100, description="Session ID")
    
    @validator('message')
    def validate_message_content(cls, v):
        """Validate message content for security"""
        # Check for SQL injection patterns
        sql_patterns = ['drop table', 'delete from', 'insert into', 'update set', 'union select']
        message_lower = v.lower()
        for pattern in sql_patterns:
            if pattern in message_lower:
                raise ValueError("Message contains potentially harmful content")
        
        # Check for script injection
        script_patterns = ['<script', 'javascript:', 'onload=', 'onerror=']
        for pattern in script_patterns:
            if pattern in message_lower:
                raise ValueError("Message contains potentially harmful content")
        
        return v


class FinancialDataValidator:
    """Main validator class for all financial data"""
    
    @staticmethod
    def validate_transaction(data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate transaction data"""
        try:
            validated = TransactionValidator(**data)
            return validated.dict()
        except Exception as e:
            raise ValidationError(f"Invalid transaction data: {e}")
    
    @staticmethod
    def validate_income(data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate income data"""
        try:
            validated = IncomeValidator(**data)
            return validated.dict()
        except Exception as e:
            raise ValidationError(f"Invalid income data: {e}")
    
    @staticmethod
    def validate_goal(data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate goal data"""
        try:
            validated = GoalValidator(**data)
            return validated.dict()
        except Exception as e:
            raise ValidationError(f"Invalid goal data: {e}")
    
    @staticmethod
    def validate_alert(data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate alert data"""
        try:
            validated = AlertValidator(**data)
            return validated.dict()
        except Exception as e:
            raise ValidationError(f"Invalid alert data: {e}")
    
    @staticmethod
    def validate_budget(data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate budget data"""
        try:
            validated = BudgetValidator(**data)
            return validated.dict()
        except Exception as e:
            raise ValidationError(f"Invalid budget data: {e}")
    
    @staticmethod
    def validate_investment(data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate investment data"""
        try:
            validated = InvestmentValidator(**data)
            return validated.dict()
        except Exception as e:
            raise ValidationError(f"Invalid investment data: {e}")
    
    @staticmethod
    def validate_user_registration(data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate user registration data"""
        try:
            validated = UserRegistrationValidator(**data)
            return validated.dict()
        except Exception as e:
            raise ValidationError(f"Invalid registration data: {e}")
    
    @staticmethod
    def validate_chat_message(data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate chat message data"""
        try:
            validated = ChatMessageValidator(**data)
            return validated.dict()
        except Exception as e:
            raise ValidationError(f"Invalid chat message: {e}")
    
    @staticmethod
    def sanitize_input(input_data: Union[str, Dict, List]) -> Union[str, Dict, List]:
        """Sanitize input data to prevent XSS and injection attacks"""
        if isinstance(input_data, str):
            # Remove HTML tags and special characters
            sanitized = re.sub(r'<[^>]+>', '', input_data)
            sanitized = re.sub(r'[<>"\']', '', sanitized)
            return sanitized.strip()
        elif isinstance(input_data, dict):
            return {k: FinancialDataValidator.sanitize_input(v) for k, v in input_data.items()}
        elif isinstance(input_data, list):
            return [FinancialDataValidator.sanitize_input(item) for item in input_data]
        else:
            return input_data
    
    @staticmethod
    def validate_financial_amount(amount: Union[str, float, Decimal]) -> Decimal:
        """Validate and convert financial amount"""
        try:
            if isinstance(amount, str):
                amount = amount.replace(',', '').replace('$', '').strip()
            
            decimal_amount = Decimal(str(amount))
            
            if decimal_amount < 0:
                raise ValueError("Amount cannot be negative")
            
            if decimal_amount.as_tuple().exponent < -2:
                raise ValueError("Amount cannot have more than 2 decimal places")
            
            return decimal_amount
            
        except (InvalidOperation, ValueError) as e:
            raise ValidationError(f"Invalid financial amount: {e}")
    
    @staticmethod
    def validate_date_range(start_date: date, end_date: date) -> bool:
        """Validate date range"""
        if start_date > end_date:
            raise ValidationError("Start date cannot be after end date")
        
        # Check if range is reasonable (not more than 10 years)
        days_diff = (end_date - start_date).days
        if days_diff > 3650:  # 10 years
            raise ValidationError("Date range exceeds maximum allowed period")
        
        return True
    
    @staticmethod
    def validate_user_id(user_id: str) -> str:
        """Validate user ID format"""
        if not user_id or not isinstance(user_id, str):
            raise ValidationError("User ID is required")
        
        if len(user_id) < 3 or len(user_id) > 50:
            raise ValidationError("User ID must be between 3 and 50 characters")
        
        if not re.match(r'^[a-zA-Z0-9_-]+$', user_id):
            raise ValidationError("User ID can only contain alphanumeric characters, underscores, and hyphens")
        
        return user_id
