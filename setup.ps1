# AUREXIS AI - Quick Setup Script (PowerShell)
# This script automates the setup process for development on Windows

$ErrorActionPreference = "Stop"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  AUREXIS AI v2.0 - Quick Setup" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python 3 is not installed" -ForegroundColor Red
    exit 1
}

# Check if Node.js is installed
try {
    $nodeVersion = node --version 2>&1
    Write-Host "✓ Node.js found: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js is not installed" -ForegroundColor Red
    exit 1
}

# Backend setup
Write-Host ""
Write-Host "📦 Setting up backend..." -ForegroundColor Yellow
Set-Location backend

# Create virtual environment
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv venv
}

# Activate virtual environment
& .\venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "Installing Python dependencies..."
pip install -r requirements.txt | Out-Null

Write-Host "✓ Backend dependencies installed" -ForegroundColor Green

# Check if .env exists
if (-not (Test-Path ".env")) {
    Write-Host "⚠  .env file not found, using defaults" -ForegroundColor Yellow
}

# Create logs directory
New-Item -ItemType Directory -Force -Path logs | Out-Null

# Initialize database
Write-Host "Initializing database..."
python migrate.py

Write-Host "✓ Database initialized" -ForegroundColor Green

Set-Location ..

# Frontend setup
Write-Host ""
Write-Host "📦 Setting up frontend..." -ForegroundColor Yellow
Set-Location frontend

# Install dependencies
Write-Host "Installing Node.js dependencies..."
npm install | Out-Null

Write-Host "✓ Frontend dependencies installed" -ForegroundColor Green

Set-Location ..

# Check if Ollama is installed
Write-Host ""
Write-Host "🤖 Checking Ollama..." -ForegroundColor Yellow
try {
    $ollamaVersion = ollama --version 2>&1
    Write-Host "✓ Ollama found" -ForegroundColor Green
    
    # Check if model is pulled
    $models = ollama list 2>&1
    if ($models -match "deepseek-v3.1:671b-cloud") {
        Write-Host "✓ Model already pulled" -ForegroundColor Green
    } else {
        Write-Host "⚠  Model not found. Pull with: ollama pull deepseek-v3.1:671b-cloud" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠  Ollama not found. Install from: https://ollama.com" -ForegroundColor Yellow
}

# Check if Redis is running (optional)
Write-Host ""
Write-Host "💾 Checking Redis..." -ForegroundColor Yellow
try {
    $redisCheck = redis-cli ping 2>&1
    if ($redisCheck -eq "PONG") {
        Write-Host "✓ Redis is running" -ForegroundColor Green
    } else {
        Write-Host "⚠  Redis is installed but not running. Start with: redis-server" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠  Redis not found (optional). Will use in-memory cache." -ForegroundColor Yellow
}

# Summary
Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  ✅ Setup Complete!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To start the application:" -ForegroundColor White
Write-Host ""
Write-Host "  Backend:" -ForegroundColor Yellow
Write-Host "    cd backend"
Write-Host "    .\venv\Scripts\Activate.ps1"
Write-Host "    python server.py"
Write-Host ""
Write-Host "  Frontend:" -ForegroundColor Yellow
Write-Host "    cd frontend"
Write-Host "    npm run dev"
Write-Host ""
Write-Host "Then open: http://localhost:5173" -ForegroundColor Cyan
Write-Host ""
Write-Host "📚 Documentation:" -ForegroundColor Yellow
Write-Host "  - README.md - Getting started"
Write-Host "  - IMPROVEMENTS.md - What's new in v2.0"
Write-Host "  - DEPLOYMENT.md - Production deployment"
Write-Host "  - TRANSFORMATION_SUMMARY.md - Complete overview"
Write-Host ""
Write-Host "🔐 Default login:" -ForegroundColor Yellow
Write-Host "  Username: Senthilkumaran"
Write-Host "  Password: Senthilkumaran@2000"
Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
