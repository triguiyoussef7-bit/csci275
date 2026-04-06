@echo off
chcp 65001 > nul
echo ================================================================================
echo                     Fixing Python Environment
echo ================================================================================
echo.

echo Checking which Python is active...
python --version
python -c "import sys; print(f'Location: {sys.executable}')"

echo.
echo Installing Flask to this Python...
python -m pip install --upgrade pip
python -m pip install Flask==2.3.3
python -m pip install Flask-SQLAlchemy==3.0.5
python -m pip install Flask-Login==0.6.2
python -m pip install Werkzeug==2.3.7
python -m pip install SQLAlchemy==2.0.21
python -m pip install python-dotenv==1.0.0

echo.
echo Checking Flask is installed...
python -c "import flask; print(f'Flask version: {flask.__version__}')"

echo.
echo ================================================================================
echo SUCCESS: Flask is installed!
echo ================================================================================
echo.
pause
