"""
Web3 Provider for SwasthVedha Blockchain Integration
Handles all blockchain interactions including smart contract calls and IPFS operations
"""

import os
import json
import hashlib
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from web3 import Web3
from web3.middleware import geth_poa_middleware
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Web3Provider:
    """Web3 provider for blockchain interactions"""
    
    def __init__(self):
        self.w3 = None
        self.medical_record_contract = None
        self.treatment_tracking_contract = None
        self.contract_address = None
        self.private_key = None
        self.account_address = None
        
        # Initialize blockchain connection
        self._initialize_web3()
        self._load_contracts()
    
    def _initialize_web3(self):
        """Initialize Web3 connection"""
        try:
            # Try different blockchain providers
            providers = [
                os.getenv("BLOCKCHAIN_RPC_URL", "http://localhost:8545"),
                "https://polygon-mumbai.g.alchemy.com/v2/demo",  # Mumbai testnet
                "https://rpc-mumbai.maticvigil.com",  # Mumbai testnet
            ]
            
            for provider_url in providers:
                try:
                    self.w3 = Web3(Web3.HTTPProvider(provider_url))
                    if self.w3.is_connected():
                        logger.info(f"✅ Connected to blockchain: {provider_url}")
                        break
                except Exception as e:
                    logger.warning(f"Failed to connect to {provider_url}: {e}")
                    continue
            
            if not self.w3 or not self.w3.is_connected():
                raise Exception("Could not connect to any blockchain provider")
            
            # Add middleware for PoA chains (like Polygon)
            if "polygon" in provider_url or "mumbai" in provider_url:
                self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
            
            # Load account credentials
            self.private_key = os.getenv("BLOCKCHAIN_PRIVATE_KEY")
            if self.private_key:
                self.account_address = self.w3.eth.account.from_key(self.private_key).address
                logger.info(f"🔑 Using account: {self.account_address}")
            else:
                logger.warning("⚠️ No private key provided. Read-only mode enabled.")
                
        except Exception as e:
            logger.error(f"❌ Failed to initialize Web3: {e}")
            raise
    
    def _load_contracts(self):
        """Load smart contract ABIs and addresses"""
        try:
            # Load deployment info
            deployment_file = Path("../blockchain/deployments/localhost.json")
            if not deployment_file.exists():
                # Try to find any deployment file
                deployments_dir = Path("../blockchain/deployments")
                if deployments_dir.exists():
                    for file in deployments_dir.glob("*.json"):
                        deployment_file = file
                        break
            
            if not deployment_file.exists():
                logger.warning("⚠️ No deployment file found. Using mock mode.")
                return
            
            with open(deployment_file, 'r') as f:
                deployment_info = json.load(f)
            
            self.contract_address = deployment_info['contracts']
            
            # Load contract ABIs
            medical_record_abi_path = Path("../blockchain/artifacts/MedicalRecord.json")
            treatment_tracking_abi_path = Path("../blockchain/artifacts/TreatmentTracking.json")
            
            if medical_record_abi_path.exists():
                with open(medical_record_abi_path, 'r') as f:
                    medical_record_abi = json.load(f)['abi']
                    self.medical_record_contract = self.w3.eth.contract(
                        address=deployment_info['contracts']['MedicalRecord'],
                        abi=medical_record_abi
                    )
                    logger.info("✅ MedicalRecord contract loaded")
            
            if treatment_tracking_abi_path.exists():
                with open(treatment_tracking_abi_path, 'r') as f:
                    treatment_tracking_abi = json.load(f)['abi']
                    self.treatment_tracking_contract = self.w3.eth.contract(
                        address=deployment_info['contracts']['TreatmentTracking'],
                        abi=treatment_tracking_abi
                    )
                    logger.info("✅ TreatmentTracking contract loaded")
                    
        except Exception as e:
            logger.error(f"❌ Failed to load contracts: {e}")
    
    def _hash_patient_id(self, patient_id: str) -> str:
        """Hash patient ID for privacy"""
        return hashlib.sha256(patient_id.encode()).hexdigest()
    
    def _send_transaction(self, contract_function, *args) -> Dict[str, Any]:
        """Send transaction to blockchain"""
        if not self.private_key:
            raise Exception("Private key required for transactions")
        
        try:
            # Build transaction
            transaction = contract_function(*args).build_transaction({
                'from': self.account_address,
                'gas': 2000000,
                'gasPrice': self.w3.eth.gas_price,
                'nonce': self.w3.eth.get_transaction_count(self.account_address),
            })
            
            # Sign transaction
            signed_txn = self.w3.eth.account.sign_transaction(transaction, self.private_key)
            
            # Send transaction
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            # Wait for receipt
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            logger.info(f"✅ Transaction confirmed: {tx_hash.hex()}")
            return {
                'success': True,
                'transaction_hash': tx_hash.hex(),
                'block_number': tx_receipt.blockNumber,
                'gas_used': tx_receipt.gasUsed,
            }
            
        except Exception as e:
            logger.error(f"❌ Transaction failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def create_medical_record(
        self, 
        patient_id: str, 
        record_hash: str, 
        record_type: str,
        practitioner_address: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new medical record on blockchain"""
        try:
            if not self.medical_record_contract:
                return {'success': False, 'error': 'MedicalRecord contract not loaded'}
            
            hashed_patient_id = self._hash_patient_id(patient_id)
            
            result = self._send_transaction(
                self.medical_record_contract.functions.createMedicalRecord,
                hashed_patient_id,
                record_hash,
                record_type,
                practitioner_address or self.account_address
            )
            
            if result['success']:
                logger.info(f"📋 Medical record created for patient {patient_id}")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Failed to create medical record: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_patient_records(self, patient_id: str, requester_address: str) -> List[Dict]:
        """Get patient records from blockchain"""
        try:
            if not self.medical_record_contract:
                return []
            
            hashed_patient_id = self._hash_patient_id(patient_id)
            record_ids = self.medical_record_contract.functions.getPatientRecords(
                hashed_patient_id, 
                requester_address
            ).call()
            
            records = []
            for record_id in record_ids:
                record = self.medical_record_contract.functions.getRecord(
                    record_id, 
                    requester_address
                ).call()
                records.append({
                    'record_id': record_id,
                    'patient_id': record[0],
                    'record_hash': record[1],
                    'record_type': record[2],
                    'timestamp': record[3],
                    'is_valid': record[4],
                    'practitioner': record[5],
                })
            
            logger.info(f"📋 Retrieved {len(records)} records for patient {patient_id}")
            return records
            
        except Exception as e:
            logger.error(f"❌ Failed to get patient records: {e}")
            return []
    
    def verify_practitioner(
        self, 
        practitioner_address: str, 
        license_hash: str, 
        specialization: str
    ) -> Dict[str, Any]:
        """Verify a practitioner on blockchain"""
        try:
            if not self.medical_record_contract:
                return {'success': False, 'error': 'MedicalRecord contract not loaded'}
            
            result = self._send_transaction(
                self.medical_record_contract.functions.verifyPractitioner,
                practitioner_address,
                license_hash,
                specialization
            )
            
            if result['success']:
                logger.info(f"👨‍⚕️ Practitioner verified: {practitioner_address}")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Failed to verify practitioner: {e}")
            return {'success': False, 'error': str(e)}
    
    def start_treatment(
        self,
        patient_id: str,
        condition_hash: str,
        treatment_hash: str,
        medicine_hashes: List[str],
        end_date_timestamp: int
    ) -> Dict[str, Any]:
        """Start a new treatment protocol"""
        try:
            if not self.treatment_tracking_contract:
                return {'success': False, 'error': 'TreatmentTracking contract not loaded'}
            
            hashed_patient_id = self._hash_patient_id(patient_id)
            
            result = self._send_transaction(
                self.treatment_tracking_contract.functions.startTreatment,
                hashed_patient_id,
                condition_hash,
                treatment_hash,
                medicine_hashes,
                end_date_timestamp
            )
            
            if result['success']:
                logger.info(f"💊 Treatment started for patient {patient_id}")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Failed to start treatment: {e}")
            return {'success': False, 'error': str(e)}
    
    def authenticate_medicine(
        self,
        medicine_hash: str,
        manufacturer: str,
        batch_number: str,
        manufacture_date: int,
        expiry_date: int,
        test_results: List[str]
    ) -> Dict[str, Any]:
        """Authenticate a medicine batch"""
        try:
            if not self.treatment_tracking_contract:
                return {'success': False, 'error': 'TreatmentTracking contract not loaded'}
            
            result = self._send_transaction(
                self.treatment_tracking_contract.functions.authenticateMedicine,
                medicine_hash,
                manufacturer,
                batch_number,
                manufacture_date,
                expiry_date,
                test_results
            )
            
            if result['success']:
                logger.info(f"🌿 Medicine authenticated: {medicine_hash}")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Failed to authenticate medicine: {e}")
            return {'success': False, 'error': str(e)}
    
    def report_treatment_outcome(
        self,
        treatment_id: int,
        outcome_hash: str,
        patient_satisfaction: int,
        symptom_improvement: int,
        feedback_hash: str
    ) -> Dict[str, Any]:
        """Report treatment outcome"""
        try:
            if not self.treatment_tracking_contract:
                return {'success': False, 'error': 'TreatmentTracking contract not loaded'}
            
            result = self._send_transaction(
                self.treatment_tracking_contract.functions.reportOutcome,
                treatment_id,
                outcome_hash,
                patient_satisfaction,
                symptom_improvement,
                feedback_hash
            )
            
            if result['success']:
                logger.info(f"📊 Treatment outcome reported for treatment {treatment_id}")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Failed to report treatment outcome: {e}")
            return {'success': False, 'error': str(e)}
    
    def is_practitioner_verified(self, practitioner_address: str) -> bool:
        """Check if practitioner is verified"""
        try:
            if not self.medical_record_contract:
                return False
            
            return self.medical_record_contract.functions.isPractitionerVerified(
                practitioner_address
            ).call()
            
        except Exception as e:
            logger.error(f"❌ Failed to check practitioner verification: {e}")
            return False
    
    def get_blockchain_status(self) -> Dict[str, Any]:
        """Get blockchain connection status"""
        try:
            if not self.w3 or not self.w3.is_connected():
                return {
                    'connected': False,
                    'error': 'Not connected to blockchain'
                }
            
            latest_block = self.w3.eth.get_block('latest')
            
            return {
                'connected': True,
                'block_number': latest_block.number,
                'gas_price': self.w3.eth.gas_price,
                'chain_id': self.w3.eth.chain_id,
                'account_address': self.account_address,
                'contracts_loaded': {
                    'MedicalRecord': self.medical_record_contract is not None,
                    'TreatmentTracking': self.treatment_tracking_contract is not None
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to get blockchain status: {e}")
            return {'connected': False, 'error': str(e)}

# Global instance
web3_provider = Web3Provider()
