import chromadb

# Connect to your existing database
client = chromadb.PersistentClient(
    path="C:/Users/Chethan/OneDrive/Desktop/SwasthVedha/backend/data/chroma_db"
)

# Delete existing collection if it exists
collection_name = "medical_records"
try:
    client.delete_collection(collection_name)
except:
    pass

# Create a new collection with metadata
metadata = {
    "description": "Collection of medical records including symptoms, vitals, and prescriptions",
    "department": "general_medicine",
    "hospital": "SwasthVedha General Hospital",
    "created_date": "2025-10-18"
}

# Create new collection
collection = client.create_collection(
    name=collection_name,
    metadata=metadata
)

# Add some medical documents with rich metadata
documents = [
    "Patient reported fever and cough for 3 days",
    "Blood pressure reading: 120/80, temperature: 98.6F",
    "Prescribed antibiotics for respiratory infection"
]
metadata = [
    {
        "type": "symptom_record",
        "date": "2025-10-18",
        "department": "general_medicine",
        "priority": "medium"
    },
    {
        "type": "vital_signs",
        "date": "2025-10-18",
        "department": "emergency",
        "priority": "low"
    },
    {
        "type": "prescription",
        "date": "2025-10-18",
        "department": "general_medicine",
        "priority": "high"
    }
]
ids = ["record1", "record2", "record3"]

# Add documents to the collection
collection.add(
    documents=documents,
    metadatas=metadata,
    ids=ids)

print("Documents added successfully!")

# Query to verify the data was added
results = collection.query(
    query_texts=["first document"],
    n_results=1
)
print("\nTest query result:", results)

# Print collection metadata
print("\nCollection Metadata:")
collection_info = client.get_collection(name=collection_name)
print(collection_info.metadata)