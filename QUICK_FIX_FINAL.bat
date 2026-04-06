@echo off
REM Use PUSHD to handle network paths properly
pushd "C:\Mac\Home\Downloads\csci275"

echo.
echo ════════════════════════════════════════════════════════════════════════════
echo   EventLogic - COMPLETE FIX & RUN
echo ════════════════════════════════════════════════════════════════════════════
echo.

taskkill /F /IM python.exe 2>nul
timeout /t 2 /nobreak

if exist eventlogic.db del eventlogic.db 2>nul

echo [1/5] Installing dependencies...
python -m pip install flask flask-login flask-sqlalchemy --quiet

echo [2/5] Creating database...
python seed_data.py

echo [3/5] Starting server...
echo.
echo ════════════════════════════════════════════════════════════════════════════
echo   ✅ SERVER STARTING AT http://localhost:5000
echo ════════════════════════════════════════════════════════════════════════════
echo.

python app_eventlogic.py

popd
pause
