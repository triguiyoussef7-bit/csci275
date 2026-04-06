@echo off
cls
echo ========================================
echo     DATABASE MIGRATION
echo ========================================
echo.
echo Running database migration script...
echo This will add missing columns to existing database
echo.
cd /d "C:\Mac\Home\Downloads\csci275"
python migrate_database.py
echo.
echo ========================================
echo Migration complete!
echo ========================================
echo.
echo Next steps:
echo 1. Restart Flask server (if running)
echo 2. Type: python app.py
echo 3. Visit: http://localhost:5000
echo 4. Try creating an event again
echo.
pause
