@echo off
echo ========================================================
echo Cyber Attack Prediction System - Auto Setup
echo ========================================================

echo.
echo Checking for existing virtual environment...
IF NOT EXIST "env\" (
    echo [1/3] Virtual environment not found. Creating a fresh 'env'...
    python -m venv env
) ELSE (
    echo [1/3] Virtual environment 'env' already exists. Skipping creation.
)

echo.
echo [2/3] Activating virtual environment and installing dependencies...
call env\Scripts\activate.bat

echo Upgrading pip just in case...
python -m pip install --upgrade pip >nul 2>&1

echo Installing packages from requirements.txt...
pip install -r requirements.txt

echo.
echo [3/3] Starting Django Application Server!
echo.
echo Once the server boots, your browser should open automatically...
echo (If it doesn't open, manually go to http://127.0.0.1:8000)
echo.

start http://127.0.0.1:8000
python manage.py runserver

pause
