@echo off
REM ============================================================
REM EventLogic - Auto Setup & Run Fresh
REM Deletes database, installs packages, seeds data, starts server
REM ============================================================

setlocal enabledelayedexpansion
cd /d "C:\Mac\Home\Downloads\csci275"

echo.
echo ============================================================
echo EventLogic - Auto Setup and Run
echo ============================================================
echo.

REM Step 1: Delete database
echo [1/4] Deleting old database...
if exist eventlogic.db (
    del eventlogic.db
    echo [OK] Database deleted
) else (
    echo [OK] No old database found
)

REM Step 2: Install dependencies
echo.
echo [2/4] Installing dependencies...
python -m pip install -q -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo [OK] Packages installed

REM Step 3: Seed database
echo.
echo [3/4] Seeding database...
python seed_data.py
if %errorlevel% neq 0 (
    echo [ERROR] Failed to seed database
    pause
    exit /b 1
)
echo [OK] Database seeded

REM Step 4: Start server
echo.
echo ============================================================
echo [4/4] Starting EventLogic server...
echo ============================================================
echo.
echo [OK] Setup complete! Server starting...
echo.
echo ============================================================
echo.
echo Open your browser and visit:
echo   http://localhost:5000
echo.
echo Demo Accounts:
echo   Vendor:   venue@eventlogic.com / vendor123
echo   Customer: john@example.com / customer123
echo   Admin:    admin@eventlogic.com / admin123
echo.
echo Press Ctrl+C to stop the server
echo.
echo ============================================================
echo.

python app_eventlogic.py

pause
