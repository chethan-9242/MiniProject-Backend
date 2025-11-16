// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract TreatmentTracking is Ownable, ReentrancyGuard {
    using Counters for Counters.Counter;
    
    struct Treatment {
        uint256 treatmentId;
        string patientId;           // Hashed patient identifier
        string conditionHash;       // IPFS hash of condition details
        string treatmentHash;       // IPFS hash of treatment protocol
        string[] medicineHashes;    // IPFS hashes of prescribed medicines
        uint256 startDate;          // Treatment start date
        uint256 endDate;            // Expected end date
        bool isActive;              // Treatment status
        address practitioner;       // Prescribing practitioner
        uint8 effectiveness;       // 0-255 scale (0 = no data, 255 = highly effective)
    }
    
    struct Medicine {
        string medicineHash;        // IPFS hash of medicine details
        string manufacturer;        // Manufacturer identifier
        string batchNumber;         // Batch number
        uint256 manufactureDate;    // Manufacture date
        uint256 expiryDate;         // Expiry date
        bool isAuthentic;           // Authentication status
        string[] testResults;       // Quality test result hashes
    }
    
    struct TreatmentOutcome {
        uint256 treatmentId;
        string outcomeHash;         // IPFS hash of outcome details
        uint8 patientSatisfaction;  // 0-255 scale
        uint8 symptomImprovement;   // 0-255 scale
        string feedbackHash;        // IPFS hash of patient feedback
        uint256 reportDate;         // When outcome was reported
    }
    
    Counters.Counter private _treatmentIds;
    mapping(uint256 => Treatment) public treatments;
    mapping(string => uint256[]) public patientTreatments; // patientId => treatmentIds
    mapping(string => Medicine) public medicines;
    mapping(uint256 => TreatmentOutcome) public outcomes;
    mapping(address => bool) public authorizedPractitioners;
    
    // Events
    event TreatmentStarted(
        uint256 indexed treatmentId,
        string patientId,
        string conditionHash,
        address indexed practitioner
    );
    
    event MedicineAuthenticated(
        string indexed medicineHash,
        string manufacturer,
        string batchNumber
    );
    
    event OutcomeReported(
        uint256 indexed treatmentId,
        uint8 patientSatisfaction,
        uint8 symptomImprovement
    );
    
    constructor() {
        authorizedPractitioners[msg.sender] = true;
    }
    
    modifier onlyAuthorizedPractitioner() {
        require(
            authorizedPractitioners[msg.sender] || msg.sender == owner(),
            "Not authorized practitioner"
        );
        _;
    }
    
    // Start a new treatment protocol
    function startTreatment(
        string memory _patientId,
        string memory _conditionHash,
        string memory _treatmentHash,
        string[] memory _medicineHashes,
        uint256 _endDate
    ) public onlyAuthorizedPractitioner nonReentrant returns (uint256) {
        _treatmentIds.increment();
        uint256 newTreatmentId = _treatmentIds.current();
        
        treatments[newTreatmentId] = Treatment({
            treatmentId: newTreatmentId,
            patientId: _patientId,
            conditionHash: _conditionHash,
            treatmentHash: _treatmentHash,
            medicineHashes: _medicineHashes,
            startDate: block.timestamp,
            endDate: _endDate,
            isActive: true,
            practitioner: msg.sender,
            effectiveness: 0
        });
        
        patientTreatments[_patientId].push(newTreatmentId);
        
        emit TreatmentStarted(newTreatmentId, _patientId, _conditionHash, msg.sender);
        return newTreatmentId;
    }
    
    // Authenticate a medicine batch
    function authenticateMedicine(
        string memory _medicineHash,
        string memory _manufacturer,
        string memory _batchNumber,
        uint256 _manufactureDate,
        uint256 _expiryDate,
        string[] memory _testResults
    ) public onlyOwner {
        medicines[_medicineHash] = Medicine({
            medicineHash: _medicineHash,
            manufacturer: _manufacturer,
            batchNumber: _batchNumber,
            manufactureDate: _manufactureDate,
            expiryDate: _expiryDate,
            isAuthentic: true,
            testResults: _testResults
        });
        
        emit MedicineAuthenticated(_medicineHash, _manufacturer, _batchNumber);
    }
    
    // Report treatment outcome
    function reportOutcome(
        uint256 _treatmentId,
        string memory _outcomeHash,
        uint8 _patientSatisfaction,
        uint8 _symptomImprovement,
        string memory _feedbackHash
    ) public onlyAuthorizedPractitioner {
        require(treatments[_treatmentId].isActive, "Treatment not found or inactive");
        
        outcomes[_treatmentId] = TreatmentOutcome({
            treatmentId: _treatmentId,
            outcomeHash: _outcomeHash,
            patientSatisfaction: _patientSatisfaction,
            symptomImprovement: _symptomImprovement,
            feedbackHash: _feedbackHash,
            reportDate: block.timestamp
        });
        
        // Update treatment effectiveness (average of satisfaction and improvement)
        treatments[_treatmentId].effectiveness = (_patientSatisfaction + _symptomImprovement) / 2;
        
        emit OutcomeReported(_treatmentId, _patientSatisfaction, _symptomImprovement);
    }
    
    // Complete treatment
    function completeTreatment(uint256 _treatmentId) public onlyAuthorizedPractitioner {
        require(treatments[_treatmentId].isActive, "Treatment not found or inactive");
        treatments[_treatmentId].isActive = false;
    }
    
    // Get patient treatments
    function getPatientTreatments(string memory _patientId) 
        public view returns (uint256[] memory) {
        return patientTreatments[_patientId];
    }
    
    // Get treatment details
    function getTreatment(uint256 _treatmentId) public view returns (Treatment memory) {
        return treatments[_treatmentId];
    }
    
    // Get treatment outcome
    function getOutcome(uint256 _treatmentId) public view returns (TreatmentOutcome memory) {
        return outcomes[_treatmentId];
    }
    
    // Check medicine authenticity
    function isMedicineAuthentic(string memory _medicineHash) public view returns (bool) {
        return medicines[_medicineHash].isAuthentic;
    }
    
    // Authorize practitioner
    function authorizePractitioner(address _practitioner) public onlyOwner {
        authorizedPractitioners[_practitioner] = true;
    }
    
    // Get total treatments
    function getTotalTreatments() public view returns (uint256) {
        return _treatmentIds.current();
    }
}
