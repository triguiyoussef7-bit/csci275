@echo off
REM Delete the old broken app and use the fixed version
cd /d "C:\Mac\Home\Downloads\csci275"

echo.
echo ================================================
echo       EventLogic Server - Quick Fix
echo ================================================
echo.

REM Backup old app
if exist app_eventlogic.py (
    ren app_eventlogic.py app_eventlogic_broken.py
    echo [OK] Backed up old app to app_eventlogic_broken.py
)

REM Use the fixed app
if exist app_fixed.py (
    ren app_fixed.py app_eventlogic.py
    echo [OK] Installed fixed app as app_eventlogic.py
)

echo.
echo Starting Flask server...
echo.

python app_eventlogic.py

pause
