@echo off
REM ════════════════════════════════════════════════════════════════════════════
REM   EventLogic - COMPLETE AUTOMATED SETUP & RUN
REM ════════════════════════════════════════════════════════════════════════════

setlocal enabledelayedexpansion

cd /d "C:\Mac\Home\Downloads\csci275"

echo.
echo ════════════════════════════════════════════════════════════════════════════
echo   EventLogic - Complete Setup & Launch
echo ════════════════════════════════════════════════════════════════════════════
echo.

REM ════════════════════════════════════════════════════════════════════════════
REM STEP 1: Stop any running Flask servers
REM ════════════════════════════════════════════════════════════════════════════
echo [STEP 1] Stopping any running Python servers...
taskkill /F /IM python.exe 2>nul
timeout /t 2 /nobreak

REM ════════════════════════════════════════════════════════════════════════════
REM STEP 2: Delete old database
REM ════════════════════════════════════════════════════════════════════════════
echo [STEP 2] Cleaning up old database...
if exist eventlogic.db (
    del eventlogic.db 2>nul
    echo   ✓ Old database removed
)

REM ════════════════════════════════════════════════════════════════════════════
REM STEP 3: Install/update dependencies
REM ════════════════════════════════════════════════════════════════════════════
echo [STEP 3] Installing dependencies...
python -m pip install flask flask-login flask-sqlalchemy -q
echo   ✓ Dependencies installed

REM ════════════════════════════════════════════════════════════════════════════
REM STEP 4: Seed the database
REM ════════════════════════════════════════════════════════════════════════════
echo [STEP 4] Seeding database with test data...
python seed_data.py >nul 2>&1
if %errorlevel% equ 0 (
    echo   ✓ Database seeded successfully
) else (
    echo   ✗ Error seeding database
    pause
    exit /b 1
)

REM ════════════════════════════════════════════════════════════════════════════
REM STEP 5: Launch Flask server
REM ════════════════════════════════════════════════════════════════════════════
echo [STEP 5] Starting Flask server...
echo.
echo ════════════════════════════════════════════════════════════════════════════
echo   ✅ READY TO USE!
echo ════════════════════════════════════════════════════════════════════════════
echo.
echo   Server starting at: http://localhost:5000
echo.
echo   TEST ACCOUNTS:
echo   ─────────────────────────────────────────────────────────────
echo   ADMIN:
echo     Email:    admin@eventlogic.com
echo     Password: admin123
echo.
echo   CUSTOMER:
echo     Email:    john@example.com
echo     Password: customer123
echo.
echo   VENDOR:
echo     Email:    venue@eventlogic.com
echo     Password: vendor123
echo.
echo ════════════════════════════════════════════════════════════════════════════
echo.

python app_eventlogic.py

pause
