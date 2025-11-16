"""
Blockchain Router for SwasthVedha
API endpoints for blockchain functionality
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import logging

from .web3_provider import web3_provider
from .ipfs_service import ipfs_service

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Pydantic models
class MedicalRecordRequest(BaseModel):
    patient_id: str
    record_type: str  # "symptom_analysis", "disease_prediction", "dosha_assessment"
    analysis_data: Dict[str, Any]
    practitioner_address: Optional[str] = None

class TreatmentProtocolRequest(BaseModel):
    patient_id: str
    condition: str
    treatment_data: Dict[str, Any]
    medicines: List[Dict[str, Any]]
    duration_days: int
    practitioner_address: Optional[str] = None

class MedicineAuthenticationRequest(BaseModel):
    medicine_data: Dict[str, Any]
    manufacturer: str
    batch_number: str
    manufacture_date: str
    expiry_date: str
    test_results: List[str]

class TreatmentOutcomeRequest(BaseModel):
    treatment_id: int
    outcome_data: Dict[str, Any]
    patient_satisfaction: int  # 0-255 scale
    symptom_improvement: int   # 0-255 scale
    patient_feedback: str

class PractitionerVerificationRequest(BaseModel):
    practitioner_address: str
    license_data: Dict[str, Any]
    specialization: str

@router.get("/health")
async def blockchain_health():
    """Check blockchain integration health"""
    try:
        blockchain_status = web3_provider.get_blockchain_status()
        ipfs_status = ipfs_service.get_ipfs_status()
        
        return {
            "status": "healthy" if blockchain_status["connected"] and ipfs_status["connected"] else "unhealthy",
            "blockchain": blockchain_status,
            "ipfs": ipfs_status,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"❌ Health check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/medical-record")
async def create_medical_record(request: MedicalRecordRequest):
    """Create a new medical record on blockchain"""
    try:
        # Upload data to IPFS first
        ipfs_result = ipfs_service.upload_medical_record(
            request.analysis_data, 
            request.patient_id
        )
        
        if not ipfs_result["success"]:
            raise HTTPException(status_code=500, detail=ipfs_result["error"])
        
        # Create blockchain record
        blockchain_result = web3_provider.create_medical_record(
            request.patient_id,
            ipfs_result["ipfs_hash"],
            request.record_type,
            request.practitioner_address
        )
        
        if not blockchain_result["success"]:
            raise HTTPException(status_code=500, detail=blockchain_result["error"])
        
        # Pin the IPFS file
        ipfs_service.pin_file(ipfs_result["ipfs_hash"])
        
        return {
            "success": True,
            "message": "Medical record created successfully",
            "ipfs_hash": ipfs_result["ipfs_hash"],
            "blockchain_tx": blockchain_result["transaction_hash"],
            "gateway_url": ipfs_result["gateway_url"],
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to create medical record: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/medical-records/{patient_id}")
async def get_patient_records(patient_id: str, requester_address: str = None):
    """Get patient records from blockchain"""
    try:
        if not requester_address:
            requester_address = web3_provider.account_address
        
        # Get blockchain records
        blockchain_records = web3_provider.get_patient_records(
            patient_id, 
            requester_address
        )
        
        # Retrieve IPFS data for each record
        records_with_data = []
        for record in blockchain_records:
            ipfs_result = ipfs_service.retrieve_from_ipfs(record["record_hash"])
            
            if ipfs_result["success"]:
                records_with_data.append({
                    "blockchain_record": record,
                    "ipfs_data": ipfs_result["data"],
                    "metadata": ipfs_result["metadata"]
                })
            else:
                logger.warning(f"⚠️ Could not retrieve IPFS data for record {record['record_id']}")
        
        return {
            "success": True,
            "patient_id": patient_id,
            "total_records": len(blockchain_records),
            "retrieved_records": len(records_with_data),
            "records": records_with_data,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Failed to get patient records: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/treatment-protocol")
async def start_treatment_protocol(request: TreatmentProtocolRequest):
    """Start a new treatment protocol"""
    try:
        # Upload treatment protocol to IPFS
        treatment_ipfs_result = ipfs_service.upload_treatment_protocol(
            request.treatment_data,
            request.practitioner_address or "system"
        )
        
        if not treatment_ipfs_result["success"]:
            raise HTTPException(status_code=500, detail=treatment_ipfs_result["error"])
        
        # Upload medicines to IPFS
        medicine_hashes = []
        for medicine in request.medicines:
            medicine_ipfs_result = ipfs_service.upload_medicine_info(medicine)
            if medicine_ipfs_result["success"]:
                medicine_hashes.append(medicine_ipfs_result["ipfs_hash"])
                ipfs_service.pin_file(medicine_ipfs_result["ipfs_hash"])
        
        # Calculate end date
        end_date = datetime.now() + timedelta(days=request.duration_days)
        end_date_timestamp = int(end_date.timestamp())
        
        # Create blockchain treatment record
        blockchain_result = web3_provider.start_treatment(
            request.patient_id,
            treatment_ipfs_result["ipfs_hash"],
            treatment_ipfs_result["ipfs_hash"],  # Using same hash for simplicity
            medicine_hashes,
            end_date_timestamp
        )
        
        if not blockchain_result["success"]:
            raise HTTPException(status_code=500, detail=blockchain_result["error"])
        
        # Pin treatment protocol
        ipfs_service.pin_file(treatment_ipfs_result["ipfs_hash"])
        
        return {
            "success": True,
            "message": "Treatment protocol started successfully",
            "treatment_ipfs_hash": treatment_ipfs_result["ipfs_hash"],
            "medicine_hashes": medicine_hashes,
            "blockchain_tx": blockchain_result["transaction_hash"],
            "end_date": end_date.isoformat(),
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to start treatment protocol: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/medicine-authentication")
async def authenticate_medicine(request: MedicineAuthenticationRequest):
    """Authenticate a medicine batch"""
    try:
        # Upload medicine info to IPFS
        ipfs_result = ipfs_service.upload_medicine_info(request.medicine_data)
        
        if not ipfs_result["success"]:
            raise HTTPException(status_code=500, detail=ipfs_result["error"])
        
        # Convert dates to timestamps
        manufacture_timestamp = int(datetime.fromisoformat(request.manufacture_date).timestamp())
        expiry_timestamp = int(datetime.fromisoformat(request.expiry_date).timestamp())
        
        # Create blockchain authentication
        blockchain_result = web3_provider.authenticate_medicine(
            ipfs_result["ipfs_hash"],
            request.manufacturer,
            request.batch_number,
            manufacture_timestamp,
            expiry_timestamp,
            request.test_results
        )
        
        if not blockchain_result["success"]:
            raise HTTPException(status_code=500, detail=blockchain_result["error"])
        
        # Pin the medicine info
        ipfs_service.pin_file(ipfs_result["ipfs_hash"])
        
        return {
            "success": True,
            "message": "Medicine authenticated successfully",
            "ipfs_hash": ipfs_result["ipfs_hash"],
            "blockchain_tx": blockchain_result["transaction_hash"],
            "manufacturer": request.manufacturer,
            "batch_number": request.batch_number,
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to authenticate medicine: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/treatment-outcome")
async def report_treatment_outcome(request: TreatmentOutcomeRequest):
    """Report treatment outcome"""
    try:
        # Upload outcome data to IPFS
        outcome_data = {
            "treatment_id": request.treatment_id,
            "outcome": request.outcome_data,
            "patient_satisfaction": request.patient_satisfaction,
            "symptom_improvement": request.symptom_improvement,
            "feedback": request.patient_feedback,
            "report_date": datetime.now().isoformat()
        }
        
        ipfs_result = ipfs_service.upload_treatment_protocol(
            outcome_data,
            "system"
        )
        
        if not ipfs_result["success"]:
            raise HTTPException(status_code=500, detail=ipfs_result["error"])
        
        # Create blockchain outcome record
        blockchain_result = web3_provider.report_treatment_outcome(
            request.treatment_id,
            ipfs_result["ipfs_hash"],
            request.patient_satisfaction,
            request.symptom_improvement,
            ipfs_result["ipfs_hash"]
        )
        
        if not blockchain_result["success"]:
            raise HTTPException(status_code=500, detail=blockchain_result["error"])
        
        # Pin the outcome data
        ipfs_service.pin_file(ipfs_result["ipfs_hash"])
        
        return {
            "success": True,
            "message": "Treatment outcome reported successfully",
            "ipfs_hash": ipfs_result["ipfs_hash"],
            "blockchain_tx": blockchain_result["transaction_hash"],
            "treatment_id": request.treatment_id,
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to report treatment outcome: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/practitioner-verification")
async def verify_practitioner(request: PractitionerVerificationRequest):
    """Verify a practitioner"""
    try:
        # Upload license data to IPFS
        ipfs_result = ipfs_service.upload_treatment_protocol(
            request.license_data,
            request.practitioner_address
        )
        
        if not ipfs_result["success"]:
            raise HTTPException(status_code=500, detail=ipfs_result["error"])
        
        # Create blockchain verification
        blockchain_result = web3_provider.verify_practitioner(
            request.practitioner_address,
            ipfs_result["ipfs_hash"],
            request.specialization
        )
        
        if not blockchain_result["success"]:
            raise HTTPException(status_code=500, detail=blockchain_result["error"])
        
        # Pin the license data
        ipfs_service.pin_file(ipfs_result["ipfs_hash"])
        
        return {
            "success": True,
            "message": "Practitioner verified successfully",
            "practitioner_address": request.practitioner_address,
            "specialization": request.specialization,
            "license_ipfs_hash": ipfs_result["ipfs_hash"],
            "blockchain_tx": blockchain_result["transaction_hash"],
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to verify practitioner: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/practitioner/{practitioner_address}/verification")
async def check_practitioner_verification(practitioner_address: str):
    """Check if practitioner is verified"""
    try:
        is_verified = web3_provider.is_practitioner_verified(practitioner_address)
        
        return {
            "success": True,
            "practitioner_address": practitioner_address,
            "is_verified": is_verified,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Failed to check practitioner verification: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/ipfs/{ipfs_hash}")
async def get_ipfs_data(ipfs_hash: str, decrypt: bool = True):
    """Get data from IPFS"""
    try:
        result = ipfs_service.retrieve_from_ipfs(ipfs_hash, decrypt)
        
        if not result["success"]:
            raise HTTPException(status_code=404, detail=result["error"])
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to get IPFS data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats")
async def get_blockchain_stats():
    """Get blockchain and IPFS statistics"""
    try:
        blockchain_status = web3_provider.get_blockchain_status()
        ipfs_status = ipfs_service.get_ipfs_status()
        
        return {
            "blockchain": blockchain_status,
            "ipfs": ipfs_status,
            "integration_status": "active" if blockchain_status["connected"] and ipfs_status["connected"] else "inactive",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Failed to get stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))
