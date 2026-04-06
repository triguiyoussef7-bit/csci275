@echo off
REM Complete installation and setup for EventLogic
REM This installs all dependencies, sets up database, and starts server

cls
echo.
echo ============================================================
echo         EventLogic - Complete Setup & Installation
echo ============================================================
echo.

cd /d C:\Mac\Home\Downloads\csci275

REM Step 1: Install/Update Python packages
echo [STEP 1/4] Installing required Python packages...
echo This may take a moment...
echo.

python -m pip install --upgrade pip > nul 2>&1

pip install -q Flask==2.3.3
pip install -q Flask-SQLAlchemy==3.0.5
pip install -q Flask-Login==0.6.2
pip install -q SQLAlchemy==2.0.21
pip install -q Werkzeug==2.3.7

if %errorlevel% neq 0 (
    echo [ERROR] Failed to install packages!
    echo Please run: pip install -r requirements.txt
    pause
    exit /b 1
)

echo [OK] All packages installed!
echo.

REM Step 2: Delete old database
echo [STEP 2/4] Preparing database...
if exist eventlogic.db (
    del eventlogic.db
    echo [OK] Old database deleted
) else (
    echo [OK] No old database found
)
echo.

REM Step 3: Seed database
echo [STEP 3/4] Creating fresh database with sample data...
python seed_data.py

if %errorlevel% neq 0 (
    echo [ERROR] Failed to seed database!
    echo Check seed_data.py for errors.
    pause
    exit /b 1
)

echo [OK] Database created!
echo.

REM Step 4: Start server
echo [STEP 4/4] Starting EventLogic server...
echo.
echo ============================================================
echo                  [OK] READY TO USE!
echo ============================================================
echo.
echo  Your EventLogic server is starting...
echo.
echo  OPEN YOUR BROWSER AND VISIT:
echo    http://localhost:5000
echo.
echo  LOGIN WITH:
echo    Email:    john@example.com
echo    Password: customer123
echo.
echo  FEATURES READY:
echo    ✓ Service images (emoji display)
echo    ✓ Budget calculator
echo    ✓ Booking system
echo    ✓ All navigation working
echo.
echo  TO STOP:
echo    Press Ctrl+C in this window
echo.
echo ============================================================
echo.

python app_eventlogic.py
