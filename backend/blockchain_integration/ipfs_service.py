"""
IPFS Service for SwasthVedha Blockchain Integration
Handles IPFS operations for storing and retrieving medical data
"""

import os
import json
import hashlib
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path
import logging
from cryptography.fernet import Fernet
import base64

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IPFSService:
    """IPFS service for decentralized storage"""
    
    def __init__(self):
        self.ipfs_api_url = os.getenv("IPFS_API_URL", "http://localhost:5001")
        self.ipfs_gateway_url = os.getenv("IPFS_GATEWAY_URL", "http://localhost:8080")
        self.encryption_keys_dir = Path("./encryption_keys")
        self.encryption_keys_dir.mkdir(exist_ok=True)
        
        # Test IPFS connection
        self._test_connection()
    
    def _test_connection(self):
        """Test IPFS connection"""
        try:
            response = requests.get(f"{self.ipfs_api_url}/api/v0/version")
            if response.status_code == 200:
                version = response.json().get("Version", "unknown")
                logger.info(f"✅ Connected to IPFS: {version}")
            else:
                logger.warning("⚠️ IPFS connection failed")
        except Exception as e:
            logger.warning(f"⚠️ Could not connect to IPFS: {e}")
    
    def _generate_encryption_key(self) -> bytes:
        """Generate encryption key"""
        return Fernet.generate_key()
    
    def _encrypt_data(self, data: Dict[str, Any], key: bytes) -> str:
        """Encrypt data using Fernet symmetric encryption"""
        f = Fernet(key)
        json_data = json.dumps(data, default=str).encode()
        encrypted_data = f.encrypt(json_data)
        return base64.b64encode(encrypted_data).decode()
    
    def _decrypt_data(self, encrypted_data: str, key: bytes) -> Dict[str, Any]:
        """Decrypt data using Fernet symmetric encryption"""
        f = Fernet(key)
        encrypted_bytes = base64.b64decode(encrypted_data.encode())
        decrypted_data = f.decrypt(encrypted_bytes)
        return json.loads(decrypted_data.decode())
    
    def _hash_patient_id(self, patient_id: str) -> str:
        """Hash patient ID for privacy"""
        return hashlib.sha256(patient_id.encode()).hexdigest()
    
    def _save_encryption_key(self, ipfs_hash: str, key: bytes, patient_id: str):
        """Save encryption key securely"""
        key_data = {
            "ipfs_hash": ipfs_hash,
            "encryption_key": base64.b64encode(key).decode(),
            "patient_id": self._hash_patient_id(patient_id),
            "created_at": datetime.now().isoformat()
        }
        
        key_file = self.encryption_keys_dir / f"{ipfs_hash}.json"
        with open(key_file, 'w') as f:
            json.dump(key_data, f, indent=2)
        
        logger.info(f"🔐 Encryption key saved for hash: {ipfs_hash}")
    
    def _get_encryption_key(self, ipfs_hash: str) -> Optional[bytes]:
        """Retrieve encryption key"""
        key_file = self.encryption_keys_dir / f"{ipfs_hash}.json"
        if key_file.exists():
            with open(key_file, 'r') as f:
                key_data = json.load(f)
                return base64.b64decode(key_data["encryption_key"].encode())
        return None
    
    def upload_medical_record(self, data: Dict[str, Any], patient_id: str) -> Dict[str, Any]:
        """Upload medical record to IPFS"""
        try:
            logger.info(f"📤 Uploading medical record for patient: {patient_id}")
            
            # Generate encryption key
            encryption_key = self._generate_encryption_key()
            
            # Create IPFS data structure
            ipfs_data = {
                "patient_id": self._hash_patient_id(patient_id),
                "encrypted_data": self._encrypt_data(data, encryption_key),
                "timestamp": datetime.now().isoformat(),
                "data_type": "medical_record",
                "version": "1.0",
                "metadata": {
                    "original_patient_id": patient_id[:8] + "...",  # Partial ID for identification
                    "record_type": data.get("analysis_type", "unknown"),
                    "confidence": data.get("confidence", 0)
                }
            }
            
            # Upload to IPFS
            files = {'file': json.dumps(ipfs_data)}
            response = requests.post(f"{self.ipfs_api_url}/api/v0/add", files=files)
            
            if response.status_code != 200:
                raise Exception(f"IPFS upload failed: {response.text}")
            
            result = response.json()
            ipfs_hash = result["Hash"]
            
            # Save encryption key
            self._save_encryption_key(ipfs_hash, encryption_key, patient_id)
            
            logger.info(f"✅ Medical record uploaded to IPFS: {ipfs_hash}")
            
            return {
                "ipfs_hash": ipfs_hash,
                "success": True,
                "timestamp": ipfs_data["timestamp"],
                "gateway_url": f"{self.ipfs_gateway_url}/ipfs/{ipfs_hash}"
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to upload medical record: {e}")
            return {"success": False, "error": str(e)}
    
    def upload_treatment_protocol(self, data: Dict[str, Any], practitioner_id: str) -> Dict[str, Any]:
        """Upload treatment protocol to IPFS"""
        try:
            logger.info(f"📤 Uploading treatment protocol from practitioner: {practitioner_id}")
            
            ipfs_data = {
                "practitioner_id": self._hash_patient_id(practitioner_id),
                "treatment_data": data,
                "timestamp": datetime.now().isoformat(),
                "data_type": "treatment_protocol",
                "version": "1.0",
                "metadata": {
                    "condition": data.get("condition", "unknown"),
                    "duration": data.get("duration", "unknown"),
                    "medicines_count": len(data.get("medicines", []))
                }
            }
            
            # Upload to IPFS
            files = {'file': json.dumps(ipfs_data)}
            response = requests.post(f"{self.ipfs_api_url}/api/v0/add", files=files)
            
            if response.status_code != 200:
                raise Exception(f"IPFS upload failed: {response.text}")
            
            result = response.json()
            ipfs_hash = result["Hash"]
            
            logger.info(f"✅ Treatment protocol uploaded to IPFS: {ipfs_hash}")
            
            return {
                "ipfs_hash": ipfs_hash,
                "success": True,
                "timestamp": ipfs_data["timestamp"],
                "gateway_url": f"{self.ipfs_gateway_url}/ipfs/{ipfs_hash}"
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to upload treatment protocol: {e}")
            return {"success": False, "error": str(e)}
    
    def upload_medicine_info(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Upload medicine information to IPFS"""
        try:
            logger.info(f"📤 Uploading medicine information: {data.get('name', 'unknown')}")
            
            ipfs_data = {
                "medicine_data": data,
                "timestamp": datetime.now().isoformat(),
                "data_type": "medicine_info",
                "version": "1.0",
                "metadata": {
                    "name": data.get("name", "unknown"),
                    "manufacturer": data.get("manufacturer", "unknown"),
                    "batch_number": data.get("batchNumber", "unknown")
                }
            }
            
            # Upload to IPFS
            files = {'file': json.dumps(ipfs_data)}
            response = requests.post(f"{self.ipfs_api_url}/api/v0/add", files=files)
            
            if response.status_code != 200:
                raise Exception(f"IPFS upload failed: {response.text}")
            
            result = response.json()
            ipfs_hash = result["Hash"]
            
            logger.info(f"✅ Medicine information uploaded to IPFS: {ipfs_hash}")
            
            return {
                "ipfs_hash": ipfs_hash,
                "success": True,
                "timestamp": ipfs_data["timestamp"],
                "gateway_url": f"{self.ipfs_gateway_url}/ipfs/{ipfs_hash}"
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to upload medicine information: {e}")
            return {"success": False, "error": str(e)}
    
    def retrieve_from_ipfs(self, ipfs_hash: str, decrypt: bool = True) -> Dict[str, Any]:
        """Retrieve data from IPFS"""
        try:
            logger.info(f"📥 Retrieving data from IPFS: {ipfs_hash}")
            
            # Get data from IPFS
            response = requests.post(f"{self.ipfs_api_url}/api/v0/cat", params={"arg": ipfs_hash})
            
            if response.status_code != 200:
                raise Exception(f"IPFS retrieval failed: {response.text}")
            
            ipfs_data = json.loads(response.text)
            
            # Decrypt if requested and encrypted
            if decrypt and "encrypted_data" in ipfs_data:
                encryption_key = self._get_encryption_key(ipfs_hash)
                if encryption_key:
                    decrypted_data = self._decrypt_data(ipfs_data["encrypted_data"], encryption_key)
                    return {
                        "success": True,
                        "data": decrypted_data,
                        "metadata": ipfs_data.get("metadata", {}),
                        "timestamp": ipfs_data.get("timestamp"),
                        "decrypted": True
                    }
                else:
                    logger.warning(f"⚠️ No encryption key found for hash: {ipfs_hash}")
                    return {
                        "success": False,
                        "error": "Encryption key not found",
                        "metadata": ipfs_data.get("metadata", {})
                    }
            
            # Return unencrypted data
            return {
                "success": True,
                "data": ipfs_data,
                "metadata": ipfs_data.get("metadata", {}),
                "timestamp": ipfs_data.get("timestamp"),
                "decrypted": False
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to retrieve from IPFS: {e}")
            return {"success": False, "error": str(e)}
    
    def pin_file(self, ipfs_hash: str) -> Dict[str, Any]:
        """Pin a file to prevent garbage collection"""
        try:
            response = requests.post(f"{self.ipfs_api_url}/api/v0/pin/add", params={"arg": ipfs_hash})
            
            if response.status_code == 200:
                logger.info(f"📌 File pinned: {ipfs_hash}")
                return {"success": True, "ipfs_hash": ipfs_hash}
            else:
                raise Exception(f"Pin failed: {response.text}")
                
        except Exception as e:
            logger.error(f"❌ Failed to pin file: {e}")
            return {"success": False, "error": str(e)}
    
    def get_ipfs_status(self) -> Dict[str, Any]:
        """Get IPFS node status"""
        try:
            # Get version
            version_response = requests.get(f"{self.ipfs_api_url}/api/v0/version")
            version = version_response.json().get("Version", "unknown") if version_response.status_code == 200 else "unknown"
            
            # Get ID
            id_response = requests.post(f"{self.ipfs_api_url}/api/v0/id")
            id_info = id_response.json() if id_response.status_code == 200 else {}
            
            # Get repo stats
            stats_response = requests.post(f"{self.ipfs_api_url}/api/v0/repo/stat")
            stats = stats_response.json() if stats_response.status_code == 200 else {}
            
            return {
                "connected": version_response.status_code == 200,
                "version": version,
                "peer_id": id_info.get("ID", "unknown"),
                "addresses": id_info.get("Addresses", []),
                "repo_stats": stats,
                "api_url": self.ipfs_api_url,
                "gateway_url": self.ipfs_gateway_url
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to get IPFS status: {e}")
            return {"connected": False, "error": str(e)}

# Global instance
ipfs_service = IPFSService()
