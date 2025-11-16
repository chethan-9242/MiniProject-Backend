# 🔗 Blockchain Integration Setup Guide

## 📋 Overview

SwasthVedha now includes comprehensive blockchain integration for:
- **Immutable Medical Records** - All diagnoses and treatments stored on blockchain
- **IPFS Storage** - Decentralized storage for medical images and large data
- **Patient Consent Management** - Blockchain-based consent tracking
- **Practitioner Verification** - Verified Ayurvedic practitioners
- **Medicine Authentication** - Track medicine authenticity from manufacturer to patient

---

## 🚀 Quick Start (Docker)

### Prerequisites
- Docker Desktop installed and running
- Git (for cloning blockchain contracts)

### Step 1: Initialize Blockchain Contracts
```bash
# Navigate to blockchain directory
cd blockchain

# Install dependencies
npm install

# Compile smart contracts
npm run compile

# Start local blockchain node
npm run node
```

### Step 2: Deploy Contracts
Open a new terminal and run:
```bash
# Deploy contracts to local network
npm run deploy:local
```

### Step 3: Start Full Platform
```bash
# Navigate to project root
cd ..

# Start all services with blockchain
docker-compose up --build
```

### Step 4: Verify Integration
- **Backend API**: http://localhost:8000
- **Blockchain Health**: http://localhost:8000/api/blockchain/health
- **Frontend**: http://localhost:3000
- **IPFS Gateway**: http://localhost:8080
- **Blockchain Node**: http://localhost:8545

---

## 🛠️ Manual Setup

### 1. Install Node.js Dependencies
```bash
cd blockchain
npm install
```

### 2. Install Python Dependencies
```bash
cd ../backend
pip install -r requirements.txt
```

### 3. Start IPFS
```bash
# Install IPFS (if not already installed)
# Download from: https://ipfs.io/install/

# Initialize IPFS repository
ipfs init

# Start IPFS daemon
ipfs daemon
```

### 4. Start Blockchain Node
```bash
cd ../blockchain

# Start Hardhat local network
npx hardhat node
```

### 5. Deploy Smart Contracts
```bash
# Deploy to local network
npx hardhat run scripts/deploy.js --network localhost
```

### 6. Configure Environment
```bash
# Copy blockchain environment template
cd ../backend
cp .env.blockchain .env

# Edit .env with your configuration
nano .env
```

### 7. Start Backend
```bash
# Start backend with blockchain integration
python main.py
```

---

## 🔧 Configuration

### Environment Variables (.env)

```bash
# Blockchain Configuration
BLOCKCHAIN_RPC_URL=http://localhost:8545
BLOCKCHAIN_PRIVATE_KEY=your_private_key_here
BLOCKCHAIN_CHAIN_ID=31337

# IPFS Configuration
IPFS_API_URL=http://localhost:5001
IPFS_GATEWAY_URL=http://localhost:8080

# Contract Addresses (after deployment)
MEDICAL_RECORD_CONTRACT_ADDRESS=0x...
TREATMENT_TRACKING_CONTRACT_ADDRESS=0x...
```

### Getting Test ETH
For local testing, the Hardhat node provides test ETH automatically.

For testnet deployment:
```bash
# Get test ETH from Mumbai faucet
# Visit: https://faucet.polygon.technology/
```

---

## 📊 Smart Contracts

### MedicalRecord.sol
- **Purpose**: Store medical record metadata and access controls
- **Key Functions**:
  - `createMedicalRecord()` - Create new medical record
  - `getPatientRecords()` - Retrieve patient records (with consent)
  - `verifyPractitioner()` - Verify practitioner credentials
  - `grantConsent()` - Grant data access consent

### TreatmentTracking.sol
- **Purpose**: Track treatment protocols and outcomes
- **Key Functions**:
  - `startTreatment()` - Begin new treatment protocol
  - `authenticateMedicine()` - Verify medicine authenticity
  - `reportOutcome()` - Report treatment effectiveness
  - `completeTreatment()` - Mark treatment as completed

---

## 🌐 API Endpoints

### Medical Records
```bash
# Create medical record
POST /api/blockchain/medical-record
{
  "patient_id": "patient_123",
  "record_type": "symptom_analysis",
  "analysis_data": {...},
  "practitioner_address": "0x..."
}

# Get patient records
GET /api/blockchain/medical-records/{patient_id}?requester_address=0x...
```

### Treatment Protocols
```bash
# Start treatment
POST /api/blockchain/treatment-protocol
{
  "patient_id": "patient_123",
  "condition": "Tension Headache",
  "treatment_data": {...},
  "medicines": [...],
  "duration_days": 30
}

# Report outcome
POST /api/blockchain/treatment-outcome
{
  "treatment_id": 1,
  "outcome_data": {...},
  "patient_satisfaction": 200,
  "symptom_improvement": 180,
  "patient_feedback": "Treatment was effective"
}
```

### Medicine Authentication
```bash
# Authenticate medicine
POST /api/blockchain/medicine-authentication
{
  "medicine_data": {...},
  "manufacturer": "Ayurvedic Pharma Ltd",
  "batch_number": "ASH2024001",
  "manufacture_date": "2024-01-15",
  "expiry_date": "2026-01-15",
  "test_results": ["QC-ASH-001", "QC-ASH-002"]
}
```

### System Health
```bash
# Check blockchain integration health
GET /api/blockchain/health

# Get system statistics
GET /api/blockchain/stats
```

---

## 🔐 Security Features

### Data Encryption
- **Patient Data**: Encrypted before IPFS upload
- **Encryption Keys**: Stored securely in local encryption_keys directory
- **Hashed IDs**: Patient IDs hashed for privacy on blockchain

### Access Control
- **Role-Based Access**: Practitioners, patients, and systems have different permissions
- **Consent Management**: Patients must grant explicit consent for data access
- **Smart Contract Permissions**: Built-in access control in smart contracts

### Immutable Records
- **Tamper-Proof**: All medical records stored immutably on blockchain
- **Audit Trail**: Complete history of all medical interactions
- **Timestamp**: Every record includes blockchain timestamp

---

## 📱 Frontend Integration

### React Components
```typescript
// Blockchain service for frontend
import { BlockchainService } from '../services/blockchain';

// Create medical record
const result = await BlockchainService.createMedicalRecord({
  patientId: 'patient_123',
  recordType: 'symptom_analysis',
  analysisData: symptomAnalysis
});

// Get patient records
const records = await BlockchainService.getPatientRecords(
  'patient_123', 
  userAddress
);
```

### Web3 Integration
```typescript
// Connect user wallet
const connectWallet = async () => {
  if (window.ethereum) {
    const accounts = await window.ethereum.request({
      method: 'eth_requestAccounts'
    });
    return accounts[0];
  }
};

// Sign transactions with user wallet
const signTransaction = async (transactionData) => {
  const signature = await window.ethereum.request({
    method: 'eth_signTypedData_v4',
    params: [account, transactionData]
  });
  return signature;
};
```

---

## 🧪 Testing

### Run Blockchain Tests
```bash
cd blockchain

# Run all tests
npm test

# Run specific test file
npx hardhat test test/MedicalRecord.test.js

# Run tests with gas reporting
REPORT_GAS=true npm test
```

### Test API Endpoints
```bash
# Test blockchain health
curl http://localhost:8000/api/blockchain/health

# Test medical record creation
curl -X POST http://localhost:8000/api/blockchain/medical-record \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": "test_patient",
    "record_type": "symptom_analysis",
    "analysis_data": {"symptoms": ["headache"]},
    "practitioner_address": "0x..."
  }'
```

---

## 🚀 Deployment

### Testnet Deployment (Polygon Mumbai)
```bash
# Configure testnet in .env
BLOCKCHAIN_RPC_URL=https://polygon-mumbai.g.alchemy.com/v2/your_api_key
BLOCKCHAIN_CHAIN_ID=80001

# Deploy to testnet
npm run deploy:mumbai

# Verify contracts
npm run verify --network polygon_mumbai
```

### Mainnet Deployment
```bash
# Configure mainnet in .env
BLOCKCHAIN_RPC_URL=https://mainnet.infura.io/v3/your_project_id
BLOCKCHAIN_CHAIN_ID=1

# Deploy to mainnet
npx hardhat run scripts/deploy.js --network mainnet

# Verify contracts
npx hardhat verify --network mainnet <contract-address>
```

---

## 📈 Monitoring

### Blockchain Metrics
- **Transaction Count**: Total medical records created
- **Gas Usage**: Average gas cost per transaction
- **Block Time**: Network performance metrics
- **Contract Activity**: Usage statistics for each contract

### IPFS Metrics
- **Storage Used**: Total IPFS storage consumption
- **Pinned Files**: Number of pinned medical records
- **Network Peers**: IPFS network connectivity
- **Gateway Requests**: API gateway usage

### Monitoring Tools
```bash
# Check blockchain status
curl http://localhost:8000/api/blockchain/stats

# Monitor IPFS
ipfs repo stats

# View blockchain logs
docker-compose logs -f blockchain-node
```

---

## 🔍 Troubleshooting

### Common Issues

#### "Blockchain connection failed"
**Solution**: Ensure blockchain node is running
```bash
# Check if Hardhat node is running
curl http://localhost:8545

# Restart blockchain node
docker-compose restart blockchain-node
```

#### "IPFS connection failed"
**Solution**: Check IPFS daemon status
```bash
# Check IPFS status
ipfs id

# Restart IPFS
docker-compose restart ipfs
```

#### "Transaction failed: Insufficient funds"
**Solution**: Ensure account has test ETH
```bash
# Check account balance
curl -X POST http://localhost:8545 \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "eth_getBalance",
    "params": ["0x...", "latest"],
    "id": 1
  }'
```

#### "Contract not found"
**Solution**: Deploy contracts and update addresses
```bash
# Redeploy contracts
npm run deploy:local

# Update .env with new addresses
```

### Debug Mode
Enable debug logging:
```bash
# Set debug mode in .env
DEBUG_MODE=true

# View detailed logs
docker-compose logs -f backend
```

---

## 📚 Documentation

- **Smart Contract Documentation**: `blockchain/contracts/README.md`
- **API Documentation**: http://localhost:8000/docs
- **IPFS Documentation**: https://docs.ipfs.io/
- **Hardhat Documentation**: https://hardhat.org/docs

---

## 🆘 Support

### Getting Help
1. **Check Logs**: `docker-compose logs backend`
2. **Health Check**: http://localhost:8000/api/blockchain/health
3. **Documentation**: Read this guide thoroughly
4. **Community**: Open an issue on GitHub

### Emergency Recovery
```bash
# Reset blockchain data
docker-compose down -v
docker volume rm swasthvedha_blockchain_data
docker-compose up --build

# Reset IPFS data
docker volume rm swasthvedha_ipfs_data
```

---

## 🎉 Success!

Your SwasthVedha platform now has full blockchain integration! 

**What you now have:**
- ✅ Immutable medical records
- ✅ Decentralized IPFS storage
- ✅ Patient consent management
- ✅ Practitioner verification
- ✅ Medicine authentication
- ✅ Complete audit trail

**Next Steps:**
1. Test all blockchain endpoints
2. Deploy to testnet for staging
3. Plan mainnet deployment
4. Train healthcare providers

Welcome to the future of Ayurvedic healthcare on blockchain! 🚀
