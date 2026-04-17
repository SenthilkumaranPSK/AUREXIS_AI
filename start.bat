@echo off
setlocal enabledelayedexpansion

echo ========================================
echo   AUREXIS AI - Startup Script
echo ========================================
echo.

REM Check Python
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python not found. Install Python 3.11+ and try again.
    pause & exit /b 1
)

REM Check Node
where npm >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Node.js not found. Install Node.js and try again.
    pause & exit /b 1
)

REM Check Ollama
where ollama >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [WARNING] Ollama not found. AI chat will not work.
    echo Download from: https://ollama.com
    echo.
)

echo [1/3] Starting Backend...
cd /d "%~dp0backend"

REM Use venv if it exists, otherwise use system Python
if exist "venv\Scripts\python.exe" (
    set PYTHON_EXE=venv\Scripts\python.exe
) else (
    set PYTHON_EXE=python
)

start "AUREXIS Backend" cmd /k "%PYTHON_EXE% server.py"
timeout /t 3 /nobreak >nul
echo Backend started on http://localhost:8000
echo.

echo [2/3] Starting Frontend...
cd /d "%~dp0frontend"
if not exist "node_modules" (
    echo Installing frontend dependencies...
    call npm install
)
start "AUREXIS Frontend" cmd /k "npm run dev"
echo Frontend started on http://localhost:5173
echo.

echo [3/3] Starting Ollama...
start "AUREXIS Ollama" cmd /k "ollama serve"
timeout /t 2 /nobreak >nul
echo.

echo ========================================
echo   AUREXIS AI is running!
echo ========================================
echo   Backend:  http://localhost:8000
echo   Docs:     http://localhost:8000/docs
echo   Frontend: http://localhost:5173
echo ========================================
echo   Close the opened windows to stop.
echo ========================================
pause >nul
