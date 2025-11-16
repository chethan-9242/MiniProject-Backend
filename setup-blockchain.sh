#!/bin/bash

# SwasthVedha Blockchain Setup Script
# This script sets up the complete blockchain integration

set -e

echo "🔗 Setting up SwasthVedha Blockchain Integration..."
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check if Docker is installed
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    # Check if Docker Compose is installed
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    # Check if Node.js is installed
    if ! command -v node &> /dev/null; then
        log_error "Node.js is not installed. Please install Node.js first."
        exit 1
    fi
    
    # Check if Python is installed
    if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
        log_error "Python is not installed. Please install Python first."
        exit 1
    fi
    
    log_success "All prerequisites are installed!"
}

# Setup blockchain contracts
setup_blockchain_contracts() {
    log_info "Setting up blockchain contracts..."
    
    cd blockchain
    
    # Install Node.js dependencies
    log_info "Installing Node.js dependencies..."
    npm install
    
    # Compile smart contracts
    log_info "Compiling smart contracts..."
    npm run compile
    
    # Start local blockchain node in background
    log_info "Starting local blockchain node..."
    npm run node > blockchain.log 2>&1 &
    BLOCKCHAIN_PID=$!
    
    # Wait for blockchain to start
    log_info "Waiting for blockchain node to start..."
    sleep 10
    
    # Deploy contracts
    log_info "Deploying smart contracts..."
    npm run deploy:local
    
    # Save deployment info
    if [ -f "deployments/localhost.json" ]; then
        log_success "Smart contracts deployed successfully!"
        
        # Extract contract addresses
        MEDICAL_RECORD_ADDRESS=$(cat deployments/localhost.json | jq -r '.contracts.MedicalRecord')
        TREATMENT_TRACKING_ADDRESS=$(cat deployments/localhost.json | jq -r '.contracts.TreatmentTracking')
        
        log_info "MedicalRecord contract: $MEDICAL_RECORD_ADDRESS"
        log_info "TreatmentTracking contract: $TREATMENT_TRACKING_ADDRESS"
    else
        log_error "Contract deployment failed!"
        kill $BLOCKCHAIN_PID 2>/dev/null || true
        exit 1
    fi
    
    cd ..
}

# Setup IPFS
setup_ipfs() {
    log_info "Setting up IPFS..."
    
    # Check if IPFS is already running
    if ! pgrep -f "ipfs daemon" > /dev/null; then
        log_info "Starting IPFS daemon..."
        
        # Initialize IPFS if not already initialized
        if [ ! -d "$HOME/.ipfs" ]; then
            ipfs init
        fi
        
        # Start IPFS daemon in background
        ipfs daemon > ipfs.log 2>&1 &
        IPFS_PID=$!
        
        # Wait for IPFS to start
        log_info "Waiting for IPFS daemon to start..."
        sleep 5
        
        # Test IPFS connection
        if ipfs id > /dev/null 2>&1; then
            log_success "IPFS daemon started successfully!"
        else
            log_error "Failed to start IPFS daemon!"
            kill $IPFS_PID 2>/dev/null || true
            exit 1
        fi
    else
        log_success "IPFS daemon is already running!"
    fi
}

# Setup backend
setup_backend() {
    log_info "Setting up backend..."
    
    cd backend
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        log_info "Creating Python virtual environment..."
        python -m venv venv
    fi
    
    # Activate virtual environment
    if [ -f "venv/Scripts/activate" ]; then
        # Windows
        source venv/Scripts/activate
    else
        # Unix
        source venv/bin/activate
    fi
    
    # Install Python dependencies
    log_info "Installing Python dependencies..."
    pip install -r requirements.txt
    
    # Create encryption keys directory
    mkdir -p encryption_keys
    
    # Setup environment file
    if [ ! -f ".env" ]; then
        log_info "Creating environment file..."
        cp .env.blockchain .env
        
        # Update with actual contract addresses
        if [ -f "../blockchain/deployments/localhost.json" ]; then
            MEDICAL_RECORD_ADDRESS=$(cat ../blockchain/deployments/localhost.json | jq -r '.contracts.MedicalRecord')
            TREATMENT_TRACKING_ADDRESS=$(cat ../blockchain/deployments/localhost.json | jq -r '.contracts.TreatmentTracking')
            
            sed -i "s/MEDICAL_RECORD_CONTRACT_ADDRESS=/MEDICAL_RECORD_CONTRACT_ADDRESS=$MEDICAL_RECORD_ADDRESS/" .env
            sed -i "s/TREATMENT_TRACKING_CONTRACT_ADDRESS=/TREATMENT_TRACKING_CONTRACT_ADDRESS=$TREATMENT_TRACKING_ADDRESS/" .env
        fi
    fi
    
    cd ..
    log_success "Backend setup completed!"
}

# Setup frontend
setup_frontend() {
    log_info "Setting up frontend..."
    
    cd frontend
    
    # Install Node.js dependencies
    log_info "Installing frontend dependencies..."
    npm install
    
    cd ..
    log_success "Frontend setup completed!"
}

# Start services with Docker
start_docker_services() {
    log_info "Starting Docker services..."
    
    # Build and start all services
    docker-compose up --build -d
    
    # Wait for services to start
    log_info "Waiting for services to start..."
    sleep 30
    
    # Check service health
    log_info "Checking service health..."
    
    # Check backend
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        log_success "Backend is healthy!"
    else
        log_warning "Backend might still be starting..."
    fi
    
    # Check blockchain health
    if curl -f http://localhost:8000/api/blockchain/health > /dev/null 2>&1; then
        log_success "Blockchain integration is healthy!"
    else
        log_warning "Blockchain integration might still be starting..."
    fi
    
    # Check frontend
    if curl -f http://localhost:3000 > /dev/null 2>&1; then
        log_success "Frontend is running!"
    else
        log_warning "Frontend might still be starting..."
    fi
}

# Display setup summary
display_summary() {
    echo ""
    echo "🎉 SwasthVedha Blockchain Setup Complete!"
    echo "=========================================="
    echo ""
    echo "📊 Service URLs:"
    echo "  • Frontend:           http://localhost:3000"
    echo "  • Backend API:        http://localhost:8000"
    echo "  • API Documentation:  http://localhost:8000/docs"
    echo "  • Blockchain Health:  http://localhost:8000/api/blockchain/health"
    echo "  • IPFS Gateway:       http://localhost:8080"
    echo "  • Blockchain Node:    http://localhost:8545"
    echo ""
    echo "🔗 Blockchain Features:"
    echo "  • Immutable Medical Records"
    echo "  • IPFS Decentralized Storage"
    echo "  • Patient Consent Management"
    echo "  • Practitioner Verification"
    echo "  • Medicine Authentication"
    echo ""
    echo "📝 Next Steps:"
    echo "  1. Open http://localhost:3000 in your browser"
    echo "  2. Navigate to 'Blockchain Status' to verify integration"
    echo "  3. Use 'Medical Records' to view blockchain-stored data"
    echo "  4. Try the AI modules to create blockchain records"
    echo ""
    echo "🔧 Management Commands:"
    echo "  • View logs:          docker-compose logs -f"
    echo "  • Stop services:      docker-compose down"
    echo "  • Restart services:   docker-compose restart"
    echo "  • View blockchain:    curl http://localhost:8545"
    echo "  • View IPFS status:   ipfs repo stats"
    echo ""
    echo "📚 Documentation:"
    echo "  • Setup Guide:        BLOCKCHAIN_SETUP_GUIDE.md"
    echo "  • API Docs:           http://localhost:8000/docs"
    echo "  • Smart Contracts:    blockchain/contracts/"
    echo ""
}

# Cleanup function
cleanup() {
    log_info "Cleaning up..."
    
    # Kill background processes
    if [ ! -z "$BLOCKCHAIN_PID" ]; then
        kill $BLOCKCHAIN_PID 2>/dev/null || true
    fi
    
    if [ ! -z "$IPFS_PID" ]; then
        kill $IPFS_PID 2>/dev/null || true
    fi
}

# Set up cleanup on script exit
trap cleanup EXIT

# Main execution
main() {
    echo "Starting SwasthVedha Blockchain Setup..."
    echo ""
    
    check_prerequisites
    setup_blockchain_contracts
    setup_ipfs
    setup_backend
    setup_frontend
    start_docker_services
    display_summary
    
    log_success "Setup completed successfully! 🎉"
}

# Run main function
main "$@"
