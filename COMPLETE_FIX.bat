@echo off
REM COMPLETE FIX FOR EVENTLOGIC
REM This script will:
REM 1. Show current status
REM 2. Delete old database
REM 3. Create new database
REM 4. Test database
REM 5. Show if it works

setlocal enabledelayedexpansion

cd /d C:\Mac\Home\Downloads\csci275

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║          EVENTLOGIC COMPLETE FIX SCRIPT                    ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Step 1: Check current database
echo [STEP 1] Checking current database...
if exist eventlogic.db (
    echo   Found: eventlogic.db (will delete)
) else (
    echo   Not found: OK to proceed
)

REM Step 2: Delete old database
echo.
echo [STEP 2] Deleting old database...
if exist eventlogic.db (
    del eventlogic.db
    echo   ✓ Deleted eventlogic.db
) else (
    echo   ✓ No old database
)

REM Step 3: Delete cache
echo.
echo [STEP 3] Clearing Python cache...
if exist __pycache__ (
    rmdir /s /q __pycache__
    echo   ✓ Cache cleared
) else (
    echo   ✓ No cache to clear
)

REM Step 4: Create fresh database
echo.
echo [STEP 4] Creating fresh database with seed data...
python seed_data.py
if !errorlevel! neq 0 (
    echo   ✗ ERROR: Seed script failed!
    echo   Check error message above
    pause
    exit /b 1
)
echo   ✓ Database created successfully

REM Step 5: Test database
echo.
echo [STEP 5] Testing database...
python DIAGNOSE.py
if !errorlevel! neq 0 (
    echo   ✗ Diagnostic test failed
)

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║               SETUP COMPLETE!                              ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo NEXT STEPS:
echo   1. Close this window
echo   2. Double-click: START_EVENTLOGIC_SERVER.bat
echo   3. Open browser: http://localhost:5000
echo   4. Login:
echo      Email: admin@eventlogic.com
echo      Password: admin123
echo.
pause
