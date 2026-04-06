@echo off
REM Delete old database and run setup

echo [1/2] Deleting old database...
cd C:\Mac\Home\Downloads\csci275
if exist eventlogic.db (
    del eventlogic.db
    echo [OK] Database deleted
) else (
    echo [OK] No old database found
)

REM Clear cache
if exist __pycache__ (
    echo [OK] Clearing Python cache...
    rmdir /s /q __pycache__ 2>nul
)

echo.
echo [2/2] Creating new database with photos...
python seed_data.py

echo.
echo ================================================
echo [OK] Setup Complete!
echo ================================================
echo.
echo Next: Run START_EVENTLOGIC_SERVER.bat
echo.
pause
