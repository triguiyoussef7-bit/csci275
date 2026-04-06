@echo off
echo [1/2] Deleting old database...
if exist eventlogic.db del eventlogic.db
if exist __pycache__ rmdir /s /q __pycache__
echo [OK] Database deleted

echo.
echo [2/2] Creating new database with seed data...
cd /Mac/Home/Downloads/csci275
python seed_data.py

echo.
echo [OK] Database reset and seeded! Photos added to all services.
echo.
pause
