import chromadb
from datetime import datetime

class SwasthVedhaDB:
    def __init__(self):
        self.client = chromadb.PersistentClient(
            path="C:/Users/Chethan/OneDrive/Desktop/SwasthVedha/backend/data/chroma_db"
        )
        # Initialize all collections
        self.setup_collections()

    def setup_collections(self):
        """Set up all required collections"""
        # Patient Records Collection
        self.patient_records = self.client.get_or_create_collection(
            name="patient_records",
            metadata={
                "description": "Patient medical records, history, and personal information",
                "type": "patient_data",
                "created_date": datetime.now().strftime("%Y-%m-%d")
            }
        )

        # Medical Documents Collection
        self.medical_docs = self.client.get_or_create_collection(
            name="medical_documents",
            metadata={
                "description": "Medical documents, reports, and test results",
                "type": "medical_documents",
                "created_date": datetime.now().strftime("%Y-%m-%d")
            }
        )

        # Chat Conversations Collection
        self.chat_history = self.client.get_or_create_collection(
            name="chat_conversations",
            metadata={
                "description": "Patient-doctor chat conversations and consultations",
                "type": "chat_history",
                "created_date": datetime.now().strftime("%Y-%m-%d")
            }
        )

    def add_patient_record(self, patient_data, metadata):
        """Add patient record"""
        self.patient_records.add(
            documents=[patient_data],
            metadatas=[{
                **metadata,
                "record_type": "patient_record",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }],
            ids=[f"patient_{metadata.get('patient_id')}_{datetime.now().strftime('%Y%m%d%H%M%S')}"]
        )

    def add_medical_document(self, document_data, metadata):
        """Add medical document"""
        self.medical_docs.add(
            documents=[document_data],
            metadatas=[{
                **metadata,
                "record_type": "medical_document",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }],
            ids=[f"doc_{metadata.get('doc_type')}_{datetime.now().strftime('%Y%m%d%H%M%S')}"]
        )

    def add_chat_conversation(self, chat_data, metadata):
        """Add chat conversation"""
        self.chat_history.add(
            documents=[chat_data],
            metadatas=[{
                **metadata,
                "record_type": "chat",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }],
            ids=[f"chat_{metadata.get('session_id')}_{datetime.now().strftime('%Y%m%d%H%M%S')}"]
        )

    def search_patient_records(self, query_text, n_results=5):
        """Search patient records"""
        return self.patient_records.query(
            query_texts=[query_text],
            n_results=n_results
        )

    def search_medical_documents(self, query_text, n_results=5):
        """Search medical documents"""
        return self.medical_docs.query(
            query_texts=[query_text],
            n_results=n_results
        )

    def search_chat_history(self, query_text, n_results=5):
        """Search chat history"""
        return self.chat_history.query(
            query_texts=[query_text],
            n_results=n_results
        )

# Example usage:
if __name__ == "__main__":
    db = SwasthVedhaDB()

    # Example: Adding a patient record
    patient_record = {
        "patient_id": "P12345",
        "name": "John Doe",
        "age": 45,
        "condition": "Diabetes Type 2"
    }
    db.add_patient_record(
        patient_data=str(patient_record),
        metadata={
            "patient_id": "P12345",
            "department": "Endocrinology",
            "priority": "medium"
        }
    )

    # Example: Adding a medical document
    medical_doc = "Blood sugar levels: Fasting - 126 mg/dL, Post-meal - 185 mg/dL"
    db.add_medical_document(
        document_data=medical_doc,
        metadata={
            "doc_type": "lab_report",
            "patient_id": "P12345",
            "department": "Laboratory"
        }
    )

    # Example: Adding a chat conversation
    chat = "Doctor: How are you feeling today?\nPatient: My blood sugar has been higher than usual."
    db.add_chat_conversation(
        chat_data=chat,
        metadata={
            "session_id": "CHAT123",
            "patient_id": "P12345",
            "doctor_id": "D789"
        }
    )

    # Example: Searching
    print("\nSearching patient records:")
    results = db.search_patient_records("diabetes")
    print(results)

    print("\nSearching medical documents:")
    results = db.search_medical_documents("blood sugar")
    print(results)

    print("\nSearching chat history:")
    results = db.search_chat_history("feeling today")
    print(results)