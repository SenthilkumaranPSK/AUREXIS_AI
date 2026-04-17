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
│   ├── user_manager.py    # User auth and financial data loading
│   ├── user_data/         # Per-user JSON financial data files
│   │   └── {user_number}/
│   ├── requirements.txt
│   └── .env               # Backend environment config
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

## Login

Credentials are name-based — the username and password are the same value (case-insensitive).

| Name | Password | Occupation |
|------|----------|------------|
| Senthilkumaran | Senthilkumaran@2000 | Software Engineer |
| Imayavarman | Imayavarman@2000 | Doctor |
| Srivarshan | Srivarshan@2000 | Business Owner |
| Rahulprasath | Rahulprasath@2000 | Teacher |
| Magudesh | Magudesh@2000 | Freelancer |
| Deepak | Deepak@2000 | CA |
| Mani | Mani@2000 | Government Employee |
| Dineshkumar | Dineshkumar@2000 | Lawyer |
| Avinash | Avinash@2000 | IPS |
| Kumar | Kumar@2000 | Content Creator |
| Hari | Hari@2000 | Startup Founder |
| Janakrishnan | Janakrishnan@2000 | Government Employee |

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

## Features

- **Dashboard** — Net worth, income, expenses, savings rate, credit score, health score
- **Financial Health** — Score gauge, trend analysis, recommendations
- **Risk Analysis** — Debt-to-income ratio, risk level assessment
- **Investments** — Portfolio breakdown, allocation, returns
- **Goals** — Progress tracking with monthly savings targets
- **Scenario Simulator** — What-if modeling for loans, salary changes, job loss
- **Forecasting** — 6-month income/expense/savings projection
- **AI Chat** — Personalized financial advice via local Ollama LLM
- **Animated Background** — Canvas-based moving gradient mesh
- **Dark / Light theme** — Toggle in the header
