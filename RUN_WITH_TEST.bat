@echo off
REM Test system and run diagnostic before starting server

cls
echo.
echo ============================================================
echo     EventLogic - System Diagnostic & Setup
echo ============================================================
echo.

cd /d C:\Mac\Home\Downloads\csci275

echo [STEP 1] Testing system...
echo.
python TEST_SYSTEM.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] System test failed! Check the errors above.
    pause
    exit /b 1
)

echo.
echo [STEP 2] Installing/updating requirements...
pip install -q Flask Flask-Login Flask-SQLAlchemy

echo.
echo [STEP 3] Cleaning up old database...
if exist eventlogic.db (
    del eventlogic.db
    echo [OK] Old database deleted
) else (
    echo [OK] No old database found
)

echo.
echo [STEP 4] Creating fresh database...
python seed_data.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to seed database!
    pause
    exit /b 1
)

echo.
echo ============================================================
echo         [OK] Everything is ready!
echo ============================================================
echo.
echo Starting server now...
echo.
echo Visit: http://localhost:5000
echo Login: john@example.com / customer123
echo.
echo Press Ctrl+C to stop the server
echo ============================================================
echo.

REM Start Flask server
python app_eventlogic.py
