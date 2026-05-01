"""
Enhanced OpenAPI Documentation for AUREXIS AI
Comprehensive API documentation with examples and detailed schemas
"""

from typing import Dict, Any, List, Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field
from datetime import datetime, date
from decimal import Decimal

from exceptions import ErrorResponse
from api_versioning import get_api_version_info


class OpenAPIEnhancer:
    """Enhanced OpenAPI documentation with examples and detailed schemas"""
    
    @staticmethod
    def enhance_openapi_schema(app: FastAPI) -> Dict[str, Any]:
        """Enhance the OpenAPI schema with comprehensive documentation"""
        
        # Custom schema definitions
        schemas = {
            "ErrorResponse": {
                "type": "object",
                "properties": {
                    "success": {"type": "boolean", "example": False},
                    "error_code": {"type": "string", "example": "VALIDATION_ERROR"},
                    "message": {"type": "string", "example": "Invalid input data"},
                    "details": {"type": "object", "example": {"field": "username", "issue": "Required field"}},
                    "timestamp": {"type": "string", "example": "2024-01-15T10:30:00Z"},
                    "path": {"type": "string", "example": "/api/v1/auth/login"}
                },
                "required": ["success", "error_code", "message", "timestamp"]
            },
            
            "APIResponse": {
                "type": "object",
                "properties": {
                    "success": {"type": "boolean", "example": True},
                    "data": {"type": "object", "example": {"user_id": "1010101010"}},
                    "message": {"type": "string", "example": "Operation completed successfully"},
                    "timestamp": {"type": "string", "example": "2024-01-15T10:30:00Z"},
                    "version": {"type": "string", "example": "v1"}
                },
                "required": ["success", "timestamp"]
            },
            
            "User": {
                "type": "object",
                "properties": {
                    "id": {"type": "string", "example": "1010101010"},
                    "name": {"type": "string", "example": "John Doe"},
                    "email": {"type": "string", "example": "john@example.com", "format": "email"},
                    "occupation": {"type": "string", "example": "Software Engineer"},
                    "age": {"type": "integer", "example": 30, "minimum": 18, "maximum": 120},
                    "location": {"type": "string", "example": "San Francisco, CA"},
                    "user_number": {"type": "string", "example": "1010101010"},
                    "is_active": {"type": "boolean", "example": True},
                    "is_verified": {"type": "boolean", "example": False},
                    "created_at": {"type": "string", "example": "2024-01-01T00:00:00Z"},
                    "last_login": {"type": "string", "example": "2024-01-15T10:30:00Z"}
                },
                "required": ["id", "name", "email", "user_number"]
            },
            
            "LoginRequest": {
                "type": "object",
                "properties": {
                    "username": {
                        "type": "string",
                        "description": "Username or email address",
                        "example": "john@example.com",
                        "minLength": 1,
                        "maxLength": 50
                    },
                    "password": {
                        "type": "string",
                        "description": "User password",
                        "example": "SecurePassword123!",
                        "minLength": 8,
                        "maxLength": 128,
                        "format": "password"
                    }
                },
                "required": ["username", "password"]
            },
            
            "LoginResponse": {
                "type": "object",
                "properties": {
                    "success": {"type": "boolean", "example": True},
                    "data": {
                        "type": "object",
                        "properties": {
                            "session_id": {"type": "string", "example": "session_1010101010_20240115_103000"},
                            "user": {"$ref": "#/components/schemas/User"},
                            "expires_in": {"type": "integer", "example": 1800, "description": "Session expiration in seconds"}
                        }
                    },
                    "message": {"type": "string", "example": "Login successful"},
                    "timestamp": {"type": "string", "example": "2024-01-15T10:30:00Z"}
                }
            },
            
            "Transaction": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer", "example": 123},
                    "user_id": {"type": "string", "example": "1010101010"},
                    "date": {"type": "string", "format": "date", "example": "2024-01-15"},
                    "amount": {"type": "number", "example": 45.67, "minimum": 0.01},
                    "category": {
                        "type": "string",
                        "enum": ["Food", "Transportation", "Housing", "Utilities", "Healthcare", 
                                "Entertainment", "Shopping", "Education", "Insurance", "Taxes", 
                                "Debt Payment", "Savings", "Investment", "Other"],
                        "example": "Food"
                    },
                    "description": {"type": "string", "example": "Lunch at restaurant"},
                    "merchant": {"type": "string", "example": "McDonald's"},
                    "created_at": {"type": "string", "example": "2024-01-15T10:30:00Z"}
                },
                "required": ["user_id", "date", "amount", "category"]
            },
            
            "Goal": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer", "example": 456},
                    "user_id": {"type": "string", "example": "1010101010"},
                    "name": {"type": "string", "example": "Emergency Fund"},
                    "target_amount": {"type": "number", "example": 10000.00, "minimum": 0.01},
                    "current_amount": {"type": "number", "example": 3500.00, "minimum": 0},
                    "deadline": {"type": "string", "format": "date", "example": "2024-12-31"},
                    "category": {"type": "string", "example": "Savings"},
                    "status": {
                        "type": "string",
                        "enum": ["active", "completed", "paused"],
                        "example": "active"
                    },
                    "created_at": {"type": "string", "example": "2024-01-01T00:00:00Z"},
                    "updated_at": {"type": "string", "example": "2024-01-15T10:30:00Z"}
                },
                "required": ["user_id", "name", "target_amount"]
            },
            
            "ChatMessage": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "example": "1010101010"},
                    "message": {
                        "type": "string",
                        "description": "Chat message content",
                        "example": "How can I save more money each month?",
                        "minLength": 1,
                        "maxLength": 2000
                    },
                    "conversation_history": {
                        "type": "array",
                        "items": {"type": "object"},
                        "description": "Previous conversation messages",
                        "example": []
                    },
                    "session_id": {"type": "string", "example": "session_abc123"},
                    "use_memory": {"type": "boolean", "example": True, "description": "Use conversation memory"}
                },
                "required": ["user_id", "message"]
            },
            
            "ChatResponse": {
                "type": "object",
                "properties": {
                    "success": {"type": "boolean", "example": True},
                    "response": {
                        "type": "object",
                        "properties": {
                            "content": {"type": "string", "example": "Based on your spending patterns..."},
                            "model": {"type": "string", "example": "deepseek-v3.1:671b-cloud"},
                            "confidence": {"type": "number", "example": 0.85, "minimum": 0, "maximum": 1},
                            "timestamp": {"type": "string", "example": "2024-01-15T10:30:00Z"}
                        }
                    },
                    "user_id": {"type": "string", "example": "1010101010"},
                    "session_id": {"type": "string", "example": "session_abc123"}
                }
            },
            
            "FinancialMetrics": {
                "type": "object",
                "properties": {
                    "monthly_income": {"type": "number", "example": 5000.00},
                    "monthly_expenses": {"type": "number", "example": 3500.00},
                    "monthly_savings": {"type": "number", "example": 1500.00},
                    "savings_rate": {"type": "number", "example": 0.30},
                    "net_worth": {"type": "number", "example": 45000.00},
                    "debt_to_income_ratio": {"type": "number", "example": 0.25},
                    "emergency_fund_months": {"type": "number", "example": 6},
                    "investment_portfolio_value": {"type": "number", "example": 25000.00}
                }
            },
            
            "Alert": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer", "example": 789},
                    "user_id": {"type": "string", "example": "1010101010"},
                    "type": {"type": "string", "example": "budget_warning"},
                    "title": {"type": "string", "example": "Budget Alert"},
                    "message": {"type": "string", "example": "You've exceeded your food budget by 20%"},
                    "severity": {
                        "type": "string",
                        "enum": ["low", "medium", "high", "critical"],
                        "example": "medium"
                    },
                    "is_read": {"type": "boolean", "example": False},
                    "created_at": {"type": "string", "example": "2024-01-15T10:30:00Z"}
                }
            }
        }
        
        # Enhanced tags with descriptions
        tags = [
            {
                "name": "Authentication",
                "description": "User authentication and session management",
                "externalDocs": {
                    "description": "Authentication Guide",
                    "url": "https://docs.aurexis.ai/auth"
                }
            },
            {
                "name": "Users",
                "description": "User profile and account management",
                "externalDocs": {
                    "description": "User Management Guide",
                    "url": "https://docs.aurexis.ai/users"
                }
            },
            {
                "name": "Financial Data",
                "description": "Financial transactions, income, and expense management",
                "externalDocs": {
                    "description": "Financial Data Guide",
                    "url": "https://docs.aurexis.ai/financial-data"
                }
            },
            {
                "name": "Goals",
                "description": "Financial goal setting and tracking",
                "externalDocs": {
                    "description": "Goals Guide",
                    "url": "https://docs.aurexis.ai/goals"
                }
            },
            {
                "name": "Analytics",
                "description": "Financial analytics and metrics",
                "externalDocs": {
                    "description": "Analytics Guide",
                    "url": "https://docs.aurexis.ai/analytics"
                }
            },
            {
                "name": "Chat",
                "description": "AI-powered financial advice chat",
                "externalDocs": {
                    "description": "Chat API Guide",
                    "url": "https://docs.aurexis.ai/chat"
                }
            },
            {
                "name": "Reports",
                "description": "Financial report generation and export",
                "externalDocs": {
                    "description": "Reports Guide",
                    "url": "https://docs.aurexis.ai/reports"
                }
            },
            {
                "name": "Alerts",
                "description": "Financial alerts and notifications",
                "externalDocs": {
                    "description": "Alerts Guide",
                    "url": "https://docs.aurexis.ai/alerts"
                }
            },
            {
                "name": "WebSocket",
                "description": "Real-time WebSocket connections",
                "externalDocs": {
                    "description": "WebSocket Guide",
                    "url": "https://docs.aurexis.ai/websocket"
                }
            }
        ]
        
        # Enhanced security schemes
        security_schemes = {
            "SessionAuth": {
                "type": "apiKey",
                "in": "header",
                "name": "X-Session-ID",
                "description": "Session-based authentication"
            },
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
                "description": "JWT token authentication"
            }
        }
        
        # Example responses
        examples = {
            "ValidationError": {
                "summary": "Validation Error Example",
                "value": {
                    "success": False,
                    "error_code": "VALIDATION_ERROR",
                    "message": "Invalid input data",
                    "details": {
                        "field": "email",
                        "issue": "Invalid email format"
                    },
                    "timestamp": "2024-01-15T10:30:00Z",
                    "path": "/api/v1/users"
                }
            },
            "AuthenticationError": {
                "summary": "Authentication Error Example",
                "value": {
                    "success": False,
                    "error_code": "AUTHENTICATION_ERROR",
                    "message": "Invalid credentials",
                    "details": {
                        "username": "john@example.com"
                    },
                    "timestamp": "2024-01-15T10:30:00Z",
                    "path": "/api/v1/auth/login"
                }
            },
            "SuccessResponse": {
                "summary": "Success Response Example",
                "value": {
                    "success": True,
                    "data": {
                        "user_id": "1010101010",
                        "name": "John Doe"
                    },
                    "message": "Operation completed successfully",
                    "timestamp": "2024-01-15T10:30:00Z",
                    "version": "v1"
                }
            }
        }
        
        return {
            "openapi": "3.0.0",
            "info": {
                "title": "AUREXIS AI API",
                "version": "2.1.0",
                "description": """
                ## AUREXIS AI Financial Decision Support System API
                
                A comprehensive REST API for financial analysis, planning, and AI-powered advice.
                
                ### Key Features
                - **API Versioning**: Support for multiple API versions with backward compatibility
                - **Authentication**: Session-based and JWT authentication
                - **Real-time Updates**: WebSocket support for live data
                - **Comprehensive Analytics**: Financial metrics, forecasting, and insights
                - **AI-Powered Advice**: Intelligent financial recommendations
                
                ### Getting Started
                1. **Authentication**: Use `/api/v1/auth/login` to get a session
                2. **User Data**: Access user financial data via `/api/v1/users/{user_id}`
                3. **Analytics**: Get financial metrics via `/api/v1/analytics/metrics`
                4. **Chat**: Get AI advice via `/api/v1/chat`
                
                ### API Versions
                - **v1**: Current stable version (`/api/v1/*`)
                - **Legacy**: Deprecated version (`/api/*` - will be removed Dec 2025)
                
                ### Rate Limiting
                - General endpoints: 100 requests/minute
                - Authentication: 5 requests/minute
                - Chat endpoints: 20 requests/minute
                
                ### Error Handling
                All errors follow a consistent format with error codes, messages, and details.
                """,
                "termsOfService": "https://aurexis.ai/terms",
                "contact": {
                    "name": "AUREXIS AI Support",
                    "email": "support@aurexis.ai",
                    "url": "https://aurexis.ai/support"
                },
                "license": {
                    "name": "MIT License",
                    "url": "https://opensource.org/licenses/MIT"
                }
            },
            "servers": [
                {
                    "url": "http://localhost:8000",
                    "description": "Development server"
                },
                {
                    "url": "https://api.aurexis.ai",
                    "description": "Production server"
                },
                {
                    "url": "https://staging-api.aurexis.ai",
                    "description": "Staging server"
                }
            ],
            "paths": {},  # Will be populated by FastAPI automatically
            "components": {
                "schemas": schemas,
                "securitySchemes": security_schemes,
                "examples": examples
            },
            "tags": tags,
            "security": [
                {"SessionAuth": []},
                {"BearerAuth": []}
            ]
        }
    
    @staticmethod
    def add_endpoint_examples(app: FastAPI):
        """Add detailed examples to specific endpoints"""
        
        # Custom endpoint documentation
        endpoint_docs = {
            "/api/v1/auth/login": {
                "summary": "User Login",
                "description": """
                Authenticate a user and create a session.
                
                The login endpoint accepts either username or email address.
                Successful authentication returns a session ID that must be included
                in subsequent requests via the `X-Session-ID` header.
                
                **Rate Limiting**: 5 requests per minute per IP address
                **Session Duration**: 30 minutes (configurable)
                
                **Example Usage:**
                ```bash
                curl -X POST "https://api.aurexis.ai/api/v1/auth/login" \\
                  -H "Content-Type: application/json" \\
                  -d '{
                    "username": "john@example.com",
                    "password": "SecurePassword123!"
                  }'
                ```
                """,
                "requestBody": {
                    "content": {
                        "application/json": {
                            "example": {
                                "username": "john@example.com",
                                "password": "SecurePassword123!"
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Login successful",
                        "content": {
                            "application/json": {
                                "example": {
                                    "success": True,
                                    "data": {
                                        "session_id": "session_1010101010_20240115_103000",
                                        "user": {
                                            "id": "1010101010",
                                            "name": "John Doe",
                                            "email": "john@example.com",
                                            "occupation": "Software Engineer",
                                            "age": 30,
                                            "location": "San Francisco, CA"
                                        },
                                        "expires_in": 1800
                                    },
                                    "message": "Login successful",
                                    "timestamp": "2024-01-15T10:30:00Z"
                                }
                            }
                        }
                    },
                    "401": {
                        "description": "Authentication failed",
                        "content": {
                            "application/json": {
                                "example": {
                                    "success": False,
                                    "error_code": "AUTHENTICATION_ERROR",
                                    "message": "Invalid credentials",
                                    "details": {"username": "john@example.com"},
                                    "timestamp": "2024-01-15T10:30:00Z",
                                    "path": "/api/v1/auth/login"
                                }
                            }
                        }
                    }
                }
            },
            
            "/api/v1/chat": {
                "summary": "AI Financial Advice",
                "description": """
                Get AI-powered financial advice and insights.
                
                The chat endpoint analyzes your financial data and provides personalized advice.
                It can help with budgeting, investment strategies, goal planning, and more.
                
                **Features:**
                - Contextual advice based on your financial data
                - Conversation memory for follow-up questions
                - Real-time analysis and recommendations
                - Multi-turn conversations
                
                **Rate Limiting**: 20 requests per minute per session
                
                **Example Usage:**
                ```bash
                curl -X POST "https://api.aurexis.ai/api/v1/chat" \\
                  -H "Content-Type: application/json" \\
                  -H "X-Session-ID: session_1010101010_20240115_103000" \\
                  -d '{
                    "user_id": "1010101010",
                    "message": "How can I save more money each month?",
                    "use_memory": true
                  }'
                ```
                """,
                "requestBody": {
                    "content": {
                        "application/json": {
                            "example": {
                                "user_id": "1010101010",
                                "message": "How can I save more money each month?",
                                "conversation_history": [],
                                "session_id": "session_abc123",
                                "use_memory": True
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Chat response with AI advice",
                        "content": {
                            "application/json": {
                                "example": {
                                    "success": True,
                                    "response": {
                                        "content": "Based on your spending patterns, I recommend...",
                                        "model": "deepseek-v3.1:671b-cloud",
                                        "confidence": 0.85,
                                        "timestamp": "2024-01-15T10:30:00Z"
                                    },
                                    "user_id": "1010101010",
                                    "session_id": "session_abc123"
                                }
                            }
                        }
                    }
                }
            }
        }
        
        # Apply custom documentation to endpoints
        for path, docs in endpoint_docs.items():
            if path in app.routes:
                # This would require more complex route manipulation
                # For now, the documentation will be available through the enhanced schema
                pass
    
    @staticmethod
    def generate_api_documentation() -> Dict[str, Any]:
        """Generate comprehensive API documentation"""
        version_info = get_api_version_info()
        
        return {
            "title": "AUREXIS AI API Documentation",
            "version": "2.1.0",
            "description": "Comprehensive financial decision support API",
            "api_versions": version_info,
            "authentication": {
                "methods": ["Session-based", "JWT Bearer Token"],
                "headers": ["X-Session-ID", "Authorization: Bearer <token>"],
                "session_duration": "30 minutes",
                "rate_limits": {
                    "general": "100 requests/minute",
                    "auth": "5 requests/minute",
                    "chat": "20 requests/minute"
                }
            },
            "base_urls": {
                "development": "http://localhost:8000",
                "staging": "https://staging-api.aurexis.ai",
                "production": "https://api.aurexis.ai"
            },
            "endpoints": {
                "authentication": [
                    {
                        "path": "/api/v1/auth/login",
                        "method": "POST",
                        "description": "User authentication",
                        "auth_required": False
                    },
                    {
                        "path": "/api/v1/auth/logout",
                        "method": "POST",
                        "description": "User logout",
                        "auth_required": True
                    }
                ],
                "users": [
                    {
                        "path": "/api/v1/users/{user_id}",
                        "method": "GET",
                        "description": "Get user profile",
                        "auth_required": True
                    },
                    {
                        "path": "/api/v1/users/{user_id}/data",
                        "method": "GET",
                        "description": "Get user financial data",
                        "auth_required": True
                    }
                ],
                "analytics": [
                    {
                        "path": "/api/v1/analytics/metrics/{user_id}",
                        "method": "GET",
                        "description": "Get financial metrics",
                        "auth_required": True
                    },
                    {
                        "path": "/api/v1/analytics/forecast/{user_id}",
                        "method": "GET",
                        "description": "Get financial forecast",
                        "auth_required": True
                    }
                ],
                "chat": [
                    {
                        "path": "/api/v1/chat",
                        "method": "POST",
                        "description": "AI financial advice",
                        "auth_required": True
                    }
                ]
            },
            "error_codes": {
                "VALIDATION_ERROR": "Input validation failed",
                "AUTHENTICATION_ERROR": "Authentication failed",
                "AUTHORIZATION_ERROR": "Access denied",
                "NOT_FOUND": "Resource not found",
                "RATE_LIMIT_EXCEEDED": "Too many requests",
                "DATABASE_ERROR": "Database operation failed",
                "EXTERNAL_SERVICE_ERROR": "External service unavailable",
                "BUSINESS_LOGIC_ERROR": "Business rule violation"
            },
            "examples": {
                "authentication": {
                    "login": {
                        "request": {
                            "username": "john@example.com",
                            "password": "SecurePassword123!"
                        },
                        "response": {
                            "success": True,
                            "data": {
                                "session_id": "session_1010101010_20240115_103000",
                                "user": {
                                    "id": "1010101010",
                                    "name": "John Doe",
                                    "email": "john@example.com"
                                },
                                "expires_in": 1800
                            }
                        }
                    }
                },
                "analytics": {
                    "metrics": {
                        "response": {
                            "success": True,
                            "data": {
                                "monthly_income": 5000.00,
                                "monthly_expenses": 3500.00,
                                "monthly_savings": 1500.00,
                                "savings_rate": 0.30,
                                "net_worth": 45000.00
                            }
                        }
                    }
                }
            },
            "sdk_and_libraries": {
                "python": "pip install aurexis-ai-client",
                "javascript": "npm install aurexis-ai-js",
                "postman": "https://api.aurexis.io/postman-collection"
            },
            "support": {
                "documentation": "https://docs.aurexis.ai",
                "api_reference": "https://api.aurexis.ai/docs",
                "support_email": "support@aurexis.ai",
                "status_page": "https://status.aurexis.ai"
            }
        }
