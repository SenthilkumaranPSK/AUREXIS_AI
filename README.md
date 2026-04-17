# AUREXIS AI — Financial Intelligence Platform

An AI-powered personal finance dashboard with real-time risk analysis, investment tracking, scenario simulation, and a local LLM chat advisor powered by Ollama.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, TypeScript, Vite, Tailwind CSS, shadcn/ui, Framer Motion |
| Backend | FastAPI, Python 3.11, Uvicorn |
| AI Chat | Ollama (local LLM — `deepseek-v3.1:671b-cloud`) |
| State | Zustand |
| Charts | Recharts |
| Routing | React Router v6 |

---

## Project Structure

```
├── backend/
│   ├── server.py          # FastAPI server — auth, chat, data endpoints
│   ├── user_manager.py    # User auth and financial data (hardcoded)
│   ├── user_data/         # Per-user JSON financial data files
│   │   └── {user_number}/
│   ├── requirements.txt
│   └── .env               # Backend environment config
│
└── frontend/
    └── src/
        ├── pages/         # LoginPage, DashboardPage, NotFound
        ├── components/
        │   ├── dashboard/ # MetricCard, Charts, Chat, Panels
        │   ├── layout/    # AppSidebar, AppHeader
        │   └── AnimatedBackground.tsx
        ├── store/         # Zustand global state
        ├── lib/           # API client, formatters
        └── types/         # TypeScript interfaces
```

---

## Prerequisites

- Python 3.11+
- Node.js 18+
- [Ollama](https://ollama.com) installed and running

---

## Setup

### 1. Pull the Ollama model

```bash
ollama pull deepseek-v3.1:671b-cloud
```

Or use a lighter local model:

```bash
ollama pull qwen2.5-coder:3b
```

If using a different model, update `OLLAMA_MODEL` in `backend/.env`.

### 2. Backend

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
python server.py
```

Backend runs at `http://localhost:8000`

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`

---

## Login Credentials

Password format: `Name@2000`

| Name | Password | Occupation | Location |
|------|----------|------------|----------|
| Senthilkumaran | Senthilkumaran@2000 | Software Engineer | Salem |
| Imayavarman | Imayavarman@2000 | Doctor | Erode |
| Srivarshan | Srivarshan@2000 | Business Owner | Theni |
| Rahulprasath | Rahulprasath@2000 | Teacher | Omalur |
| Magudesh | Magudesh@2000 | Freelancer | Bangalore |
| Deepak | Deepak@2000 | CA | Chennai |
| Mani | Mani@2000 | Government Employee | Edapadi |
| Dineshkumar | Dineshkumar@2000 | Lawyer | Sangagari |
| Avinash | Avinash@2000 | IPS | Ambur |
| Kumar | Kumar@2000 | Content Creator | Coimbatore |
| Hari | Hari@2000 | Startup Founder | Karur |
| Janakrishnan | Janakrishnan@2000 | Government Employee | Rasipuram |

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/api/login` | Authenticate user |
| POST | `/api/logout` | End session |
| GET | `/api/users` | List all users |
| GET | `/api/user/{id}/data` | All financial data for user |
| GET | `/api/user/{id}/data/{type}` | Specific data type |
| POST | `/api/chat` | Chat with Ollama AI advisor |

---

## Environment Variables

`backend/.env`:

```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=deepseek-v3.1:671b-cloud
```

---

## Dashboard Features

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
