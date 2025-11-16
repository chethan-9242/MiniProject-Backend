/**
 * Blockchain Status Component
 * Displays real-time blockchain and IPFS connection status
 */

import React, { useState, useEffect } from 'react';
import { CheckCircle, XCircle, AlertCircle, Activity, Database, Globe } from 'lucide-react';
import blockchainService from '../services/blockchain';

interface BlockchainHealth {
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

const BlockchainStatus: React.FC = () => {
  const [health, setHealth] = useState<BlockchainHealth | null>(null);
  const [loading, setLoading] = useState(true);
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date());

  useEffect(() => {
    const fetchHealth = async () => {
      try {
        const healthData = await blockchainService.getHealth();
        setHealth(healthData);
        setLastUpdate(new Date());
      } catch (error) {
        console.error('Failed to fetch blockchain health:', error);
        setHealth({
          status: 'unhealthy',
          blockchain: { connected: false },
          ipfs: { connected: false },
        });
      } finally {
        setLoading(false);
      }
    };

    // Initial fetch
    fetchHealth();

    // Poll every 30 seconds
    const interval = setInterval(fetchHealth, 30000);

    return () => clearInterval(interval);
  }, []);

  const getStatusIcon = (connected: boolean) => {
    if (connected) {
      return <CheckCircle className="w-4 h-4 text-green-500" />;
    } else {
      return <XCircle className="w-4 h-4 text-red-500" />;
    }
  };

  const getStatusColor = (connected: boolean) => {
    return connected ? 'text-green-600' : 'text-red-600';
  };

  const formatAddress = (address?: string) => {
    if (!address) return 'N/A';
    return `${address.slice(0, 6)}...${address.slice(-4)}`;
  };

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-md p-4">
        <div className="flex items-center space-x-2">
          <Activity className="w-5 h-5 text-blue-500 animate-spin" />
          <span className="text-gray-600">Loading blockchain status...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-4">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-800">Blockchain Status</h3>
        <div className="flex items-center space-x-2">
          {health?.status === 'healthy' ? (
            <CheckCircle className="w-5 h-5 text-green-500" />
          ) : (
            <AlertCircle className="w-5 h-5 text-yellow-500" />
          )}
          <span className={`text-sm font-medium ${
            health?.status === 'healthy' ? 'text-green-600' : 'text-yellow-600'
          }`}>
            {health?.status === 'healthy' ? 'Connected' : 'Issues Detected'}
          </span>
        </div>
      </div>

      <div className="space-y-3">
        {/* Blockchain Status */}
        <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
          <div className="flex items-center space-x-3">
            <Database className="w-5 h-5 text-blue-500" />
            <div>
              <p className="font-medium text-gray-800">Blockchain</p>
              <p className="text-sm text-gray-600">
                {health?.blockchain.chain_id === 31337 ? 'Local Hardhat' : 
                 health?.blockchain.chain_id === 80001 ? 'Polygon Mumbai' :
                 `Chain ID: ${health?.blockchain.chain_id || 'Unknown'}`}
              </p>
            </div>
          </div>
          <div className="text-right">
            <div className="flex items-center space-x-2">
              {getStatusIcon(health?.blockchain.connected || false)}
              <span className={`text-sm font-medium ${getStatusColor(health?.blockchain.connected || false)}`}>
                {health?.blockchain.connected ? 'Connected' : 'Disconnected'}
              </span>
            </div>
            {health?.blockchain.block_number && (
              <p className="text-xs text-gray-500 mt-1">
                Block #{health.blockchain.block_number}
              </p>
            )}
          </div>
        </div>

        {/* IPFS Status */}
        <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
          <div className="flex items-center space-x-3">
            <Globe className="w-5 h-5 text-green-500" />
            <div>
              <p className="font-medium text-gray-800">IPFS Storage</p>
              <p className="text-sm text-gray-600">
                {health?.ipfs.version || 'Unknown Version'}
              </p>
            </div>
          </div>
          <div className="text-right">
            <div className="flex items-center space-x-2">
              {getStatusIcon(health?.ipfs.connected || false)}
              <span className={`text-sm font-medium ${getStatusColor(health?.ipfs.connected || false)}`}>
                {health?.ipfs.connected ? 'Connected' : 'Disconnected'}
              </span>
            </div>
            {health?.ipfs.peer_id && (
              <p className="text-xs text-gray-500 mt-1">
                Peer: {health.ipfs.peer_id.slice(0, 8)}...
              </p>
            )}
          </div>
        </div>

        {/* Account Information */}
        {health?.blockchain.account_address && (
          <div className="p-3 bg-blue-50 rounded-lg">
            <div className="flex items-center justify-between">
              <div>
                <p className="font-medium text-gray-800">Active Account</p>
                <p className="text-sm text-gray-600 font-mono">
                  {formatAddress(health.blockchain.account_address)}
                </p>
              </div>
              <div className="text-right">
                <p className="text-xs text-gray-500">System Account</p>
                <p className="text-xs text-blue-600">Backend Service</p>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Last Update */}
      <div className="mt-4 pt-3 border-t border-gray-200">
        <p className="text-xs text-gray-500">
          Last updated: {lastUpdate.toLocaleTimeString()}
        </p>
      </div>

      {/* Action Buttons */}
      <div className="mt-4 flex space-x-2">
        <button
          onClick={() => window.location.reload()}
          className="px-3 py-1 text-sm bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
        >
          Refresh
        </button>
        <button
          onClick={() => window.open('http://localhost:8000/api/blockchain/health', '_blank')}
          className="px-3 py-1 text-sm bg-gray-500 text-white rounded hover:bg-gray-600 transition-colors"
        >
          View Details
        </button>
      </div>
    </div>
  );
};

export default BlockchainStatus;
