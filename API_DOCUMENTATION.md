# AUREXIS AI - API Documentation

**Version**: 1.0.0  
**Base URL**: `http://localhost:8000`  
**Authentication**: JWT Bearer Token

---

## Table of Contents

1. [Authentication](#authentication)
2. [Financial Management](#financial-management)
3. [Forecasting](#forecasting)
4. [Advanced Analytics](#advanced-analytics)
5. [ML Forecasting](#ml-forecasting)
6. [Investment Optimization](#investment-optimization)
7. [Notifications](#notifications)
8. [WebSocket](#websocket)
9. [Agent Monitoring](#agent-monitoring)
10. [Chat](#chat)
11. [Reports](#reports)

---

## Authentication

### POST /api/auth/signup
Create a new user account.

**Request:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "SecurePass123!",
  "full_name": "John Doe"
}
```

**Response:**
```json
{
  "success": true,
  "user": {
    "id": "user_123",
    "username": "john_doe",
    "email": "john@example.com"
  },
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

### POST /api/auth/login
Login to existing account.

**Request:**
```json
{
  "username": "john_doe",
  "password": "SecurePass123!"
}
```

**Response:**
```json
{
  "success": true,
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

### POST /api/auth/refresh
Refresh access token.

**Headers:**
```
Authorization: Bearer <refresh_token>
```

**Response:**
```json
{
  "success": true,
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

---

## Financial Management

### GET /api/financial/summary
Get financial summary for user.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "success": true,
  "summary": {
    "total_income": 150000,
    "total_expenses": 95000,
    "net_worth": 500000,
    "savings_rate": 36.67,
    "expenses_by_category": {
      "housing": 35000,
      "food": 15000,
      "transportation": 10000
    }
  }
}
```

### POST /api/financial/transactions
Add a new transaction.

**Request:**
```json
{
  "amount": 5000,
  "type": "expense",
  "category": "dining",
  "description": "Restaurant dinner",
  "date": "2026-04-23"
}
```

**Response:**
```json
{
  "success": true,
  "transaction": {
    "id": "txn_123",
    "amount": 5000,
    "type": "expense",
    "category": "dining",
    "created_at": "2026-04-23T15:30:00"
  }
}
```

---

## Advanced Analytics

### GET /api/analytics/patterns
Detect financial patterns.

**Query Parameters:**
- `days` (optional): Number of days to analyze (default: 90)

**Response:**
```json
{
  "success": true,
  "patterns": {
    "spending_patterns": [
      {
        "category": "dining",
        "frequency": "high",
        "average_amount": 2500,
        "trend": "increasing"
      }
    ],
    "recurring_transactions": [
      {
        "description": "Netflix",
        "amount": 199,
        "frequency": "monthly"
      }
    ]
  }
}
```

### GET /api/analytics/insights
Generate financial insights.

**Response:**
```json
{
  "success": true,
  "insights": [
    {
      "type": "spending_trend",
      "title": "Spending Change Alert",
      "message": "Your total spending increased by 15% this month",
      "priority": 8,
      "category": "expenses",
      "impact": "high"
    }
  ]
}
```

### GET /api/analytics/behavior
Analyze financial behavior.

**Response:**
```json
{
  "success": true,
  "analysis": {
    "overall_score": 72,
    "category_scores": {
      "discipline": 75,
      "consistency": 80,
      "planning": 65
    },
    "behavior_profile": "Developing Planner",
    "strengths": ["High consistency", "Good savings habit"],
    "recommendations": [
      "Set up automatic transfers to savings on payday"
    ]
  }
}
```

---

## ML Forecasting

### POST /api/ml/ensemble-forecast
Generate ensemble forecast.

**Request:**
```json
{
  "metric": "net_worth",
  "steps": 6,
  "include_confidence": true
}
```

**Response:**
```json
{
  "success": true,
  "forecast": {
    "forecast": [105000, 108000, 111000, 114000, 117000, 120000],
    "lower_bound": [100000, 102000, 104000, 106000, 108000, 110000],
    "upper_bound": [110000, 114000, 118000, 122000, 126000, 130000],
    "confidence_score": 0.85,
    "model_agreement": 0.92
  }
}
```

---

## Investment Optimization

### POST /api/investments/optimize
Optimize portfolio allocation.

**Request:**
```json
{
  "investment_amount": 100000,
  "risk_tolerance": "moderate"
}
```

**Response:**
```json
{
  "success": true,
  "optimization": {
    "target_allocation": {
      "equity": 60,
      "debt": 25,
      "gold": 10,
      "real_estate": 5
    },
    "expected_return": 10.5,
    "expected_risk": 12.3,
    "sharpe_ratio": 0.53
  }
}
```

---

## Notifications

### GET /api/notifications
Get user notifications.

**Query Parameters:**
- `unread_only` (optional): Return only unread (default: false)
- `notification_type` (optional): Filter by type
- `limit` (optional): Maximum number (default: 50)

**Response:**
```json
{
  "success": true,
  "notifications": [
    {
      "id": "notif_123",
      "type": "budget_warning",
      "title": "Budget Warning",
      "message": "You've used 85% of your Dining budget",
      "priority": 2,
      "created_at": "2026-04-23T10:00:00",
      "read_at": null
    }
  ],
  "count": 10
}
```

### POST /api/notifications/template
Create notification from template.

**Request:**
```json
{
  "template_name": "budget_exceeded",
  "variables": {
    "category": "Dining",
    "amount": "5000"
  }
}
```

**Response:**
```json
{
  "success": true,
  "notification": {
    "id": "notif_456",
    "title": "Budget Exceeded",
    "message": "You've exceeded your Dining budget by ₹5000",
    "status": "sent"
  }
}
```

### PUT /api/notifications/{id}/read
Mark notification as read.

**Response:**
```json
{
  "success": true,
  "notification": {
    "id": "notif_123",
    "status": "read",
    "read_at": "2026-04-23T15:30:00"
  }
}
```

---

## WebSocket

### WS /ws?token=<jwt_token>
WebSocket connection for real-time updates.

**Connection:**
```javascript
const ws = new WebSocket('ws://localhost:8000/ws?token=<jwt_token>');
```

**Subscribe to Channel:**
```json
{
  "type": "subscribe",
  "channel": "notifications"
}
```

**Server Messages:**
```json
{
  "type": "notification",
  "data": {
    "id": "notif_789",
    "title": "New Transaction",
    "message": "₹5000 spent on Dining"
  },
  "timestamp": "2026-04-23T15:30:00"
}
```

**Available Channels:**
- notifications
- transactions
- goals
- alerts
- budget
- investments
- insights
- reports

---

## Agent Monitoring

### GET /api/agents/metrics
Get metrics for all agents.

**Response:**
```json
{
  "success": true,
  "metrics": {
    "query_agent": {
      "total_executions": 450,
      "successful_executions": 443,
      "failed_executions": 7,
      "average_execution_time": 1.2,
      "success_rate": 98.4,
      "health_status": "healthy"
    }
  }
}
```

### GET /api/agents/leaderboard
Get agent performance leaderboard.

**Response:**
```json
{
  "success": true,
  "leaderboard": [
    {
      "agent_name": "query_agent",
      "performance_score": 95.8,
      "success_rate": 98.5,
      "average_execution_time": 1.2,
      "health_status": "healthy"
    }
  ]
}
```

---

## Error Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 422 | Validation Error |
| 429 | Too Many Requests |
| 500 | Internal Server Error |

---

## Rate Limiting

- **Default**: 100 requests per minute per user
- **WebSocket**: 1 connection per user
- **Burst**: 200 requests per minute

---

## Best Practices

1. **Always use HTTPS in production**
2. **Store tokens securely** (httpOnly cookies recommended)
3. **Refresh tokens before expiry**
4. **Handle WebSocket reconnection**
5. **Implement exponential backoff for retries**
6. **Validate all inputs on client side**
7. **Handle errors gracefully**
8. **Use pagination for large datasets**

---

## Support

For API support, contact: support@aurexis.ai  
Documentation: https://docs.aurexis.ai  
Status: https://status.aurexis.ai

---

**Last Updated**: April 23, 2026  
**Version**: 1.0.0
