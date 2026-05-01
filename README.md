# AUREXIS AI - Financial Decision Support System

**Status**: ✅ Production Ready - Enterprise Grade  
**Last Updated**: May 1, 2026

---

## 🌟 Project Overview

AUREXIS AI is an **enterprise-grade AI-powered Financial Decision Support System** that provides comprehensive financial analysis, risk assessment, goal tracking, and intelligent recommendations powered by a multi-agent AI system.

### 🎯 Key Highlights
- 🏗️ **Production-Ready Architecture** - Modular, scalable, maintainable
- 🤖 **14 Specialized AI Agents** - Multi-agent orchestration system
- 📊 **93+ API Endpoints** - Comprehensive REST API with versioning
- 🧠 **Advanced ML Forecasting** - Ensemble models with confidence intervals
- 💡 **Explainable AI** - Transparent recommendations with reasoning
- 🔒 **Enterprise Security** - JWT auth, bcrypt, rate limiting, input validation
- 📈 **Real-time Analytics** - WebSocket support for live updates
- 🎨 **Modern UI** - 15 pages, 13 chart types, responsive design
- ⚡ **Performance Optimized** - Intelligent caching, <50ms response time
- 🔄 **CI/CD Ready** - Automated testing and deployment
- 💾 **Automated Backups** - Daily database backups with easy restore
- 📊 **Monitoring** - Health checks, uptime tracking, performance metrics

### Core Features
- 📊 **Financial Health Analysis** - Multi-dimensional health scoring
- 💰 **Expense Tracking** - AI-powered categorization and insights
- 🎯 **Goal Management** - Smart goal tracking with ML predictions
- ⚠️ **Risk Assessment** - 10+ risk metrics with portfolio analysis
- 🔔 **Smart Alerts** - Multi-channel real-time notifications
- 🤖 **AI Insights** - Pattern detection and behavior analysis
- 📈 **Forecasting** - Ensemble ML models (ARIMA, LSTM, Prophet, Linear)
- 💼 **Investment Optimization** - MPT-based portfolio optimization
- 📱 **Responsive Design** - Works seamlessly on all devices

---

## 🚀 Quick Start

### Prerequisites
- **Python** 3.11+
- **Node.js** 18+
- **npm** or yarn
- **Git** (for version control)

### Installation

```bash
# Clone repository
git clone <repository-url>
cd aurexis-ai

# Backend setup
cd backend
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Frontend setup
cd ../frontend
npm install
```

### Configuration

1. **Create environment file** (`backend/.env`):
```env
# Security Keys
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here

# Database
DATABASE_URL=sqlite:///./aurexis.db

# Ollama (optional)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=deepseek-v3.1:671b-cloud

# Redis (optional - will use in-memory cache if not available)
REDIS_HOST=localhost
REDIS_PORT=6379
```

2. **Generate secure SECRET_KEYs**:
```bash
python -c "import secrets; print('SECRET_KEY=' + secrets.token_urlsafe(32))"
python -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_urlsafe(32))"
```

### Running the Application

```bash
# Start backend (Terminal 1)
cd backend
python server.py

# Start frontend (Terminal 2)
cd frontend
npm run dev
```

### Access the Application
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### Login Credentials
- **Username**: `22243045` or `Senthilkumaran`
- **Password**: `Senthilkumaran@2000`

Or use any of the 12 pre-configured test users (see below).

---

## 📚 AUREXIS AI — Financial Intelligence Platform

🚀 **Enterprise-grade** AI-powered personal finance platform with real-time risk analysis, ML forecasting, investment tracking, scenario simulation, and a local LLM chat advisor powered by Ollama.

---

## 🎯 Key Features

### Financial Analytics
- 📊 Real-time metrics (income, expenses, savings, net worth)
- 📈 12-month historical + 6-month projected forecasts
- 💰 Expense breakdown by category with trends
- 📉 Investment portfolio analysis (stocks, mutual funds, EPF)
- 🎯 Financial goal tracking with progress
- ⚠️ Risk analysis with detailed factors
- 💡 Personalized recommendations

### ML Forecasting
- 🤖 ARIMA time series forecasting
- 🧠 LSTM neural network predictions
- 🌲 Random Forest regression
- 📊 Gradient Boosting (XGBoost)
- 🎯 Ensemble predictions for accuracy

### AI Budget Optimizer
- 📊 **Spending Pattern Analysis** - Identify where your money goes
- 🔮 **Expense Prediction** - ML-based forecasting of future expenses
- 💡 **Optimal Budget Allocation** - AI-powered recommendations using 50/30/20 rule
- 🏷️ **Auto-Categorization** - Automatically categorize transactions
- 💰 **Personalized Savings Plans** - Custom plans to reach financial goals
- 📈 **Temporal Insights** - Spending patterns by day/time
- 🎯 **Optimization Score** - Track your budget efficiency

### Credit Score Prediction
- 🎯 **ML-Based Prediction** - Predict future credit score
- 📊 **Score Breakdown** - Detailed analysis of score components
- 💡 **Improvement Recommendations** - Actionable steps to boost score
- ⏱️ **Timeline to Excellence** - Path to 800+ credit score
- ⚠️ **Risk Factor Analysis** - Identify negative impacts
- ✅ **Positive Factor Tracking** - Recognize good habits

### Tax Planning & Optimization
- 💰 **Regime Comparison** - New vs Old tax regime analysis
- 📊 **Tax Calculation** - Accurate tax liability computation
- 💡 **Investment Suggestions** - Section 80C, 80D, NPS recommendations
- 📅 **Advance Tax Schedule** - Payment timeline and amounts
- 🎯 **Tax Efficiency Score** - Measure optimization level
- 💸 **Quick Wins** - Easy tax-saving opportunities

### Fraud Detection System
- 🔒 **Real-time Analysis** - Instant transaction risk assessment
- 🤖 **ML-Powered Scoring** - Intelligent fraud detection
- ⚠️ **Risk Factors** - Detailed fraud indicators
- 🛡️ **Account Takeover Detection** - Identify suspicious activity
- 📊 **Fraud Reports** - Comprehensive security analysis
- 🚨 **Automated Blocking** - High-risk transaction prevention

### Real-time Alert System
- 🔔 **Transaction Alerts** - Large or unusual transactions
- 💰 **Balance Warnings** - Low balance notifications
- 📅 **Bill Reminders** - Upcoming payment alerts
- 🎯 **Goal Milestones** - Progress notifications
- 📈 **Investment Alerts** - Performance updates
- ⚠️ **Spending Warnings** - Unusual pattern detection
- 💎 **Achievement Badges** - Financial milestone celebrations

### AI Chat Memory
- 🧠 **Persistent Storage** - All conversations saved to database
- 🎯 **Context-Aware Responses** - AI remembers previous conversations
- 👤 **User Preferences** - Learns from conversation history
- 📝 **Session Management** - Organize conversations by topic
- 🔍 **Search History** - Find past conversations easily
- 📊 **Conversation Statistics** - Track engagement metrics
- 🔒 **Privacy Controls** - Clear history anytime

### AI Chat Advisor
- 💬 Local LLM powered by Ollama (DeepSeek v3.1)
- 🔒 Privacy-first (no cloud APIs)
- 📊 Context-aware financial advice
- 💡 Personalized recommendations
- 📈 Real-time data integration
- 🧠 **Persistent Chat Memory** - Remembers conversations
- 🎯 **User Preferences** - Learns from history
- 📝 **Session Management** - Organized conversations

### Security & Performance
- 🔐 JWT authentication with refresh tokens
- 🔒 Bcrypt password hashing
- 🛡️ Rate limiting (100 req/min global, endpoint-specific)
- ⚡ Intelligent response caching (5-min TTL)
- 📝 Comprehensive logging with request tracking
- 🎯 Health checks and uptime monitoring
- ✅ Input validation and XSS/SQL injection prevention
- 🚫 Request size limits (10 MB max)
- 📊 Performance metrics and monitoring
- 💾 Automated daily backups

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | React 18 + TypeScript | Type-safe UI development |
| **Build Tool** | Vite | Lightning-fast HMR and builds |
| **Styling** | Tailwind CSS + shadcn/ui | Modern, accessible components |
| **State** | Zustand | Lightweight state management |
| **Charts** | Recharts | Beautiful data visualizations |
| **Routing** | React Router v6 | Client-side routing |
| **Backend** | FastAPI + Python 3.11 | High-performance async API |
| **Database** | SQLite + SQLAlchemy | Relational data storage |
| **Auth** | JWT + bcrypt | Secure authentication |
| **AI/ML** | scikit-learn, statsmodels | ML forecasting and analysis |
| **LLM** | Ollama (DeepSeek v3.1) | Local AI chat advisor |
| **Caching** | Redis (optional) | Performance optimization |
| **Validation** | Pydantic | Request/response validation |
| **Testing** | pytest + pytest-asyncio | Comprehensive test coverage |

---

## 📁 Project Structure

```
aurexis-ai/
├── backend/
│   ├── server.py                    # FastAPI application entry point
│   ├── config.py                    # Configuration management
│   ├── database/
│   │   └── db_utils.py              # Database connection and utilities
│   ├── auth/
│   │   ├── jwt_handler.py           # JWT token management
│   │   └── dependencies.py          # Auth dependencies
│   ├── models/
│   │   ├── user.py                  # User database model
│   │   └── financial.py             # Financial data models
│   ├── schemas/                     # Pydantic validation schemas
│   │   ├── auth.py
│   │   ├── financial.py
│   │   ├── chat.py
│   │   └── report.py
│   ├── services/                    # Business logic layer
│   │   ├── auth_service.py
│   │   ├── financial_service.py
│   │   ├── forecast_service.py
│   │   ├── recommendation_service.py
│   │   └── alert_service.py
│   ├── routes/                      # API route handlers
│   │   ├── auth.py
│   │   ├── financial.py
│   │   ├── forecast.py
│   │   ├── chat.py
│   │   ├── reports.py
│   │   ├── advanced_analytics.py
│   │   ├── ml_forecasting.py
│   │   ├── investment_optimization.py
│   │   ├── notifications.py
│   │   ├── websocket_routes.py
│   │   └── agent_monitoring.py
│   ├── agents/                      # Multi-agent AI system
│   │   ├── orchestrator.py          # Agent coordinator
│   │   ├── base_agent.py            # Base agent class
│   │   └── ... (14 specialized agents)
│   ├── ml/                          # Machine learning modules
│   │   ├── ensemble_forecasting.py  # Ensemble ML models
│   │   ├── time_series_analysis.py  # Time series decomposition
│   │   └── confidence_intervals.py  # Statistical confidence
│   ├── analytics/                   # Advanced analytics
│   │   ├── pattern_detector.py      # Pattern recognition
│   │   ├── insight_generator.py     # Insight generation
│   │   └── behavior_analyzer.py     # Behavior analysis
│   ├── tests/                       # Test suite
│   ├── logs/                        # Application logs
│   ├── requirements.txt             # Python dependencies
│   └── .env                         # Environment configuration
│
└── frontend/
    ├── src/
    │   ├── pages/                   # 15 application pages
    │   ├── components/              # Reusable components
    │   ├── services/                # API integration
    │   ├── store/                   # Zustand state management
    │   ├── lib/                     # Utilities
    │   ├── types/                   # TypeScript types
    │   └── App.tsx                  # Root component
    ├── package.json
    └── vite.config.ts
```

---

## 🔐 Login Credentials

All test users are pre-configured with password format: `Name@2000`

| Name | Password | User Number | Occupation | Location |
|------|----------|-------------|------------|----------|
| Senthilkumaran | Senthilkumaran@2000 | 22243045 | Software Engineer | Salem |
| Imayavarman | Imayavarman@2000 | 22243017 | Doctor | Erode |
| Srivarshan | Srivarshan@2000 | 22243050 | Business Owner | Theni |
| Rahulprasath | Rahulprasath@2000 | 22243040 | Teacher | Omalur |
| Magudesh | Magudesh@2000 | 22243055 | Freelancer | Bangalore |
| Deepak | Deepak@2000 | 22243009 | CA | Chennai |
| Mani | Mani@2000 | 22243060 | Government Employee | Edapadi |
| Dineshkumar | Dineshkumar@2000 | 22243012 | Lawyer | Sangagari |
| Avinash | Avinash@2000 | 22243007 | IPS | Ambur |
| Kumar | Kumar@2000 | 22243020 | Content Creator | Coimbatore |
| Hari | Hari@2000 | 22243016 | Startup Founder | Karur |
| Janakrishnan | Janakrishnan@2000 | 22243019 | Government Employee | Rasipuram |

**Quick Test Login:**
```bash
curl -X POST http://localhost:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username": "22243045", "password": "Senthilkumaran@2000"}'
```

---

## 📊 API Endpoints

### System Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root endpoint - Server status |
| GET | `/health` | Health check with component status |
| GET | `/metrics` | Prometheus metrics (optional) |
| GET | `/docs` | Interactive API documentation (Swagger UI) |
| GET | `/redoc` | API documentation (ReDoc) |

### Authentication (`/api/login`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/login` | Login with username/password → JWT tokens |
| POST | `/api/logout` | Logout and invalidate session |

### Financial Endpoints (`/api/financial`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/financial/expenses` | Get user expenses |
| POST | `/api/financial/expenses` | Create new expense |
| PUT | `/api/financial/expenses/{id}` | Update expense |
| DELETE | `/api/financial/expenses/{id}` | Delete expense |
| GET | `/api/financial/income` | Get user income |
| POST | `/api/financial/income` | Create income record |
| GET | `/api/financial/goals` | Get financial goals |
| POST | `/api/financial/goals` | Create new goal |
| PUT | `/api/financial/goals/{id}` | Update goal |
| DELETE | `/api/financial/goals/{id}` | Delete goal |
| GET | `/api/financial/alerts` | Get user alerts |
| POST | `/api/financial/alerts/generate` | Generate new alerts |
| GET | `/api/financial/recommendations` | Get recommendations |
| POST | `/api/financial/recommendations/generate` | Generate recommendations |
| GET | `/api/financial/health` | Get financial health score |
| GET | `/api/financial/metrics` | Get key financial metrics |
| POST | `/api/financial/simulation` | Run scenario simulation |

### Chat Endpoints (`/api/chat`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/chat/message` | Chat with AI advisor |
| GET | `/api/chat/history` | Get conversation history |
| GET | `/api/chat/sessions` | Get conversation sessions |
| GET | `/api/chat/stats` | Get conversation statistics |
| POST | `/api/chat/search` | Search conversation history |
| DELETE | `/api/chat/clear` | Clear conversation history |

---

## 🚀 Production Deployment

### Using PM2 (Recommended)

```bash
# Install PM2
npm install -g pm2

# Start backend
cd backend
pm2 start server.py --name aurexis-backend --interpreter python

# Start frontend (after build)
cd frontend
npm run build
pm2 start "serve -s dist -p 5173" --name aurexis-frontend

# View status
pm2 status

# View logs
pm2 logs

# Auto-start on boot
pm2 startup
pm2 save
```

### Using Systemd (Linux)

Create `/etc/systemd/system/aurexis-backend.service`:
```ini
[Unit]
Description=AUREXIS AI Backend
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/aurexis-ai/backend
ExecStart=/path/to/aurexis-ai/backend/venv/bin/python server.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable aurexis-backend
sudo systemctl start aurexis-backend
sudo systemctl status aurexis-backend
```

---

## 🔧 Troubleshooting

### Backend Won't Start

```bash
# Check if port 8000 is in use
# Windows:
netstat -ano | findstr :8000
# Linux/Mac:
lsof -i :8000

# Reinstall dependencies
cd backend
pip install -r requirements.txt --force-reinstall
```

### Ollama Not Responding

```bash
# Check if Ollama is running
ollama list

# Start Ollama
ollama serve

# Pull model
ollama pull deepseek-v3.1:671b-cloud

# Test Ollama
curl http://localhost:11434/api/tags
```

### Database Errors

```bash
# Check database file
cd backend
python -c "from database.db_utils import get_db; conn = get_db().__enter__(); cursor = conn.cursor(); cursor.execute('SELECT COUNT(*) FROM users'); print(f'Users: {cursor.fetchone()[0]}')"
```

---

## 📚 Dashboard Features

| Section | Description |
|---------|-------------|
| Overview | Key metrics, health score, forecast chart, quick summary cards |
| Financial Health | Health score gauge, savings rate, credit score, recommendations |
| Risk Analysis | Risk level, debt-to-income ratio, credit score |
| Savings | Monthly savings, emergency fund, goals tracking |
| Debt | Total debt, DTI ratio, scenario simulation |
| Investments | Portfolio breakdown, allocation, returns |
| Goals | Progress tracking with monthly savings targets |
| Forecasting | 6-month income/expense/savings projection |
| Scenario Sim | What-if modeling — loans, salary, job loss, purchases |
| Alerts | AI-generated financial recommendations |
| Reports | Expense breakdown + forecast charts |
| AI Chat | Personalized financial advice via local Ollama LLM |

---

## 📖 API Documentation

### Interactive Documentation
- **Swagger UI**: http://localhost:8000/docs (Try out endpoints directly)
- **ReDoc**: http://localhost:8000/redoc (Clean API reference)

### System Endpoints
- **Health Check**: http://localhost:8000/health (System status)
- **Metrics**: http://localhost:8000/metrics (Prometheus metrics)

### Quick API Test

**1. Login and Get Token:**
```bash
curl -X POST http://localhost:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username": "22243045", "password": "Senthilkumaran@2000"}'
```

**Response:**
```json
{
  "success": true,
  "data": {
    "access_token": "eyJhbGc...",
    "refresh_token": "eyJhbGc...",
    "token_type": "Bearer",
    "user": {
      "id": "22243045",
      "name": "Senthilkumaran",
      "email": "sk@gmail.com"
    }
  }
}
```

**2. Use Token to Access Protected Endpoints:**
```bash
curl -X GET http://localhost:8000/api/financial/health \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Write tests for new features
- Follow PEP 8 style guide for Python
- Use ESLint for TypeScript/React
- Update documentation
- Run tests before committing

---

## 📄 License

MIT License - See [LICENSE](./LICENSE) file for details

---

## 🙏 Acknowledgments

Built with:
- **FastAPI** - Modern, fast web framework
- **SQLAlchemy** - Powerful ORM
- **Redis** - High-performance caching
- **Prometheus** - Metrics collection
- **Ollama** - Local LLM inference
- **React** - Frontend framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Utility-first CSS
- **shadcn/ui** - Beautiful UI components
- **Recharts** - Data visualization

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/aurexis-ai/issues)
- **Documentation**: See docs folder

---

## 🎯 Roadmap

### ✅ Completed
- [x] Complete frontend architecture (15 pages)
- [x] Backend with 93+ endpoints
- [x] Multi-agent AI system (14 agents)
- [x] Advanced ML forecasting
- [x] Real-time notifications
- [x] WebSocket support
- [x] Rate limiting
- [x] Automated backups
- [x] CI/CD pipeline
- [x] Enhanced logging
- [x] Input validation
- [x] API versioning
- [x] Caching system
- [x] Data export
- [x] Monitoring system

### 🔄 In Progress
- [ ] Admin dashboard
- [ ] Email notifications
- [ ] PDF report generation
- [ ] Multi-factor authentication

### 📅 Future
- [ ] Mobile app
- [ ] Bank account integration (Plaid/Yodlee)
- [ ] Cryptocurrency tracking
- [ ] Social features
- [ ] Advanced analytics dashboard
- [ ] GraphQL API
- [ ] Kubernetes deployment
- [ ] Multi-currency support

---

## 🛠️ Maintenance & Operations

### Automated Backups 💾

**Create Backup**:
```bash
cd backend
python backup_database.py backup
```

**List Backups**:
```bash
python backup_database.py list
```

**Restore from Backup**:
```bash
python backup_database.py restore aurexis_backup_20260501_101133.db
```

### Monitoring 📊

**Check Server Health**:
```bash
curl http://localhost:8000/health
```

Response includes:
- Overall system status
- Component health (database, Redis, Ollama)
- System metrics (CPU, memory, disk)
- Version and environment info

---

**AUREXIS AI** - Enterprise-Grade Financial Intelligence Platform

*Built with ❤️ for financial intelligence*
