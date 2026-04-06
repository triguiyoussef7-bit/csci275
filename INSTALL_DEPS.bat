@echo off
echo ================================================================================
echo                    EventLogic System - Installing Dependencies
echo ================================================================================
echo.

echo [1/6] Installing Flask...
python -m pip install Flask==2.3.3

echo [2/6] Installing Flask-SQLAlchemy...
python -m pip install Flask-SQLAlchemy==3.0.5

echo [3/6] Installing Flask-Login...
python -m pip install Flask-Login==0.6.2

echo [4/6] Installing Werkzeug...
python -m pip install Werkzeug==2.3.7

echo [5/6] Installing SQLAlchemy...
python -m pip install SQLAlchemy==2.0.21

echo [6/6] Installing python-dotenv...
python -m pip install python-dotenv==1.0.0

echo.
echo ================================================================================
echo SUCCESS: All dependencies installed!
echo ================================================================================
echo.
echo Next step: Run setup_eventlogic.py
echo   python setup_eventlogic.py
echo.
pause
