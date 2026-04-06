@echo off
REM ============================================================
REM EventLogic - Simple One-Click Setup
REM This is the SIMPLEST version - just runs the Python script
REM ============================================================

cd /d "C:\Mac\Home\Downloads\csci275"
cls

echo.
echo ========================================================
echo         EventLogic Automatic Setup
echo ========================================================
echo.
echo Running all setup steps automatically...
echo.

REM Just run the Python script - it does everything!
python AUTO_SETUP.py

REM After setup is done, ask if user wants to start server
echo.
echo ========================================================
echo    Ready! Starting EventLogic server...
echo ========================================================
echo.

REM Start the server
python app_eventlogic.py
