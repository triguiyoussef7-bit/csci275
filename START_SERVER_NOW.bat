@echo off
REM ════════════════════════════════════════════════════════════════════════════
REM   EventLogic - START SERVER NOW
REM ════════════════════════════════════════════════════════════════════════════

cd /d "C:\Mac\Home\Downloads\csci275"

echo.
echo ════════════════════════════════════════════════════════════════════════════
echo   EventLogic - Starting Server
echo ════════════════════════════════════════════════════════════════════════════
echo.

REM Kill any existing Python processes
echo [1/2] Cleaning up old processes...
taskkill /F /IM python.exe 2>nul
timeout /t 1 /nobreak

REM Start server
echo [2/2] Starting Flask server on http://localhost:5000
echo.
echo ════════════════════════════════════════════════════════════════════════════
echo   ✅ SERVER STARTING...
echo ════════════════════════════════════════════════════════════════════════════
echo.
echo   Open your browser: http://localhost:5000
echo.
echo   Press Ctrl+C to stop the server
echo.
echo ════════════════════════════════════════════════════════════════════════════
echo.

python app_eventlogic.py
