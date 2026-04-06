@echo off
REM Kill existing Flask server (if running)
taskkill /PID 0 2>nul

REM Delete old database and recreate
del eventlogic.db 2>nul
python seed_data.py

REM Start the Flask server
python app_eventlogic.py
