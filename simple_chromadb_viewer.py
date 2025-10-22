"""
Simple ChromaDB Viewer - Shows ChromaDB structure without complex dependencies
"""

import os
import sys
from pathlib import Path
import json

try:
    import chromadb
    from chromadb.config import Settings
    CHROMA_AVAILABLE = True
except ImportError:
    print("❌ ChromaDB not available")
    CHROMA_AVAILABLE = False

def show_chromadb_structure():
    """Show existing ChromaDB structure"""
    
    print("🔍 SwasthVedha ChromaDB Structure Viewer")
    print("=" * 45)
    
    if not CHROMA_AVAILABLE:
        print("❌ ChromaDB is not installed")
        return
    
    # Check ChromaDB path
    chroma_path = Path("./data/chroma_db")
    print(f"📁 ChromaDB Path: {chroma_path.absolute()}")
    
    if not chroma_path.exists():
        print("❌ ChromaDB directory not found")
        print("💡 ChromaDB hasn't been initialized yet")
        return
    
    try:
        # Connect to existing ChromaDB
        print("\n🔗 Connecting to ChromaDB...")
        client = chromadb.PersistentClient(
            path=str(chroma_path),
            settings=Settings(allow_reset=False, anonymized_telemetry=False)
        )
        
        # List collections
        collections = client.list_collections()
        print(f"📚 Found {len(collections)} collection(s):")
        
        if not collections:
            print("   No collections found - database is empty")
            show_expected_structure()
            return
        
        for collection in collections:
            print(f"\n   📖 Collection: '{collection.name}'")
            print(f"      ID: {collection.id}")
            
            # Get collection stats
            count = collection.count()
            print(f"      Documents: {count}")
            
            if count > 0:
                # Get a sample
                sample = collection.peek(limit=3)
                print(f"\n      📋 Sample Documents:")
                
                for i, (doc_id, document, metadata) in enumerate(zip(
                    sample['ids'][:3], 
                    sample['documents'][:3], 
                    sample['metadatas'][:3]
                ), 1):
                    print(f"\n      [{i}] ID: {doc_id}")
                    doc_preview = document[:80] + "..." if len(document) > 80 else document
                    print(f"          Content: {doc_preview}")
                    print(f"          Metadata: {metadata}")
        
        # Show file structure
        print(f"\n📁 Database Files:")
        for item in chroma_path.rglob("*"):
            if item.is_file():
                size_mb = item.stat().st_size / (1024 * 1024)
                print(f"   📄 {item.name} ({size_mb:.2f} MB)")
        
    except Exception as e:
        print(f"❌ Error accessing ChromaDB: {str(e)}")

def show_expected_structure():
    """Show what ChromaDB structure should look like"""
    print(f"\n💡 Expected ChromaDB Structure:")
    print("-" * 30)
    
    expected_structure = {
        "Collections": {
            "swasthvedha_knowledge": {
                "Purpose": "Medical and Ayurvedic knowledge storage",
                "Document Types": [
                    "Ayurvedic symptom conditions",
                    "Hair treatment knowledge", 
                    "General medical knowledge",
                    "Treatment protocols",
                    "Herbal medicine database"
                ],
                "Metadata Fields": [
                    "type: Document category",
                    "category: Medical category", 
                    "condition: Specific condition",
                    "dosha: Ayurvedic dosha involvement"
                ]
            }
        },
        "Vector Embeddings": {
            "Model": "all-MiniLM-L6-v2 (SentenceTransformers)",
            "Dimensions": "384",
            "Similarity": "Cosine similarity"
        },
        "Storage Files": {
            "chroma.sqlite3": "Main database file",
            "*.bin": "Vector storage files",
            "*.json": "Metadata files"
        }
    }
    
    def print_dict(d, indent=0):
        for key, value in d.items():
            if isinstance(value, dict):
                print("   " * indent + f"🔹 {key}:")
                print_dict(value, indent + 1)
            elif isinstance(value, list):
                print("   " * indent + f"🔹 {key}:")
                for item in value:
                    print("   " * (indent + 1) + f"• {item}")
            else:
                print("   " * indent + f"🔹 {key}: {value}")
    
    print_dict(expected_structure)

def show_knowledge_files():
    """Show available knowledge files"""
    print(f"\n📚 Knowledge Files for ChromaDB:")
    print("-" * 35)
    
    knowledge_files = {
        "Ayurvedic Symptoms": "data/ayurvedic_symptoms_knowledge.json",
        "Hair Conditions": "config/hair_config.json", 
        "General Ayurveda": "data/general_ayurvedic_knowledge.json"
    }
    
    total_size = 0
    for name, path in knowledge_files.items():
        file_path = Path(path)
        if file_path.exists():
            size_kb = file_path.stat().st_size / 1024
            total_size += size_kb
            print(f"   ✅ {name}")
            print(f"      📄 {path} ({size_kb:.1f} KB)")
        else:
            print(f"   ❌ {name}: {path}")
    
    print(f"\n📊 Total Knowledge: {total_size:.1f} KB")

def main():
    """Main viewer function"""
    show_knowledge_files()
    show_chromadb_structure()
    
    print(f"\n🎯 ChromaDB in SwasthVedha RAG System:")
    print("   🔹 Stores medical knowledge as searchable vectors")
    print("   🔹 Enables semantic search for AI context") 
    print("   🔹 Enhances Flan-T5 responses with relevant knowledge")
    print("   🔹 Supports all LLM components in the platform")
    
    print(f"\n💻 To initialize ChromaDB with knowledge:")
    print("   1. Install: py -m pip install sentence-transformers")
    print("   2. Run RAG service to populate database")
    print("   3. Database will be created automatically on first use")

if __name__ == "__main__":
    main()