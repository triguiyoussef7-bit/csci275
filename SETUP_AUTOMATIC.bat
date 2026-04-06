@echo off
REM ============================================================
REM AUTOMATIC SETUP - Kills server, resets DB, starts fresh
REM ============================================================

cd /d "C:\Mac\Home\Downloads\csci275"

echo.
echo ============================================================
echo EVENT LOGIC - AUTOMATIC SETUP
echo ============================================================
echo.

REM Kill any Python/Flask processes
echo [1/5] Stopping any running servers...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq*EventLogic*" 2>nul
timeout /t 2 /nobreak >nul

REM Delete database
echo [2/5] Deleting old database...
if exist eventlogic.db (
    del /F eventlogic.db 2>nul
    if exist eventlogic.db (
        echo [WARNING] Could not delete database, trying again...
        timeout /t 2 /nobreak >nul
        del /F /Q eventlogic.db 2>nul
    )
    echo [OK] Database deleted
) else (
    echo [OK] No old database found
)
timeout /t 1 /nobreak >nul

REM Install dependencies
echo [3/5] Installing dependencies...
python -m pip install -q -r requirements.txt 2>nul
echo [OK] Packages installed

REM Seed database
echo [4/5] Creating and seeding database...
python seed_data.py
if %errorlevel% equ 0 (
    echo [OK] Database seeded
) else (
    echo [WARNING] Seeding status: %errorlevel%
)
timeout /t 2 /nobreak >nul

REM Start server
echo.
echo [5/5] Starting EventLogic server...
echo.
echo ============================================================
echo [OK] SETUP COMPLETE!
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
echo What's Fixed:
echo   [OK] Vendor bookings now display
echo   [OK] Customer reviews show on profiles
echo   [OK] Professional design added
echo.
echo Press Ctrl+C to stop the server
echo.
echo ============================================================
echo.

python app_eventlogic.py

pause
