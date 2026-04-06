@echo off
cls
echo ========================================
echo     FIXING DATABASE ERROR
echo ========================================
echo.
echo Deleting old database...
del /Q database.db 2>nul
echo ✓ Old database deleted
echo.
echo ========================================
echo Next: Stop the Flask server and restart
echo ========================================
echo.
echo Steps:
echo   1. Press CTRL+C in the Flask server window
echo   2. Run: python app.py
echo   3. Visit: http://localhost:5000
echo.
echo The database will recreate automatically
echo with all the new columns!
echo.
pause
