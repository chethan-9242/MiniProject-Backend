"""
Blockchain Integration Module for SwasthVedha
Provides blockchain and IPFS functionality for medical data management
"""

from .web3_provider import web3_provider
from .ipfs_service import ipfs_service
from .blockchain_router import router

__version__ = "1.0.0"
__all__ = ["web3_provider", "ipfs_service", "router"]
