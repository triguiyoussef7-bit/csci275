@echo off
REM EventLogic System - Startup Script
REM Complete Event Planning Platform

cls
echo.
echo ================================================================================
echo                       EventLogic System Startup
echo             Complete Event Planning Platform - Production Ready
echo ================================================================================
echo.

cd /d "C:\Mac\Home\Downloads\csci275"

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo ✓ Python found
echo.

REM Check if requirements are installed
python -c "import flask" >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Installing dependencies...
    echo.
    call pip install -r requirements_eventlogic.txt
    if %errorlevel% neq 0 (
        echo ❌ ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

echo ✓ All dependencies installed
echo.

REM Setup database
echo Setting up database...
python setup_eventlogic.py
if %errorlevel% neq 0 (
    echo ❌ ERROR: Database setup failed
    pause
    exit /b 1
)

echo.
echo ================================================================================
echo                    🚀 Starting EventLogic System...
echo ================================================================================
echo.
echo Opening: http://localhost:5000
echo.
echo Press CTRL+C to stop the server
echo.

timeout /t 2

REM Start the application
python app_eventlogic.py

pause
