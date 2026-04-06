@echo off
REM One-Click EventLogic Launcher - FIXED VERSION
REM This script runs Python to do everything automatically

cd /d "C:\Mac\Home\Downloads\csci275"
cls

title EventLogic - Automatic Setup & Launch

echo.
echo.
echo    ╔════════════════════════════════════════════════════════╗
echo    ║                                                        ║
echo    ║        EventLogic - Full Automatic Setup              ║
echo    ║      Processing everything for you...                 ║
echo    ║                                                        ║
echo    ╚════════════════════════════════════════════════════════╝
echo.
echo.

REM Call Python script for all the work
python AUTO_SETUP.py

echo.
echo.
echo    ========================================================
echo    Setup Complete! EventLogic is starting...
echo    ========================================================
echo.
echo    When ready, open your browser:
echo       http://localhost:5000
echo.
echo    Login with:
echo       Email: john@example.com
echo       Password: custo
echo.
echo    ========================================================
echo.
echo.

python app_eventlogic.py
