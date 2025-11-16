/**
 * Blockchain Service for SwasthVedha Frontend
 * Handles all blockchain interactions from the React frontend
 */

import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export interface MedicalRecordRequest {
  patient_id: string;
  record_type: 'symptom_analysis' | 'disease_prediction' | 'dosha_assessment';
  analysis_data: any;
  practitioner_address?: string;
}

export interface TreatmentProtocolRequest {
  patient_id: string;
  condition: string;
  treatment_data: any;
  medicines: any[];
  duration_days: number;
  practitioner_address?: string;
}

export interface MedicineAuthenticationRequest {
  medicine_data: any;
  manufacturer: string;
  batch_number: string;
  manufacture_date: string;
  expiry_date: string;
  test_results: string[];
}

export interface TreatmentOutcomeRequest {
  treatment_id: number;
  outcome_data: any;
  patient_satisfaction: number; // 0-255 scale
  symptom_improvement: number;  // 0-255 scale
  patient_feedback: string;
}

export interface BlockchainHealth {
  status: 'healthy' | 'unhealthy';
  blockchain: {
    connected: boolean;
    block_number?: number;
    chain_id?: number;
    account_address?: string;
  };
  ipfs: {
    connected: boolean;
    version?: string;
    peer_id?: string;
  };
}

export interface MedicalRecord {
  blockchain_record: {
    record_id: number;
    patient_id: string;
    record_hash: string;
    record_type: string;
    timestamp: number;
    is_valid: boolean;
    practitioner: string;
  };
  ipfs_data: any;
  metadata: any;
}

class BlockchainService {
  private api = axios.create({
    baseURL: `${API_BASE_URL}/api/blockchain`,
    headers: {
      'Content-Type': 'application/json',
    },
  });

  constructor() {
    // Add request interceptor for error handling
    this.api.interceptors.response.use(
      (response) => response,
      (error) => {
        console.error('Blockchain API Error:', error.response?.data || error.message);
        throw error;
      }
    );
  }

  /**
   * Check blockchain integration health
   */
  async getHealth(): Promise<BlockchainHealth> {
    const response = await this.api.get('/health');
    return response.data;
  }

  /**
   * Get blockchain and IPFS statistics
   */
  async getStats(): Promise<any> {
    const response = await this.api.get('/stats');
    return response.data;
  }

  /**
   * Create a new medical record on blockchain
   */
  async createMedicalRecord(request: MedicalRecordRequest): Promise<any> {
    const response = await this.api.post('/medical-record', request);
    return response.data;
  }

  /**
   * Get patient records from blockchain
   */
  async getPatientRecords(patientId: string, requesterAddress?: string): Promise<{
    success: boolean;
    patient_id: string;
    total_records: number;
    retrieved_records: number;
    records: MedicalRecord[];
  }> {
    const params = requesterAddress ? { requester_address: requesterAddress } : {};
    const response = await this.api.get(`/medical-records/${patientId}`, { params });
    return response.data;
  }

  /**
   * Start a new treatment protocol
   */
  async startTreatmentProtocol(request: TreatmentProtocolRequest): Promise<any> {
    const response = await this.api.post('/treatment-protocol', request);
    return response.data;
  }

  /**
   * Authenticate a medicine batch
   */
  async authenticateMedicine(request: MedicineAuthenticationRequest): Promise<any> {
    const response = await this.api.post('/medicine-authentication', request);
    return response.data;
  }

  /**
   * Report treatment outcome
   */
  async reportTreatmentOutcome(request: TreatmentOutcomeRequest): Promise<any> {
    const response = await this.api.post('/treatment-outcome', request);
    return response.data;
  }

  /**
   * Verify a practitioner
   */
  async verifyPractitioner(
    practitionerAddress: string,
    licenseData: any,
    specialization: string
  ): Promise<any> {
    const response = await this.api.post('/practitioner-verification', {
      practitioner_address: practitionerAddress,
      license_data: licenseData,
      specialization,
    });
    return response.data;
  }

  /**
   * Check if practitioner is verified
   */
  async checkPractitionerVerification(practitionerAddress: string): Promise<{
    success: boolean;
    practitioner_address: string;
    is_verified: boolean;
  }> {
    const response = await this.api.get(`/practitioner/${practitionerAddress}/verification`);
    return response.data;
  }

  /**
   * Get data from IPFS
   */
  async getIPFSData(ipfsHash: string, decrypt: boolean = true): Promise<any> {
    const response = await this.api.get(`/ipfs/${ipfsHash}`, {
      params: { decrypt }
    });
    return response.data;
  }

  /**
   * Save symptom analysis to blockchain
   */
  async saveSymptomAnalysis(
    patientId: string,
    symptomData: any,
    practitionerAddress?: string
  ): Promise<any> {
    return this.createMedicalRecord({
      patient_id: patientId,
      record_type: 'symptom_analysis',
      analysis_data: symptomData,
      practitioner_address: practitionerAddress,
    });
  }

  /**
   * Save disease prediction to blockchain
   */
  async saveDiseasePrediction(
    patientId: string,
    predictionData: any,
    practitionerAddress?: string
  ): Promise<any> {
    return this.createMedicalRecord({
      patient_id: patientId,
      record_type: 'disease_prediction',
      analysis_data: predictionData,
      practitioner_address: practitionerAddress,
    });
  }

  /**
   * Save dosha assessment to blockchain
   */
  async saveDoshaAssessment(
    patientId: string,
    doshaData: any,
    practitionerAddress?: string
  ): Promise<any> {
    return this.createMedicalRecord({
      patient_id: patientId,
      record_type: 'dosha_assessment',
      analysis_data: doshaData,
      practitioner_address: practitionerAddress,
    });
  }

  /**
   * Get patient's medical history
   */
  async getPatientMedicalHistory(patientId: string): Promise<MedicalRecord[]> {
    const result = await this.getPatientRecords(patientId);
    return result.records || [];
  }

  /**
   * Format timestamp to readable date
   */
  formatTimestamp(timestamp: number): string {
    return new Date(timestamp * 1000).toLocaleString();
  }

  /**
   * Get IPFS gateway URL for a hash
   */
  getIPFSGatewayUrl(ipfsHash: string): string {
    return `http://localhost:8080/ipfs/${ipfsHash}`;
  }

  /**
   * Get blockchain explorer URL for a transaction
   */
  getExplorerUrl(txHash: string): string {
    // For local Hardhat network
    return `http://localhost:8545`;
    // For Polygon Mumbai testnet:
    // return `https://mumbai.polygonscan.com/tx/${txHash}`;
    // For Polygon mainnet:
    // return `https://polygonscan.com/tx/${txHash}`;
  }
}

export const blockchainService = new BlockchainService();
export default blockchainService;
