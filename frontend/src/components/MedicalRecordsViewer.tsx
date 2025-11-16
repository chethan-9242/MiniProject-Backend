/**
 * Medical Records Viewer Component
 * Displays patient's blockchain-stored medical records
 */

import React, { useState, useEffect } from 'react';
import { Calendar, FileText, User, Hash, ExternalLink, Shield, Activity } from 'lucide-react';
import blockchainService, { MedicalRecord } from '../services/blockchain';

interface MedicalRecordsViewerProps {
  patientId: string;
  requesterAddress?: string;
}

const MedicalRecordsViewer: React.FC<MedicalRecordsViewerProps> = ({
  patientId,
  requesterAddress,
}) => {
  const [records, setRecords] = useState<MedicalRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedRecord, setSelectedRecord] = useState<MedicalRecord | null>(null);

  useEffect(() => {
    const fetchRecords = async () => {
      try {
        setLoading(true);
        setError(null);
        
        const result = await blockchainService.getPatientRecords(
          patientId,
          requesterAddress
        );
        
        if (result.success) {
          setRecords(result.records);
        } else {
          setError('Failed to retrieve medical records');
        }
      } catch (err: any) {
        setError(err.response?.data?.detail || 'Failed to fetch records');
      } finally {
        setLoading(false);
      }
    };

    if (patientId) {
      fetchRecords();
    }
  }, [patientId, requesterAddress]);

  const getRecordTypeColor = (recordType: string) => {
    switch (recordType) {
      case 'symptom_analysis':
        return 'bg-blue-100 text-blue-800';
      case 'disease_prediction':
        return 'bg-red-100 text-red-800';
      case 'dosha_assessment':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getRecordTypeIcon = (recordType: string) => {
    switch (recordType) {
      case 'symptom_analysis':
        return <Activity className="w-4 h-4" />;
      case 'disease_prediction':
        return <Shield className="w-4 h-4" />;
      case 'dosha_assessment':
        return <User className="w-4 h-4" />;
      default:
        return <FileText className="w-4 h-4" />;
    }
  };

  const formatAddress = (address: string) => {
    return `${address.slice(0, 6)}...${address.slice(-4)}`;
  };

  const viewOnIPFS = (ipfsHash: string) => {
    window.open(blockchainService.getIPFSGatewayUrl(ipfsHash), '_blank');
  };

  const viewTransaction = (txHash: string) => {
    window.open(blockchainService.getExplorerUrl(txHash), '_blank');
  };

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex items-center justify-center space-x-3">
          <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-500"></div>
          <span className="text-gray-600">Loading medical records...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex items-center space-x-3 text-red-600">
          <Shield className="w-5 h-5" />
          <span>{error}</span>
        </div>
      </div>
    );
  }

  if (records.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="text-center text-gray-500">
          <FileText className="w-12 h-12 mx-auto mb-3 text-gray-300" />
          <p>No medical records found for this patient</p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-semibold text-gray-800">
          Medical Records ({records.length})
        </h3>
        <div className="flex items-center space-x-2 text-sm text-gray-600">
          <User className="w-4 h-4" />
          <span>Patient: {patientId.slice(0, 8)}...</span>
        </div>
      </div>

      <div className="space-y-4">
        {records.map((record) => (
          <div
            key={record.blockchain_record.record_id}
            className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer"
            onClick={() => setSelectedRecord(record)}
          >
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center space-x-3 mb-2">
                  <span className={`inline-flex items-center space-x-1 px-2 py-1 rounded-full text-xs font-medium ${getRecordTypeColor(record.blockchain_record.record_type)}`}>
                    {getRecordTypeIcon(record.blockchain_record.record_type)}
                    <span className="capitalize">
                      {record.blockchain_record.record_type.replace('_', ' ')}
                    </span>
                  </span>
                  <div className="flex items-center space-x-1 text-sm text-gray-500">
                    <Calendar className="w-3 h-3" />
                    <span>{blockchainService.formatTimestamp(record.blockchain_record.timestamp)}</span>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <span className="text-gray-500">Record ID:</span>
                    <span className="ml-2 font-mono text-gray-700">
                      #{record.blockchain_record.record_id}
                    </span>
                  </div>
                  <div>
                    <span className="text-gray-500">Practitioner:</span>
                    <span className="ml-2 font-mono text-gray-700">
                      {formatAddress(record.blockchain_record.practitioner)}
                    </span>
                  </div>
                  <div>
                    <span className="text-gray-500">Status:</span>
                    <span className={`ml-2 ${record.blockchain_record.is_valid ? 'text-green-600' : 'text-red-600'}`}>
                      {record.blockchain_record.is_valid ? 'Valid' : 'Invalid'}
                    </span>
                  </div>
                  <div>
                    <span className="text-gray-500">Data Hash:</span>
                    <span className="ml-2 font-mono text-gray-700 text-xs">
                      {record.blockchain_record.record_hash.slice(0, 10)}...
                    </span>
                  </div>
                </div>

                {record.metadata && (
                  <div className="mt-3 p-2 bg-gray-50 rounded text-sm">
                    <div className="grid grid-cols-2 gap-2">
                      {record.metadata.original_patient_id && (
                        <div>
                          <span className="text-gray-500">Patient ID:</span>
                          <span className="ml-2">{record.metadata.original_patient_id}</span>
                        </div>
                      )}
                      {record.metadata.confidence && (
                        <div>
                          <span className="text-gray-500">Confidence:</span>
                          <span className="ml-2">{record.metadata.confidence}%</span>
                        </div>
                      )}
                    </div>
                  </div>
                )}
              </div>

              <div className="flex flex-col space-y-2 ml-4">
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    viewOnIPFS(record.blockchain_record.record_hash);
                  }}
                  className="p-2 text-blue-600 hover:bg-blue-50 rounded transition-colors"
                  title="View on IPFS"
                >
                  <ExternalLink className="w-4 h-4" />
                </button>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    navigator.clipboard.writeText(record.blockchain_record.record_hash);
                  }}
                  className="p-2 text-gray-600 hover:bg-gray-50 rounded transition-colors"
                  title="Copy Hash"
                >
                  <Hash className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Record Detail Modal */}
      {selectedRecord && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-4xl w-full max-h-[80vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-xl font-semibold text-gray-800">
                  Medical Record Details
                </h3>
                <button
                  onClick={() => setSelectedRecord(null)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  ✕
                </button>
              </div>

              <div className="space-y-6">
                {/* Blockchain Information */}
                <div className="bg-gray-50 rounded-lg p-4">
                  <h4 className="font-medium text-gray-800 mb-3">Blockchain Information</h4>
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <span className="text-gray-500">Record ID:</span>
                      <span className="ml-2 font-mono">#{selectedRecord.blockchain_record.record_id}</span>
                    </div>
                    <div>
                      <span className="text-gray-500">Type:</span>
                      <span className="ml-2 capitalize">{selectedRecord.blockchain_record.record_type.replace('_', ' ')}</span>
                    </div>
                    <div>
                      <span className="text-gray-500">Timestamp:</span>
                      <span className="ml-2">{blockchainService.formatTimestamp(selectedRecord.blockchain_record.timestamp)}</span>
                    </div>
                    <div>
                      <span className="text-gray-500">Status:</span>
                      <span className={`ml-2 ${selectedRecord.blockchain_record.is_valid ? 'text-green-600' : 'text-red-600'}`}>
                        {selectedRecord.blockchain_record.is_valid ? 'Valid' : 'Invalid'}
                      </span>
                    </div>
                    <div>
                      <span className="text-gray-500">Practitioner:</span>
                      <span className="ml-2 font-mono">{formatAddress(selectedRecord.blockchain_record.practitioner)}</span>
                    </div>
                    <div>
                      <span className="text-gray-500">IPFS Hash:</span>
                      <span className="ml-2 font-mono text-xs">{selectedRecord.blockchain_record.record_hash}</span>
                    </div>
                  </div>
                </div>

                {/* Medical Data */}
                <div className="bg-blue-50 rounded-lg p-4">
                  <h4 className="font-medium text-gray-800 mb-3">Medical Data</h4>
                  <pre className="text-sm bg-white p-3 rounded border overflow-x-auto">
                    {JSON.stringify(selectedRecord.ipfs_data, null, 2)}
                  </pre>
                </div>

                {/* Actions */}
                <div className="flex space-x-3">
                  <button
                    onClick={() => viewOnIPFS(selectedRecord.blockchain_record.record_hash)}
                    className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
                  >
                    View on IPFS
                  </button>
                  <button
                    onClick={() => navigator.clipboard.writeText(JSON.stringify(selectedRecord.ipfs_data, null, 2))}
                    className="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600 transition-colors"
                  >
                    Copy Data
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default MedicalRecordsViewer;
