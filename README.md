# 🏦 AUREXIS AI - Financial Intelligence Platform

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![React 18](https://img.shields.io/badge/react-18-61dafb.svg)](https://reactjs.org/)
[![Vite](https://img.shields.io/badge/vite-latest-646cff.svg)](https://vitejs.dev/)
[![Docker](https://img.shields.io/badge/docker-ready-2496ed.svg)](https://www.docker.com/)

![AUREXIS AI Dashboard Preview](assets/preview.png)

**Next-Generation AI-powered financial intelligence platform with real-time analytics, risk assessment, and local LLM integration.**

[Features](#-key-features) • [Quick Start](#-quick-start) • [Installation](#-installation--setup) • [Ollama Setup](#-ollama-ai-integration) • [Architecture](#-architecture)

</div>

---

## 🎯 Overview

**AUREXIS AI** is a comprehensive financial decision support system designed to provide institutional-grade insights. By combining advanced machine learning models with a premium, glassmorphic UI, AUREXIS transforms raw financial data into actionable intelligence.

### Why AUREXIS AI?

- **🤖 Local Intelligence**: Privacy-first AI interactions using local LLMs via Ollama.
- **📊 Financial Health DNA**: Dynamic scoring system based on 15+ financial vectors.
- **🔮 Predictive Roadmap**: ML-driven goal achievement forecasting and wealth timelines.
- **🎨 Elite UI/UX**: 3D mouse-reactive components, glassmorphism, and premium micro-animations.
- **💱 Global Ready**: Integrated multi-currency engine (INR/USD) with real-time formatting.

---

## 🚀 Quick Start (Docker)

Run the entire stack with a single command:

```bash
docker-compose up --build
```
*Requires Docker and Docker Compose installed. Ollama must be running locally or in a container.*

---

## ✨ Key Features

### 💎 Intelligence & Analytics
- 📈 **Multi-Dimensional Health Scoring** - Comprehensive assessment of savings, debt, and risk.
- 🎯 **Goal Achievement Roadmap** - Visual timeline for financial milestones and vision boards.
- ⚠️ **Smart Risk Indicators** - Real-time auditing of financial vulnerabilities.
- 🧠 **AI Smart Tips** - Context-aware financial micro-advice generated in real-time.

### 🔮 Predictive Modeling
- 📉 **ML Forecasting** - 6-month expense and income projections using ensemble models.
- 🎲 **Scenario Simulation** - "What-if" modeling for major financial decisions.
- 🛡️ **Fraud & Risk Detection** - AI-powered transaction auditing.

### 🎨 Premium Experience
- 💬 **Floating AI Chat** - Persistent financial advisor available on any page.
- 📄 **Export Suite** - Institutional-quality PDF financial reports.
- 💱 **Dynamic Currency Toggle** - Instant switching between INR (₹) and USD ($).
- 🖱 **Physics-Based UI** - Mouse-reactive cards and 3D parallax effects.

---

## 🛠 Installation & Setup

### 1. Prerequisites
- **Python 3.11+**
- **Node.js 18+**
- **Ollama** (for AI features)

### 2. Ollama AI Integration
AUREXIS AI uses local LLMs for data privacy.
1. Download Ollama from [ollama.com](https://ollama.com).
2. Install and run the Ollama service.
3. Pull the required models:
   ```bash
   ollama pull deepseek-v2:7b
   ```

### 3. Backend Setup
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
python server.py
```

### 4. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

---

## 👥 Authorized Demo Accounts

| User ID | Name | Role |
| :--- | :--- | :--- |
| **1010101010** | SK | Super User / Administrator |
| **1111111111** | Imayavarman | Senior Consultant |
| **1212121212** | Srivarshan | Business Executive |
| **1313131313** | Rahulprasath | Software Architect |
| **1414141414** | Magudesh | Financial Analyst |
| **2020202020** | Deepak | Product Manager |
| **2121212121** | Mani | Operations Head |
| **2222222222** | Dineshkumar | Research Scientist |
| **2525252525** | Avinash | UX Lead |
| **3333333333** | Kumar | Strategy Director |
| **4444444444** | Hari | Security Engineer |
| **5555555555** | Janakrishnan | Data Engineer |

---

## 🌐 Deployment

### Frontend (Vercel)
1. Push your code to GitHub.
2. Import the project into [Vercel](https://vercel.com).
3. Set the **Root Directory** to `frontend`.
4. Add the following **Environment Variables**:
   - `VITE_API_BASE_URL`: Your Render backend URL (e.g., `https://aurexis-api.onrender.com`).
5. Deploy!

### Backend (Render)
1. Create a **Web Service** on [Render](https://render.com).
2. Connect your GitHub repo.
3. Set the **Root Directory** to `backend`.
4. **Build Command**: `pip install -r requirements.txt`
5. **Start Command**: `uvicorn server:app --host 0.0.0.0 --port $PORT`
6. Add the following **Environment Variables**:
   - `JWT_SECRET_KEY`: A secure random string.
   - `FRONTEND_URL`: Your Vercel frontend URL.
   - `ENVIRONMENT`: `production`

---

## 🏗 Architecture

```mermaid
graph TD
    User((User)) -->|React Router| FE[Frontend - Vite/React]
    FE -->|Zustand| State[Global State Management]
    State -->|Fetch API| API[FastAPI Backend]
    API -->|Services| ML[ML Engine - Scikit-learn]
    API -->|Local AI| Ollama[Ollama LLM Runtime]
    API -->|Persistence| JSON[(JSON Data Store)]
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**AUREXIS AI** - Built for the future of Personal Finance.

[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/SenthilkumaranPSK)

</div>
