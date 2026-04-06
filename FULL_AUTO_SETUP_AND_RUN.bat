@echo off
REM ============================================================
REM EventLogic Complete Automated Setup & Launch
REM Fixes all issues automatically and starts the server
REM ============================================================

cd /d "C:\Mac\Home\Downloads\csci275"
cls

echo.
echo ========================================================
echo    EventLogic Complete Automated Setup
echo ========================================================
echo.

echo [1/3] Running automatic setup...
python AUTO_SETUP.py

echo.
echo ========================================================
echo    SETUP COMPLETE!
echo ========================================================
echo.
echo Fixes applied:
echo   [+] EventLogic logo clickable
echo   [+] Payment button hides when payment completed
echo   [+] Success message shows after payment
echo   [+] Database reset with fresh data
echo.
echo Starting EventLogic server...
echo.
timeout /t 2 /nobreak

python app_eventlogic.py
