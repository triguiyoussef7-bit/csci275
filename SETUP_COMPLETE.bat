@echo off
REM Complete setup and test for EventLogic
REM This script will:
REM 1. Delete old database
REM 2. Create fresh database with seeds
REM 3. Test admin login credentials
REM 4. Verify database is populated

echo.
echo ================================================
echo EventLogic Complete Setup & Test
echo ================================================
echo.

REM Step 1: Delete old database
echo [1/3] Cleaning up old database...
if exist eventlogic.db (
    del eventlogic.db
    echo [OK] Old database deleted
) else (
    echo [OK] No old database found
)

if exist __pycache__ (
    rmdir /s /q __pycache__
)

echo.

REM Step 2: Create new database with seed data
echo [2/3] Creating new database with sample data...
python seed_data.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Seed script failed!
    echo Please check the error message above.
    pause
    exit /b 1
)

echo.
echo [OK] Database seeded successfully!
echo.

REM Step 3: Test the database
echo [3/3] Testing database setup...
python TEST_SETUP.py

echo.
echo ================================================
echo [OK] Setup Complete!
echo ================================================
echo.
echo Next steps:
echo 1. Run: START_EVENTLOGIC_SERVER.bat
echo 2. Visit: http://localhost:5000
echo 3. Login as Admin:
echo    Email: admin@eventlogic.com
echo    Password: admin123
echo    Role: Admin
echo.
pause
