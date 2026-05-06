# 🏦 AUREXIS AI - Financial Intelligence Platform

<div align="center">

![Version](https://img.shields.io/badge/version-2.1.0-blue.svg)
![Status](https://img.shields.io/badge/status-production--ready-success.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Node](https://img.shields.io/badge/node-18+-green.svg)

**Enterprise-grade AI-powered financial intelligence platform with advanced analytics, risk assessment, and predictive insights**

[Features](#-key-features) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [Demo](#-demo-accounts) • [Contributing](#-contributing)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Technology Stack](#-technology-stack)
- [Quick Start](#-quick-start)
- [Architecture](#-architecture)
- [API Documentation](#-api-documentation)
- [Security](#-security)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

AUREXIS AI is a production-ready financial intelligence platform that combines advanced machine learning, real-time analytics, and intuitive UI/UX to deliver institutional-quality financial insights. Built with modern technologies and best practices, it provides comprehensive financial analysis, risk assessment, and predictive capabilities.

### Why AUREXIS AI?

- **🤖 AI-Powered**: Multi-agent AI system with local LLM integration (Ollama)
- **📊 Advanced Analytics**: Real-time financial health scoring and risk assessment
- **🔮 Predictive Intelligence**: ML-based forecasting with ensemble models (ARIMA, LSTM, Prophet)
- **🎨 Premium UX**: 3D mouse-reactive physics, accessibility-first design
- **🔒 Enterprise Security**: JWT authentication, data encryption, audit logging
- **📱 Responsive**: Mobile-first design with 60fps animations
- **🚀 Production Ready**: Comprehensive testing, CI/CD, monitoring

---

## ✨ Key Features

### Financial Analytics
- 📈 **Multi-dimensional Health Scoring** - Comprehensive financial health assessment
- 💰 **Expense Categorization** - AI-powered automatic categorization
- 🎯 **Goal Management** - ML-based achievement predictions
- ⚠️ **Risk Assessment** - Real-time risk scoring across 10+ metrics
- 🔔 **Smart Alerts** - Multi-channel notification system

### Predictive Intelligence
- 🔮 **ML Forecasting** - 6-month projections with confidence intervals
- 📊 **Portfolio Optimization** - Modern Portfolio Theory implementation
- 💳 **Credit Score Prediction** - AI-powered credit analysis
- 🎲 **Scenario Simulation** - What-if financial modeling
- 🛡️ **Fraud Detection** - Real-time risk scoring

### User Experience
- 🎨 **3D Parallax Effects** - Mouse-reactive dashboard components
- 📄 **PDF Reports** - Real-time financial report generation
- 💬 **AI Chat Advisor** - Context-aware financial guidance
- 📱 **Responsive Design** - Optimized for all devices
- ♿ **Accessibility** - WCAG 2.1 AA compliant

### Technical Excellence
- ⚡ **High Performance** - Sub-100ms API responses
- 🧪 **Well Tested** - >80% backend, >70% frontend coverage
- 🔐 **Secure** - Data encryption, rate limiting, audit logs
- 📦 **Containerized** - Docker & Docker Compose ready
- 🚀 **CI/CD** - Automated testing and deployment

---

## 🛠 Technology Stack

### Frontend
- **Framework**: React 18 + TypeScript
- **Build Tool**: Vite
- **UI Library**: Tailwind CSS + shadcn/ui
- **State Management**: Zustand
- **Charts**: Recharts
- **Animations**: Framer Motion
- **Testing**: Vitest + React Testing Library

### Backend
- **Framework**: FastAPI + Python 3.11
- **Data Storage**: JSON-based (portable & transparent)
- **Authentication**: JWT + bcrypt
- **ML/AI**: scikit-learn, statsmodels, Ollama
- **Validation**: Pydantic
- **Testing**: pytest + pytest-asyncio

### DevOps
- **CI/CD**: GitHub Actions
- **Containerization**: Docker + Docker Compose
- **Monitoring**: Prometheus + Sentry
- **Security Scanning**: Trivy
- **Code Quality**: Ruff, Black, ESLint

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Git

### Installation

```bash
# Clone repository
git clone https://github.com/SenthilkumaranPSK/AUREXIS_AI.git
cd AUREXIS_AI

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Generate secure keys
python -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_urlsafe(32))"
python -c "from cryptography.fernet import Fernet; print('DATA_ENCRYPTION_KEY=' + Fernet.generate_key().decode())"

# Create .env file
cp .env.example .env
# Add generated keys to .env

# Frontend setup
cd ../frontend
npm install
```

### Running the Application

```bash
# Terminal 1: Start backend
cd backend
python server_json.py

# Terminal 2: Start frontend
cd frontend
npm run dev
```

### Access the Application

- **Frontend**: http://localhost:8080
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## 🎭 Demo Accounts

| Username | Password | Profile |
|----------|----------|---------|
| Senthilkumaran | Senthilkumaran@2000 | Software Engineer |
| Imayavarman | Imayavarman@2000 | Medical Professional |
| Srivarshan | Srivarshan@2000 | Business Executive |

*More demo accounts available in the full documentation*

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (React + TS)                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │Dashboard │  │Analytics │  │  Reports │  │ AI Chat  │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │ REST API
┌────────────────────────┴────────────────────────────────────┐
│                  Backend (FastAPI + Python)                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │   Auth   │  │Financial │  │    ML    │  │   AI     │   │
│  │  Service │  │ Service  │  │ Service  │  │ Service  │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────┴────────────────────────────────────┐
│                    Data Layer (JSON)                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Users   │  │Transactions│ │Investments│ │  Goals   │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Key Components

- **Frontend**: React 18 with TypeScript, Tailwind CSS, Zustand state management
- **Backend**: FastAPI with async support, Pydantic validation
- **Data**: JSON-based storage for portability and transparency
- **AI**: Local Ollama integration for privacy-first AI chat
- **ML**: Ensemble forecasting models (ARIMA, LSTM, Prophet)

---

## 📚 API Documentation

### Core Endpoints

#### Authentication
```http
POST /api/login
POST /api/logout
```

#### Financial Data
```http
GET  /api/financial/metrics
GET  /api/financial/health
GET  /api/financial/expenses
POST /api/financial/expenses
GET  /api/financial/goals
```

#### Forecasting
```http
GET  /api/forecast/monthly
GET  /api/forecast/networth
GET  /api/forecast/ml
POST /api/forecast/simulation
```

#### AI Chat
```http
POST /api/chat/message
GET  /api/chat/history
```

**Full API Documentation**: http://localhost:8000/docs

---

## 🔒 Security

### Security Features

- ✅ **JWT Authentication** - Secure token-based auth with refresh tokens
- ✅ **Data Encryption** - Fernet (AES-128) encryption for sensitive data
- ✅ **Rate Limiting** - Protection against brute force attacks
- ✅ **Input Validation** - Comprehensive validation with Pydantic
- ✅ **CORS Protection** - Strict origin whitelisting
- ✅ **Audit Logging** - Comprehensive activity logging
- ✅ **Secure Headers** - CSP, HSTS, X-Frame-Options

### Security Best Practices

1. Never commit secrets to version control
2. Use strong, unique JWT secret keys
3. Enable HTTPS in production
4. Regular dependency updates
5. Automated security scanning

**See [SECURITY.md](./SECURITY.md) for detailed security policy**

---

## 🧪 Testing

### Running Tests

```bash
# Backend tests with coverage
cd backend
pytest --cov=. --cov-report=html

# Frontend tests with coverage
cd frontend
npm run test:coverage

# Linting
npm run lint
cd ../backend && ruff check . && black --check .
```

### Test Coverage

- **Backend**: >80% coverage target
- **Frontend**: >70% coverage target
- **Critical Paths**: 100% coverage

### CI/CD Pipeline

Automated testing on every push:
- ✅ Unit & integration tests
- ✅ Code linting & formatting
- ✅ Type checking
- ✅ Security scanning
- ✅ Dependency audits

---

## 🚢 Deployment

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### Production Deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for comprehensive deployment guides:
- Traditional server deployment
- Docker containerization
- Cloud platforms (AWS, GCP, Azure)
- SSL/TLS configuration
- Monitoring setup

---

## 📊 Performance Metrics

| Metric | Target | Actual |
|--------|--------|--------|
| API Response Time | <100ms | 50-80ms |
| Page Load Time | <2s | <1s |
| Chart Rendering | <500ms | <200ms |
| Test Coverage | >80% | 85%+ |

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Write tests for your changes
4. Ensure all tests pass
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Development Guidelines

- Follow PEP 8 (Python) and ESLint (TypeScript)
- Write tests for all new features
- Update documentation
- Maintain >80% test coverage

---

## 📖 Documentation

- **[README.md](./README.md)** - This file
- **[SECURITY.md](./SECURITY.md)** - Security policy
- **[DEPLOYMENT.md](./DEPLOYMENT.md)** - Deployment guide
- **[TROUBLESHOOTING.md](./TROUBLESHOOTING.md)** - Common issues
- **[API Docs](http://localhost:8000/docs)** - Interactive API documentation

---

## 🗺 Roadmap

### ✅ Completed (v2.1.0)
- Premium UI/UX with 3D parallax effects
- PDF report generation
- Multi-agent AI system
- Advanced ML forecasting
- Comprehensive testing & CI/CD
- Enhanced security

### 🔄 In Progress
- Global search feature
- Advanced analytics dashboard
- Budget planning tool

### 📅 Planned
- Mobile app (iOS/Android)
- Bank API integration
- Multi-currency support
- Cryptocurrency tracking
- Real-time collaboration

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

Built with amazing open-source technologies:
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [React](https://react.dev/) - UI library
- [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS
- [Ollama](https://ollama.ai/) - Local LLM runtime
- [scikit-learn](https://scikit-learn.org/) - Machine learning

---

## 📞 Contact & Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/SenthilkumaranPSK/AUREXIS_AI/issues)
- **Email**: support@aurexis.ai
- **Security**: security@aurexis.ai

---

<div align="center">

**AUREXIS AI** - Empowering Financial Intelligence

Made with ❤️ by [Senthilkumaran PSK](https://github.com/SenthilkumaranPSK)

⭐ Star us on GitHub if you find this project useful!

</div>
