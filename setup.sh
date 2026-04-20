#!/bin/bash

# AUREXIS AI - Quick Setup Script
# This script automates the setup process for development

set -e

echo "=========================================="
echo "  AUREXIS AI v2.0 - Quick Setup"
echo "=========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✓${NC} Python 3 found"

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✓${NC} Node.js found"

# Backend setup
echo ""
echo "📦 Setting up backend..."
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate || source venv/Scripts/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt > /dev/null 2>&1

echo -e "${GREEN}✓${NC} Backend dependencies installed"

# Check if .env exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠${NC}  .env file not found, using defaults"
fi

# Create logs directory
mkdir -p logs

# Initialize database
echo "Initializing database..."
python migrate.py

echo -e "${GREEN}✓${NC} Database initialized"

cd ..

# Frontend setup
echo ""
echo "📦 Setting up frontend..."
cd frontend

# Install dependencies
echo "Installing Node.js dependencies..."
npm install > /dev/null 2>&1

echo -e "${GREEN}✓${NC} Frontend dependencies installed"

cd ..

# Check if Ollama is installed
echo ""
echo "🤖 Checking Ollama..."
if command -v ollama &> /dev/null; then
    echo -e "${GREEN}✓${NC} Ollama found"
    
    # Check if model is pulled
    if ollama list | grep -q "deepseek-v3.1:671b-cloud"; then
        echo -e "${GREEN}✓${NC} Model already pulled"
    else
        echo -e "${YELLOW}⚠${NC}  Model not found. Pull with: ollama pull deepseek-v3.1:671b-cloud"
    fi
else
    echo -e "${YELLOW}⚠${NC}  Ollama not found. Install from: https://ollama.com"
fi

# Check if Redis is running (optional)
echo ""
echo "💾 Checking Redis..."
if command -v redis-cli &> /dev/null; then
    if redis-cli ping > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} Redis is running"
    else
        echo -e "${YELLOW}⚠${NC}  Redis is installed but not running. Start with: redis-server"
    fi
else
    echo -e "${YELLOW}⚠${NC}  Redis not found (optional). Will use in-memory cache."
fi

# Summary
echo ""
echo "=========================================="
echo "  ✅ Setup Complete!"
echo "=========================================="
echo ""
echo "To start the application:"
echo ""
echo "  Backend:"
echo "    cd backend"
echo "    source venv/bin/activate  # or venv\\Scripts\\activate on Windows"
echo "    python server.py"
echo ""
echo "  Frontend:"
echo "    cd frontend"
echo "    npm run dev"
echo ""
echo "Then open: http://localhost:5173"
echo ""
echo "📚 Documentation:"
echo "  - README.md - Getting started"
echo "  - IMPROVEMENTS.md - What's new in v2.0"
echo "  - DEPLOYMENT.md - Production deployment"
echo "  - TRANSFORMATION_SUMMARY.md - Complete overview"
echo ""
echo "🔐 Default login:"
echo "  Username: Senthilkumaran"
echo "  Password: Senthilkumaran@2000"
echo ""
echo "=========================================="
