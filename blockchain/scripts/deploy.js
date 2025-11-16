const { ethers } = require("hardhat");
require("dotenv").config();

async function main() {
  console.log("🚀 Deploying SwasthVedha Blockchain Contracts...");
  
  // Get the deployer account
  const [deployer] = await ethers.getSigners();
  console.log("📝 Deploying contracts with the account:", deployer.address);
  console.log("💰 Account balance:", (await deployer.getBalance()).toString());

  // Deploy MedicalRecord contract
  console.log("\n🏥 Deploying MedicalRecord contract...");
  const MedicalRecord = await ethers.getContractFactory("MedicalRecord");
  const medicalRecord = await MedicalRecord.deploy();
  await medicalRecord.deployed();
  console.log("✅ MedicalRecord deployed to:", medicalRecord.address);

  // Deploy TreatmentTracking contract
  console.log("\n💊 Deploying TreatmentTracking contract...");
  const TreatmentTracking = await ethers.getContractFactory("TreatmentTracking");
  const treatmentTracking = await TreatmentTracking.deploy();
  await treatmentTracking.deployed();
  console.log("✅ TreatmentTracking deployed to:", treatmentTracking.address);

  // Authorize the TreatmentTracking contract to access MedicalRecord
  console.log("\n🔗 Setting up contract permissions...");
  await medicalRecord.authorizeSystem(treatmentTracking.address);
  console.log("✅ TreatmentTracking authorized in MedicalRecord");

  // Save deployment addresses
  const deploymentInfo = {
    network: network.name,
    chainId: network.config.chainId,
    deployer: deployer.address,
    contracts: {
      MedicalRecord: medicalRecord.address,
      TreatmentTracking: treatmentTracking.address
    },
    deployedAt: new Date().toISOString(),
    gasUsed: {
      MedicalRecord: (await medicalRecord.deployTransaction.wait()).gasUsed.toString(),
      TreatmentTracking: (await treatmentTracking.deployTransaction.wait()).gasUsed.toString()
    }
  };

  // Save to file
  const fs = require("fs");
  const deploymentPath = `./deployments/${network.name}.json`;
  
  // Ensure deployments directory exists
  if (!fs.existsSync("./deployments")) {
    fs.mkdirSync("./deployments");
  }
  
  fs.writeFileSync(deploymentPath, JSON.stringify(deploymentInfo, null, 2));
  console.log(`\n📄 Deployment info saved to: ${deploymentPath}`);

  // Log summary
  console.log("\n🎉 Deployment Summary:");
  console.log("=====================================");
  console.log(`📍 Network: ${network.name} (Chain ID: ${network.config.chainId})`);
  console.log(`🏥 MedicalRecord: ${medicalRecord.address}`);
  console.log(`💊 TreatmentTracking: ${treatmentTracking.address}`);
  console.log(`👤 Deployer: ${deployer.address}`);
  console.log("=====================================");

  // Verify contracts on Etherscan (if not localhost)
  if (network.name !== "hardhat" && network.name !== "localhost") {
    console.log("\n🔍 Verifying contracts on Etherscan...");
    try {
      await hre.run("verify:verify", {
        address: medicalRecord.address,
        constructorArguments: [],
      });
      console.log("✅ MedicalRecord verified");
    } catch (error) {
      console.log("❌ MedicalRecord verification failed:", error.message);
    }

    try {
      await hre.run("verify:verify", {
        address: treatmentTracking.address,
        constructorArguments: [],
      });
      console.log("✅ TreatmentTracking verified");
    } catch (error) {
      console.log("❌ TreatmentTracking verification failed:", error.message);
    }
  }

  console.log("\n🚀 Setup complete! You can now use the SwasthVedha blockchain integration.");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error("❌ Deployment failed:", error);
    process.exit(1);
  });
