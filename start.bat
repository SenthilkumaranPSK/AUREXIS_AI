@echo off
setlocal enabledelayedexpansion

echo ========================================
echo   AUREXIS AI - Startup Script
echo ========================================
echo.

REM Check if Python is available
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.11+ and try again
    pause
    exit /b 1
)

REM Check if Node is available
where npm >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Node.js/npm is not installed or not in PATH
    echo Please install Node.js and try again
    pause
    exit /b 1
)

echo [1/3] Setting up Backend...
cd /d "%~dp0backend"
if exist "venv\Scripts\python.exe" (
    echo Using virtual environment...
    set PYTHON_EXE=venv\Scripts\python.exe
) else (
    echo [WARNING] Virtual environment not found. Using system python.
    set PYTHON_EXE=python
)

REM Optional: Install requirements if needed
REM %PYTHON_EXE% -m pip install -r requirements.txt

start "AUREXIS Backend" cmd /k "%PYTHON_EXE% server.py"
timeout /t 3 /nobreak >nul

echo [2/3] Backend server started
echo.

echo [3/3] Setting up Frontend...
cd /d "%~dp0frontend"
if not exist "node_modules" (
    echo [INFO] node_modules not found. Running npm install...
    call npm install
)

start "AUREXIS Frontend" cmd /k "npm run dev"

echo.
echo ========================================
echo   AUREXIS AI is starting...
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Backend API Docs: http://localhost:8000/docs
echo Frontend: http://localhost:5173
echo.
echo To stop the servers, close the command windows
echo ========================================

pause >nul
