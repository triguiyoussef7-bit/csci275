@echo off
REM Simple restart
pushd "\\mac\Home\Downloads\csci275"
taskkill /F /IM python.exe 2>nul
timeout /t 2 /nobreak
python seed_data.py
python app_eventlogic.py
