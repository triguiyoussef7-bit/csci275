@echo off
REM ════════════════════════════════════════════════════════════════════════════
REM   EventLogic - COMPLETE RESET & FIX
REM ════════════════════════════════════════════════════════════════════════════

setlocal enabledelayedexpansion

cd /d "C:\Mac\Home\Downloads\csci275"

echo.
echo ════════════════════════════════════════════════════════════════════════════
echo   COMPLETE SYSTEM RESET & FIX
echo ════════════════════════════════════════════════════════════════════════════
echo.

REM Kill all Python
echo [1/5] Killing all Python processes...
taskkill /F /IM python.exe 2>nul
timeout /t 2 /nobreak
echo   ✓ Done

REM Remove database
echo [2/5] Removing old database...
if exist eventlogic.db del eventlogic.db 2>nul
if exist __pycache__ rmdir /s /q __pycache__ 2>nul
echo   ✓ Done

REM Install dependencies
echo [3/5] Installing dependencies...
python -m pip install flask flask-login flask-sqlalchemy --quiet
echo   ✓ Done

REM Create database and seed
echo [4/5] Creating fresh database...
python seed_data.py
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Database creation failed!
    pause
    exit /b 1
)
echo   ✓ Database created with admin account

REM Verify admin exists
echo [5/5] Verifying admin account...
python -c "from app_eventlogic import app, db; from models_eventlogic import Admin; app.app_context().push(); admin = Admin.query.filter_by(email='admin@eventlogic.com').first(); print('✓ Admin verified!' if admin else '✗ Admin NOT FOUND')"

echo.
echo ════════════════════════════════════════════════════════════════════════════
echo   ✅ SYSTEM READY - STARTING SERVER
echo ════════════════════════════════════════════════════════════════════════════
echo.
echo   Server will run at: http://localhost:5000
echo.
echo   TEST LOGIN:
echo   ─────────────────────────────────────────────────────────────
echo   Email:    admin@eventlogic.com
echo   Password: admin123
echo   Role:     Admin
echo.
echo   Steps:
echo   1. Browser opens automatically or go to http://localhost:5000
echo   2. Enter admin@eventlogic.com
echo   3. Enter admin123
echo   4. Select "Admin" role
echo   5. Click "Sign In"
echo   6. Should redirect to admin dashboard
echo.
echo ════════════════════════════════════════════════════════════════════════════
echo.

python app_eventlogic.py
