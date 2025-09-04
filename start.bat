@echo off
REM Smart ATS Startup Script for Windows

echo Starting Smart ATS Application...

REM Check if .env file exists
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo Please edit .env file with your API keys and configuration
    pause
    exit /b 1
)

REM Create necessary directories
if not exist logs mkdir logs
if not exist uploads mkdir uploads

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is required but not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM Check if pip is installed
pip --version >nul 2>&1
if errorlevel 1 (
    echo pip is required but not installed. Please install pip.
    pause
    exit /b 1
)

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install dependencies.
    pause
    exit /b 1
)

REM Start backend server
echo Starting backend server...
start "Backend Server" cmd /k "cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

REM Wait for backend to start
timeout /t 5 /nobreak

REM Start frontend server
echo Starting frontend server...
start "Frontend Server" cmd /k "cd frontend && python app.py"

echo Smart ATS is now running!
echo Frontend: http://localhost:5000
echo Backend API: http://localhost:8000
echo API Documentation: http://localhost:8000/api/docs
echo.
echo Close the command windows to stop the services
pause