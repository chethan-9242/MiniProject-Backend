// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract MedicalRecord is Ownable, ReentrancyGuard {
    using Counters for Counters.Counter;
    
    // Structs for medical data
    struct PatientRecord {
        string patientId;           // Hashed patient identifier
        string recordHash;          // IPFS hash of encrypted medical data
        string recordType;          // "symptom_analysis", "disease_prediction", "dosha_assessment"
        uint256 timestamp;          // When record was created
        bool isValid;               // Record validity status
        address practitioner;       // Certified practitioner address (if any)
        string[] consentHashes;     // Hashes of consent documents
    }
    
    struct Practitioner {
        address practitionerAddress;
        string licenseHash;         // IPFS hash of license/certification
        string specialization;      // "Ayurvedic", "Dermatology", etc.
        bool isVerified;           // Verification status
        uint256 verificationDate;  // When verified
    }
    
    struct ConsentRecord {
        string patientId;
        string dataHash;           // Hash of specific data being consented
        string purpose;            // Purpose of data usage
        uint256 expiryDate;        // Consent expiry timestamp
        bool isActive;            // Consent status
        address authorizedUser;   // Who can access the data
    }
    
    // Mappings
    Counters.Counter private _recordIds;
    mapping(uint256 => PatientRecord) public medicalRecords;
    mapping(string => uint256[]) public patientRecords; // patientId => recordIds
    mapping(address => Practitioner) public practitioners;
    mapping(string => ConsentRecord) public consents;
    mapping(address => bool) public authorizedSystems;
    
    // Events
    event RecordCreated(
        uint256 indexed recordId,
        string patientId,
        string recordHash,
        string recordType,
        uint256 timestamp
    );
    
    event PractitionerVerified(
        address indexed practitioner,
        string specialization,
        uint256 verificationDate
    );
    
    event ConsentGranted(
        string patientId,
        address indexed authorizedUser,
        string purpose,
        uint256 expiryDate
    );
    
    event RecordAccessed(
        uint256 indexed recordId,
        address indexed accessor,
        uint256 timestamp
    );
    
    constructor() {
        // Authorize the SwasthVedha backend system
        authorizedSystems[msg.sender] = true;
    }
    
    // Modifier for authorized systems only
    modifier onlyAuthorized() {
        require(
            authorizedSystems[msg.sender] || msg.sender == owner(),
            "Not authorized to access this function"
        );
        _;
    }
    
    // Create a new medical record
    function createMedicalRecord(
        string memory _patientId,
        string memory _recordHash,
        string memory _recordType,
        address _practitioner
    ) public onlyAuthorized nonReentrant returns (uint256) {
        _recordIds.increment();
        uint256 newRecordId = _recordIds.current();
        
        medicalRecords[newRecordId] = PatientRecord({
            patientId: _patientId,
            recordHash: _recordHash,
            recordType: _recordType,
            timestamp: block.timestamp,
            isValid: true,
            practitioner: _practitioner,
            consentHashes: new string[](0)
        });
        
        patientRecords[_patientId].push(newRecordId);
        
        emit RecordCreated(newRecordId, _patientId, _recordHash, _recordType, block.timestamp);
        return newRecordId;
    }
    
    // Verify a practitioner
    function verifyPractitioner(
        address _practitionerAddress,
        string memory _licenseHash,
        string memory _specialization
    ) public onlyOwner {
        practitioners[_practitionerAddress] = Practitioner({
            practitionerAddress: _practitionerAddress,
            licenseHash: _licenseHash,
            specialization: _specialization,
            isVerified: true,
            verificationDate: block.timestamp
        });
        
        emit PractitionerVerified(_practitionerAddress, _specialization, block.timestamp);
    }
    
    // Grant consent for data access
    function grantConsent(
        string memory _patientId,
        string memory _dataHash,
        string memory _purpose,
        uint256 _expiryDate,
        address _authorizedUser
    ) public onlyAuthorized {
        consents[_dataHash] = ConsentRecord({
            patientId: _patientId,
            dataHash: _dataHash,
            purpose: _purpose,
            expiryDate: _expiryDate,
            isActive: true,
            authorizedUser: _authorizedUser
        });
        
        emit ConsentGranted(_patientId, _authorizedUser, _purpose, _expiryDate);
    }
    
    // Get patient records (with consent check)
    function getPatientRecords(string memory _patientId, address _requester) 
        public view returns (uint256[] memory) {
        // Check if requester has valid consent
        uint256[] memory records = patientRecords[_patientId];
        uint256[] memory accessibleRecords = new uint256[](records.length);
        uint256 count = 0;
        
        for (uint i = 0; i < records.length; i++) {
            if (hasAccessPermission(records[i], _requester)) {
                accessibleRecords[count] = records[i];
                count++;
            }
        }
        
        // Resize array to actual count
        uint256[] memory result = new uint256[](count);
        for (uint i = 0; i < count; i++) {
            result[i] = accessibleRecords[i];
        }
        
        return result;
    }
    
    // Check if user has access to a specific record
    function hasAccessPermission(uint256 _recordId, address _requester) 
        public view returns (bool) {
        PatientRecord memory record = medicalRecords[_recordId];
        
        // Owner access
        if (authorizedSystems[_requester] || _requester == owner()) {
            return true;
        }
        
        // Practitioner access
        if (record.practitioner == _requester && practitioners[_requester].isVerified) {
            return true;
        }
        
        // Consent-based access
        ConsentRecord memory consent = consents[record.recordHash];
        if (consent.isActive && 
            consent.authorizedUser == _requester && 
            block.timestamp < consent.expiryDate) {
            return true;
        }
        
        return false;
    }
    
    // Get record details (if authorized)
    function getRecord(uint256 _recordId, address _requester) 
        public view returns (PatientRecord memory) {
        require(hasAccessPermission(_recordId, _requester), "Access denied");
        return medicalRecords[_recordId];
    }
    
    // Authorize new system
    function authorizeSystem(address _systemAddress) public onlyOwner {
        authorizedSystems[_systemAddress] = true;
    }
    
    // Revoke system authorization
    function revokeSystemAuthorization(address _systemAddress) public onlyOwner {
        authorizedSystems[_systemAddress] = false;
    }
    
    // Get total number of records
    function getTotalRecords() public view returns (uint256) {
        return _recordIds.current();
    }
    
    // Check if practitioner is verified
    function isPractitionerVerified(address _practitioner) public view returns (bool) {
        return practitioners[_practitioner].isVerified;
    }
}
