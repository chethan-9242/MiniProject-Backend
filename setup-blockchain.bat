@echo off
setlocal enabledelayedexpansion

REM SwasthVedha Blockchain Setup Script for Windows
REM This script sets up the complete blockchain integration

echo 🔗 Setting up SwasthVedha Blockchain Integration...
echo ==================================================

REM Helper functions
:log_info
echo ℹ️  %~1
goto :eof

:log_success
echo ✅ %~1
goto :eof

:log_warning
echo ⚠️  %~1
goto :eof

:log_error
echo ❌ %~1
goto :eof

REM Check prerequisites
call :log_info "Checking prerequisites..."

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    call :log_error "Docker is not installed. Please install Docker Desktop first."
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    call :log_error "Node.js is not installed. Please install Node.js first."
    pause
    exit /b 1
)

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    call :log_error "Python is not installed. Please install Python first."
    pause
    exit /b 1
)

call :log_success "All prerequisites are installed!"

REM Setup blockchain contracts
call :log_info "Setting up blockchain contracts..."

cd blockchain

REM Install Node.js dependencies
call :log_info "Installing Node.js dependencies..."
call npm install
if errorlevel 1 (
    call :log_error "Failed to install Node.js dependencies."
    cd ..
    pause
    exit /b 1
)

REM Compile smart contracts
call :log_info "Compiling smart contracts..."
call npm run compile
if errorlevel 1 (
    call :log_error "Failed to compile smart contracts."
    cd ..
    pause
    exit /b 1
)

REM Start local blockchain node in background
call :log_info "Starting local blockchain node..."
start /B "Blockchain Node" cmd /c "npm run node > blockchain.log 2>&1"

REM Wait for blockchain to start
call :log_info "Waiting for blockchain node to start..."
timeout /t 10 /nobreak > nul

REM Deploy contracts
call :log_info "Deploying smart contracts..."
call npm run deploy:local
if errorlevel 1 (
    call :log_error "Failed to deploy smart contracts."
    cd ..
    pause
    exit /b 1
)

REM Check if deployment was successful
if exist "deployments\localhost.json" (
    call :log_success "Smart contracts deployed successfully!"
) else (
    call :log_error "Contract deployment failed!"
    cd ..
    pause
    exit /b 1
)

cd ..

REM Setup IPFS
call :log_info "Setting up IPFS..."

REM Check if IPFS is installed
ipfs --version >nul 2>&1
if errorlevel 1 (
    call :log_warning "IPFS is not installed. Using Docker IPFS instead."
) else (
    REM Initialize IPFS if not already initialized
    if not exist "%USERPROFILE%\.ipfs" (
        call ipfs init
    )
    
    REM Start IPFS daemon in background
    call :log_info "Starting IPFS daemon..."
    start /B "IPFS Daemon" cmd /c "ipfs daemon > ipfs.log 2>&1"
    
    REM Wait for IPFS to start
    call :log_info "Waiting for IPFS daemon to start..."
    timeout /t 5 /nobreak > nul
    
    call :log_success "IPFS daemon started!"
)

REM Setup backend
call :log_info "Setting up backend..."

cd backend

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    call :log_info "Creating Python virtual environment..."
    python -m venv venv
    if errorlevel 1 (
        call :log_error "Failed to create virtual environment."
        cd ..
        pause
        exit /b 1
    )
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install Python dependencies
call :log_info "Installing Python dependencies..."
pip install -r requirements.txt
if errorlevel 1 (
    call :log_error "Failed to install Python dependencies."
    cd ..
    pause
    exit /b 1
)

REM Create encryption keys directory
if not exist "encryption_keys" mkdir encryption_keys

REM Setup environment file
if not exist ".env" (
    call :log_info "Creating environment file..."
    copy .env.blockchain .env > nul
    call :log_success "Environment file created!"
)

cd ..
call :log_success "Backend setup completed!"

REM Setup frontend
call :log_info "Setting up frontend..."

cd frontend

REM Install Node.js dependencies
call :log_info "Installing frontend dependencies..."
call npm install
if errorlevel 1 (
    call :log_error "Failed to install frontend dependencies."
    cd ..
    pause
    exit /b 1
)

cd ..
call :log_success "Frontend setup completed!"

REM Start services with Docker
call :log_info "Starting Docker services..."

REM Build and start all services
docker-compose up --build -d
if errorlevel 1 (
    call :log_error "Failed to start Docker services."
    pause
    exit /b 1
)

REM Wait for services to start
call :log_info "Waiting for services to start..."
timeout /t 30 /nobreak > nul

REM Check service health
call :log_info "Checking service health..."

REM Check backend
curl -f http://localhost:8000/health >nul 2>&1
if errorlevel 1 (
    call :log_warning "Backend might still be starting..."
) else (
    call :log_success "Backend is healthy!"
)

REM Check blockchain health
curl -f http://localhost:8000/api/blockchain/health >nul 2>&1
if errorlevel 1 (
    call :log_warning "Blockchain integration might still be starting..."
) else (
    call :log_success "Blockchain integration is healthy!"
)

REM Check frontend
curl -f http://localhost:3000 >nul 2>&1
if errorlevel 1 (
    call :log_warning "Frontend might still be starting..."
) else (
    call :log_success "Frontend is running!"
)

REM Display setup summary
echo.
echo 🎉 SwasthVedha Blockchain Setup Complete!
echo ==========================================
echo.
echo 📊 Service URLs:
echo   • Frontend:           http://localhost:3000
echo   • Backend API:        http://localhost:8000
echo   • API Documentation:  http://localhost:8000/docs
echo   • Blockchain Health:  http://localhost:8000/api/blockchain/health
echo   • IPFS Gateway:       http://localhost:8080
echo   • Blockchain Node:    http://localhost:8545
echo.
echo 🔗 Blockchain Features:
echo   • Immutable Medical Records
echo   • IPFS Decentralized Storage
echo   • Patient Consent Management
echo   • Practitioner Verification
echo   • Medicine Authentication
echo.
echo 📝 Next Steps:
echo   1. Open http://localhost:3000 in your browser
echo   2. Navigate to 'Blockchain Status' to verify integration
echo   3. Use 'Medical Records' to view blockchain-stored data
echo   4. Try the AI modules to create blockchain records
echo.
echo 🔧 Management Commands:
echo   • View logs:          docker-compose logs -f
echo   • Stop services:      docker-compose down
echo   • Restart services:   docker-compose restart
echo   • View blockchain:    curl http://localhost:8545
echo   • View IPFS status:   ipfs repo stats
echo.
echo 📚 Documentation:
echo   • Setup Guide:        BLOCKCHAIN_SETUP_GUIDE.md
echo   • API Docs:           http://localhost:8000/docs
echo   • Smart Contracts:    blockchain\contracts\
echo.

call :log_success "Setup completed successfully! 🎉"
echo.
echo Press any key to open the application in your browser...
pause > nul
start http://localhost:3000

endlocal
