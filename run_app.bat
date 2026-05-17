@echo off
title AUREXIS AI - Intelligence Dashboard
setlocal enabledelayedexpansion

:: Set colors (Blue/Cyan/White)
color 0B

:: Clear screen
cls

echo.
echo  [94m###################################################################[0m
echo  [94m#[0m                                                                 [94m#[0m
echo  [94m#[0m   [96m  ___   _   _  ____   _____  __  __  ___  ____      _     ___  [94m#[0m
echo  [94m#[0m   [96m / _ \ ^| ^| ^| ^|^|  _ \ ^| ____^| \ \/ / ^|_ _^|/ ___^|    / \   ^|_ _^| [94m#[0m
echo  [94m#[0m   [96m^| ^|_^| ^|^| ^| ^| ^|^| ^|_^| ^|^|  _^|    \  /   ^| ^| \___ \   / _ \   ^| ^|  [94m#[0m
echo  [94m#[0m   [96m^|  _  ^|^| ^|_^| ^|^|  _ / ^| ^|___   /  \   ^| ^|  ___) ^| / ___ \  ^| ^|  [94m#[0m
echo  [94m#[0m   [96m^|_^| ^|_^| \___/ ^|_^| \_\ ^|_____^| /_/\_\ ^|___^|^|____/ /_/   \_\^|___^| [94m#[0m
echo  [94m#[0m                                                                 [94m#[0m
echo  [94m#[0m              [97mNEXT-GEN FINANCIAL INTELLIGENCE PLATFORM[0m           [94m#[0m
echo  [94m###################################################################[0m
echo.

echo [90m[SYSTEM][0m Initializing AUREXIS AI environment...
timeout /t 1 >nul

:: --- Backend Startup ---
echo [90m[BACKEND][0m Starting Python API Service...
:: Using start to run in a separate terminal as requested
start "AUREXIS Backend Server" cmd /k "cd backend && call venv\Scripts\activate && python server.py"

echo [92m[OK][0m Backend sequence initiated.
timeout /t 3 >nul

:: --- Frontend Startup ---
echo [90m[FRONTEND][0m Launching Interactive Dashboard on Port 8080...
:: Using start to run in a separate terminal as requested
start "AUREXIS Frontend Dev" cmd /k "cd frontend && npm run dev"

echo [92m[OK][0m Frontend engine warming up.
timeout /t 2 >nul

:: --- Final Animation & Launch ---
echo.
echo [96m[STATUS][0m Syncing Neural Bridges...
echo [94m[[97m====                [94m] 20%%[0m
timeout /t 1 >nul
echo [94m[[97m========            [94m] 45%%[0m
timeout /t 1 >nul
echo [94m[[97m============        [94m] 70%%[0m
timeout /t 1 >nul
echo [94m[[97m====================[94m] 100%%[0m
echo.
echo [92m[SUCCESS][0m AUREXIS AI is now active.
echo [97mLocal URL:[0m [96mhttp://localhost:8080[0m
echo.

:: Open browser
start http://localhost:8080

echo [90mTerminals are running in the background.[0m
echo [90mPress any key to close this dashboard...[0m
pause >nul
exit
