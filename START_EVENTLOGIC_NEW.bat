@echo off
REM EventLogic - Automatic Setup & Start
REM This will:
REM 1. Change to project directory
REM 2. Kill any running Python processes
REM 3. Delete old database
REM 4. Create fresh database with seed data
REM 5. Start the Flask server

REM Change to project directory
cd /d C:\Mac\Home\Downloads\csci275

echo.
echo ========================================
echo   EventLogic - Automatic Setup
echo ========================================
echo.
echo Project directory: %cd%
echo.

REM Find and kill Python processes
echo Stopping any running Flask server...
tasklist | find /I "python.exe" >nul 2>&1
if not errorlevel 1 (
    for /f "tokens=2" %%A in ('tasklist ^| find /I "python.exe"') do (
        echo Killing process %%A...
        taskkill /PID %%A /F 2>nul
    )
) else (
    echo No Python processes found.
)

REM Wait a moment
timeout /t 2 /nobreak >nul

REM Delete old database
echo.
echo Deleting old database...
if exist eventlogic.db (
    del eventlogic.db
    echo ✓ Database deleted.
) else (
    echo ✓ No old database found.
)

REM Create new database
echo.
echo Creating fresh database with seed data...
python seed_data.py
if errorlevel 1 (
    echo.
    echo ❌ ERROR: Failed to create database
    echo Make sure you're in the correct directory: %cd%
    echo Check that Python is installed: python --version
    pause
    exit /b 1
)
echo ✓ Database ready!

REM Start Flask server
echo.
echo ========================================
echo   Starting Flask Server...
echo ========================================
echo.
echo ✓ Server starting...
echo.
echo 📍 Server running at: http://localhost:5000
echo.
echo 👤 LOGIN CREDENTIALS:
echo    Email: john@example.com
echo    Password: custo
echo.
echo 🎉 NEW FEATURE:
echo    1. Click "Plan Your Event" on dashboard
echo    2. Select event type (Wedding, Birthday, etc)
echo    3. Enter budget and date
echo    4. Get vendor recommendations!
echo.
echo ========================================
echo.
echo Press Ctrl+C to stop the server
echo.

python app_eventlogic.py

pause
