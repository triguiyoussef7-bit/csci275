@echo off
REM EVENTLOGIC - SIMPLE STARTUP SCRIPT
REM Just run this file and it will work!

REM Get the directory where this script is located
cd /d "%~dp0"

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║           🚀 EventLogic Startup Script 🚀                ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo Project directory: %cd%
echo.

REM Kill any running Python processes
echo [1/4] Stopping any running servers...
tasklist /FI "IMAGENAME eq python.exe" 2>NUL | find /I /N "python.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo       ✓ Found running Python processes, stopping...
    taskkill /F /IM python.exe >nul 2>&1
    timeout /t 2 /nobreak >nul
) else (
    echo       ✓ No Python processes running
)

REM Delete old database
echo.
echo [2/4] Cleaning up old database...
if exist eventlogic.db (
    del eventlogic.db >nul 2>&1
    echo       ✓ Old database deleted
) else (
    echo       ✓ No old database found
)

REM Create fresh database
echo.
echo [3/4] Creating fresh database...
python seed_data.py
if errorlevel 1 (
    echo.
    echo ❌ ERROR: Could not create database
    echo.
    echo Make sure:
    echo   1. You're in the right directory: %cd%
    echo   2. Python is installed: python --version
    echo   3. You have pip packages: pip install flask sqlalchemy
    echo.
    pause
    exit /b 1
)
echo       ✓ Database created with sample data

REM Start the server
echo.
echo [4/4] Starting Flask server...
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                  ✅ SERVER STARTING!                       ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo 📍 Open your browser and go to:
echo    http://localhost:5000
echo.
echo 👤 Login with:
echo    Email:    john@example.com
echo    Password: custo
echo.
echo 🎉 Then click "Plan Your Event" to try the new feature!
echo.
echo Press Ctrl+C in this window to stop the server
echo.

python app_eventlogic.py

echo.
echo Server stopped.
pause
