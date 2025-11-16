const { create } = require("ipfs-http-client");
const crypto = require("crypto");
const fs = require("fs");
const path = require("path");

// IPFS client configuration
const IPFS_CLIENT = create({
  host: "localhost",
  port: "5001",
  protocol: "http",
});

// Encryption utilities
class DataEncryption {
  static generateKey() {
    return crypto.randomBytes(32);
  }

  static encryptData(data, key) {
    const iv = crypto.randomBytes(16);
    const cipher = crypto.createCipher("aes-256-cbc", key);
    let encrypted = cipher.update(JSON.stringify(data), "utf8", "hex");
    encrypted += cipher.final("hex");
    return { encrypted, iv: iv.toString("hex") };
  }

  static decryptData(encryptedData, key, iv) {
    const decipher = crypto.createDecipher("aes-256-cbc", key);
    let decrypted = decipher.update(encryptedData, "hex", "utf8");
    decrypted += decipher.final("utf8");
    return JSON.parse(decrypted);
  }

  static hashData(data) {
    return crypto.createHash("sha256").update(JSON.stringify(data)).digest("hex");
  }
}

// IPFS Upload Service
class IPFSService {
  static async uploadMedicalRecord(data, patientId) {
    try {
      console.log(`📤 Uploading medical record for patient: ${patientId}`);
      
      // Generate encryption key for this record
      const encryptionKey = DataEncryption.generateKey();
      
      // Encrypt the medical data
      const { encrypted, iv } = DataEncryption.encryptData(data, encryptionKey);
      
      // Create IPFS upload structure
      const ipfsData = {
        patientId: DataEncryption.hashData(patientId), // Hash patient ID for privacy
        encryptedData: encrypted,
        iv: iv,
        timestamp: new Date().toISOString(),
        dataType: "medical_record",
        version: "1.0"
      };

      // Upload to IPFS
      const { cid } = await IPFS_CLIENT.add(JSON.stringify(ipfsData));
      const ipfsHash = cid.toString();
      
      console.log(`✅ Medical record uploaded to IPFS: ${ipfsHash}`);
      
      // Save encryption key securely (in production, use secure key management)
      const keyInfo = {
        ipfsHash,
        encryptionKey: encryptionKey.toString("hex"),
        patientId,
        uploadedAt: new Date().toISOString()
      };
      
      // Store key info locally (in production, use secure vault)
      this.saveEncryptionKey(keyInfo);
      
      return {
        ipfsHash,
        success: true,
        timestamp: ipfsData.timestamp
      };
      
    } catch (error) {
      console.error("❌ Failed to upload medical record to IPFS:", error);
      throw error;
    }
  }

  static async uploadTreatmentProtocol(data, practitionerId) {
    try {
      console.log(`📤 Uploading treatment protocol from practitioner: ${practitionerId}`);
      
      const ipfsData = {
        practitionerId: DataEncryption.hashData(practitionerId),
        treatmentData: data,
        timestamp: new Date().toISOString(),
        dataType: "treatment_protocol",
        version: "1.0"
      };

      const { cid } = await IPFS_CLIENT.add(JSON.stringify(ipfsData));
      const ipfsHash = cid.toString();
      
      console.log(`✅ Treatment protocol uploaded to IPFS: ${ipfsHash}`);
      
      return {
        ipfsHash,
        success: true,
        timestamp: ipfsData.timestamp
      };
      
    } catch (error) {
      console.error("❌ Failed to upload treatment protocol to IPFS:", error);
      throw error;
    }
  }

  static async uploadMedicineInfo(medicineData) {
    try {
      console.log(`📤 Uploading medicine information for: ${medicineData.name}`);
      
      const ipfsData = {
        medicineData,
        timestamp: new Date().toISOString(),
        dataType: "medicine_info",
        version: "1.0"
      };

      const { cid } = await IPFS_CLIENT.add(JSON.stringify(ipfsData));
      const ipfsHash = cid.toString();
      
      console.log(`✅ Medicine information uploaded to IPFS: ${ipfsHash}`);
      
      return {
        ipfsHash,
        success: true,
        timestamp: ipfsData.timestamp
      };
      
    } catch (error) {
      console.error("❌ Failed to upload medicine information to IPFS:", error);
      throw error;
    }
  }

  static async retrieveFromIPFS(ipfsHash) {
    try {
      console.log(`📥 Retrieving data from IPFS: ${ipfsHash}`);
      
      const chunks = [];
      for await (const chunk of IPFS_CLIENT.cat(ipfsHash)) {
        chunks.push(chunk);
      }
      
      const data = Buffer.concat(chunks).toString();
      return JSON.parse(data);
      
    } catch (error) {
      console.error("❌ Failed to retrieve data from IPFS:", error);
      throw error;
    }
  }

  static saveEncryptionKey(keyInfo) {
    const keysDir = "./encryption_keys";
    if (!fs.existsSync(keysDir)) {
      fs.mkdirSync(keysDir);
    }
    
    const keyFile = path.join(keysDir, `${keyInfo.ipfsHash}.json`);
    fs.writeFileSync(keyFile, JSON.stringify(keyInfo, null, 2));
    console.log(`🔐 Encryption key saved for hash: ${keyInfo.ipfsHash}`);
  }

  static getEncryptionKey(ipfsHash) {
    const keyFile = path.join("./encryption_keys", `${ipfsHash}.json`);
    if (fs.existsSync(keyFile)) {
      const keyInfo = JSON.parse(fs.readFileSync(keyFile, "utf8"));
      return Buffer.from(keyInfo.encryptionKey, "hex");
    }
    return null;
  }
}

// Example usage and testing
async function main() {
  try {
    console.log("🚀 Testing IPFS Upload Service...");
    
    // Example medical record
    const medicalRecord = {
      patientId: "patient_123",
      analysisType: "symptom_analysis",
      symptoms: ["headache", "fatigue", "stress"],
      predictedCondition: "Tension Headache (Shiroroga)",
      confidence: 85.5,
      recommendations: {
        herbal: ["Ashwagandha", "Brahmi"],
        dietary: ["Warm foods", "Avoid caffeine"],
        lifestyle: ["Regular sleep", "Meditation"]
      },
      practitioner: "dr_ayurvedic_456"
    };

    // Upload medical record
    const recordResult = await IPFSService.uploadMedicalRecord(
      medicalRecord, 
      medicalRecord.patientId
    );
    
    // Example treatment protocol
    const treatmentProtocol = {
      condition: "Tension Headache (Shiroroga)",
      duration: "30 days",
      medicines: [
        {
          name: "Ashwagandha Churna",
          dosage: "500mg twice daily",
          duration: "30 days"
        },
        {
          name: "Brahmi Ghrita",
          dosage: "1 tsp morning",
          duration: "30 days"
        }
      ],
      dietaryRestrictions: ["Avoid spicy foods", "No caffeine"],
      lifestyleChanges: ["Early bedtime", "Oil massage"],
      followUpRequired: true
    };

    const treatmentResult = await IPFSService.uploadTreatmentProtocol(
      treatmentProtocol,
      "dr_ayurvedic_456"
    );

    // Example medicine information
    const medicineInfo = {
      name: "Ashwagandha Churna",
      manufacturer: "Ayurvedic Pharma Ltd",
      batchNumber: "ASH2024001",
      manufactureDate: "2024-01-15",
      expiryDate: "2026-01-15",
      composition: "Withania somnifera root powder",
      qualityTests: [
        {
          test: "Heavy metal analysis",
          result: "Within limits",
          certificate: "QC-ASH-001"
        },
        {
          test: "Microbial analysis",
          result: "Pass",
          certificate: "QC-ASH-002"
        }
      ]
    };

    const medicineResult = await IPFSService.uploadMedicineInfo(medicineInfo);

    console.log("\n🎉 Upload Results:");
    console.log("==================");
    console.log("📋 Medical Record:", recordResult.ipfsHash);
    console.log("💊 Treatment Protocol:", treatmentResult.ipfsHash);
    console.log("🌿 Medicine Info:", medicineResult.ipfsHash);
    console.log("==================");

    // Test retrieval
    console.log("\n📥 Testing data retrieval...");
    const retrievedRecord = await IPFSService.retrieveFromIPFS(recordResult.ipfsHash);
    console.log("✅ Successfully retrieved medical record");

  } catch (error) {
    console.error("❌ Test failed:", error);
  }
}

// Export for use in other modules
module.exports = {
  IPFSService,
  DataEncryption
};

// Run tests if called directly
if (require.main === module) {
  main();
}
