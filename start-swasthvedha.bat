@echo off
echo ========================================
echo    Starting SwasthVedha Application
echo ========================================
echo.

echo Starting Backend Server...
start "SwasthVedha Backend" cmd /k "cd /d C:\Users\Chethan\OneDrive\Desktop\SwasthVedha\backend && py -m uvicorn main:app --reload --host 127.0.0.1 --port 8000"

echo Waiting for backend to start...
timeout /t 5 /nobreak > nul

echo Starting Frontend Server...
start "SwasthVedha Frontend" cmd /k "cd /d C:\Users\Chethan\OneDrive\Desktop\SwasthVedha\frontend && npm start"

echo.
echo ========================================
echo   SwasthVedha is starting up!
echo ========================================
echo.
echo Frontend will open at: http://localhost:3000
echo Backend API docs at:   http://localhost:8000/docs
echo.
echo Press any key to continue...
pause > nul