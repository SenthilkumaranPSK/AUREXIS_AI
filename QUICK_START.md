# AUREXIS AI - Quick Start Guide

**Version**: 2.0.0  
**Estimated Setup Time**: 5-10 minutes

---

## Prerequisites

Ensure the following software is installed on your system:

- **Python**: Version 3.11 or higher
- **Node.js**: Version 18 LTS or higher
- **npm**: Version 9.0 or higher (included with Node.js)
- **Git**: Latest stable version

Verify installations:
```bash
python --version  # Should show 3.11+
node --version    # Should show 18+
npm --version     # Should show 9+
```

---

## Installation

### Step 1: Repository Setup

```bash
# Clone the repository
git clone <repository-url>
cd aurexis-ai
```

### Step 2: Backend Configuration

```bash
# Navigate to backend directory
cd backend

# Create Python virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Unix/MacOS:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

### Step 3: Frontend Configuration

```bash
# Navigate to frontend directory
cd ../frontend

# Install Node.js dependencies
npm install
```

---

## Configuration

### Environment Variables (Optional)

For enhanced features, create `backend/.env`:

```env
# JWT Authentication (Recommended for production)
JWT_SECRET_KEY=<your-secure-key>

# AI Chat Integration (Optional - requires Ollama)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=deepseek-v3.1:671b-cloud
```

Generate secure JWT key:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## Launch Application

### Development Mode

Open two terminal windows:

**Terminal 1 - Backend Server:**
```bash
cd backend
python server_json.py
```

Expected output:
```
🚀 AUREXIS AI - JSON-Based Financial Intelligence Platform
✅ No database required - Reading from JSON files
🌐 Server starting on: http://localhost:8000
```

**Terminal 2 - Frontend Server:**
```bash
cd frontend
npm run dev
```

Expected output:
```
VITE ready in XXX ms
➜  Local:   http://localhost:5173/
```

---

## Access Application

1. Open web browser
2. Navigate to: **http://localhost:5173**
3. Use demonstration credentials to login

### Demonstration Accounts

| User ID | Username | Password | Profile |
|---------|----------|----------|---------|
| 22243045 | Senthilkumaran | Senthilkumaran@2000 | Software Engineer |
| 22243017 | Imayavarman | Imayavarman@2000 | Medical Professional |
| 22243050 | Srivarshan | Srivarshan@2000 | Business Executive |

**Note**: Authentication accepts User ID, Username, or Account Number

---

## Verification

### Backend Health Check

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "2.0.0",
  "timestamp": "2026-05-02T..."
}
```

### API Documentation

Access interactive API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Test Authentication

```bash
curl -X POST http://localhost:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username": "22243045", "password": "Senthilkumaran@2000"}'
```

---

## Platform Features

### Dashboard Sections

1. **Overview** - Comprehensive financial summary
2. **Financial Health** - Health score and analysis
3. **Risk Analysis** - Risk assessment and metrics
4. **Savings** - Savings tracking and goals
5. **Debt Management** - Debt analysis and payoff plans
6. **Investments** - Portfolio management
7. **Goals** - Financial goal tracking
8. **Forecasting** - ML-based predictions
9. **Scenario Simulation** - What-if analysis
10. **Alerts** - Notifications and recommendations
11. **Reports** - Financial reports and exports
12. **AI Chat** - Intelligent financial advisor

### Key Capabilities

- Real-time financial metrics
- Interactive data visualizations
- ML-powered forecasting
- Risk assessment tools
- Goal progress tracking
- AI-powered recommendations

---

## Troubleshooting

### Backend Issues

**Port 8000 already in use:**
```bash
# Windows:
netstat -ano | findstr :8000
# Unix/MacOS:
lsof -i :8000

# Kill the process or use different port
```

**Module import errors:**
```bash
pip install -r requirements.txt --force-reinstall
```

### Frontend Issues

**Port 5173 already in use:**
```bash
# Modify vite.config.ts to use different port
# Or kill existing process
```

**Dependency errors:**
```bash
rm -rf node_modules package-lock.json
npm install
```

### Authentication Issues

- Verify credentials are case-sensitive
- Ensure backend server is running
- Check browser console for errors
- Verify API endpoint accessibility

---

## Production Deployment

### Backend (Gunicorn)

```bash
cd backend
gunicorn server:app \
  --workers 4 \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile -
```

### Frontend (Build & Serve)

```bash
cd frontend
npm run build
npx serve -s dist -p 5173
```

### Environment Configuration

Set production environment variables:
```bash
export JWT_SECRET_KEY=<production-key>
export NODE_ENV=production
```

---

## Next Steps

1. **Explore Dashboard**: Navigate through all sections
2. **Test Features**: Try forecasting, simulation, and AI chat
3. **Review API**: Examine API documentation at `/docs`
4. **Customize**: Modify user data in `backend/user_data/`
5. **Deploy**: Follow production deployment guidelines

---

## Additional Resources

- **Full Documentation**: See README.md
- **API Reference**: http://localhost:8000/docs
- **Issue Reporting**: GitHub Issues
- **Support**: Repository discussions

---

## System Architecture

```
┌─────────────────┐
│   Frontend      │  React + TypeScript
│   Port: 5173    │  Vite Development Server
└────────┬────────┘
         │ HTTP/REST
         ↓
┌─────────────────┐
│   Backend       │  FastAPI + Python
│   Port: 8000    │  JSON-based Storage
└────────┬────────┘
         │ File I/O
         ↓
┌─────────────────┐
│   User Data     │  JSON Files
│   user_data/    │  12 Demo Accounts
└─────────────────┘
```

---

**AUREXIS AI** - Enterprise Financial Intelligence Platform

For detailed information, refer to the complete documentation in README.md

**Version 2.0.0** | **Quick Start Guide** | **May 2026**
