@echo off
cls
cd /d "C:\Mac\Home\Downloads\csci275"

echo.
echo ================================================
echo    EventLogic Automatic Setup Running...
echo ================================================
echo.

python AUTO_SETUP.py

echo.
echo Setup complete! You can now run:
echo   python app_eventlogic.py
echo.
pause
