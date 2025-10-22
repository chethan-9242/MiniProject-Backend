"""
ChromaDB Inspector for SwasthVedha RAG System
Shows the structure and contents of the vector database
"""

import os
import sys
from pathlib import Path
import json
from typing import List, Dict, Any

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

try:
    from services.rag_service import get_rag_service
    RAG_AVAILABLE = True
except ImportError as e:
    print(f"❌ RAG service not available: {e}")
    RAG_AVAILABLE = False

try:
    import chromadb
    from chromadb.config import Settings
    CHROMA_AVAILABLE = True
except ImportError:
    print("❌ ChromaDB not available")
    CHROMA_AVAILABLE = False

def initialize_and_inspect_chromadb():
    """Initialize RAG service and inspect ChromaDB"""
    
    print("🔍 ChromaDB Inspector for SwasthVedha RAG System")
    print("=" * 60)
    
    if not CHROMA_AVAILABLE:
        print("❌ ChromaDB is not installed. Install with: pip install chromadb")
        return
    
    if not RAG_AVAILABLE:
        print("❌ RAG service not available")
        return
    
    try:
        # Initialize RAG service
        print("\n📊 Initializing RAG Service...")
        rag_service = get_rag_service()
        
        # Check if ChromaDB exists
        chroma_path = Path("./data/chroma_db")
        print(f"📁 ChromaDB Path: {chroma_path.absolute()}")
        
        if not chroma_path.exists():
            print("🔧 ChromaDB directory doesn't exist. Creating and initializing...")
            
            # Initialize the RAG service components
            rag_service.initialize_embedding_model()
            rag_service.initialize_vector_store()
            rag_service.load_knowledge_bases()
            
            print("✅ ChromaDB initialized successfully!")
        else:
            print("✅ ChromaDB directory found!")
        
        # Connect to ChromaDB
        print("\n🔗 Connecting to ChromaDB...")
        client = chromadb.PersistentClient(
            path=str(chroma_path),
            settings=Settings(allow_reset=False, anonymized_telemetry=False)
        )
        
        # List all collections
        collections = client.list_collections()
        print(f"📚 Found {len(collections)} collection(s):")
        
        for collection in collections:
            print(f"   • {collection.name} (ID: {collection.id})")
        
        # Inspect the main collection
        if collections:
            main_collection = collections[0]  # Usually 'swasthvedha_knowledge'
            
            print(f"\n🔬 Inspecting Collection: '{main_collection.name}'")
            print("-" * 40)
            
            # Get collection info
            count = main_collection.count()
            print(f"📊 Total Documents: {count}")
            
            if count > 0:
                # Get sample documents
                sample_size = min(5, count)
                results = main_collection.peek(limit=sample_size)
                
                print(f"\n📋 Sample Documents (showing {sample_size} of {count}):")
                print("-" * 40)
                
                for i, (doc_id, document, metadata) in enumerate(zip(
                    results['ids'], 
                    results['documents'], 
                    results['metadatas']
                ), 1):
                    print(f"\n[{i}] Document ID: {doc_id}")
                    print(f"    Content: {document[:100]}..." if len(document) > 100 else f"    Content: {document}")
                    print(f"    Metadata: {metadata}")
                
                # Show collection metadata
                print(f"\n⚙️ Collection Metadata:")
                collection_metadata = main_collection.metadata
                if collection_metadata:
                    for key, value in collection_metadata.items():
                        print(f"   {key}: {value}")
                else:
                    print("   No metadata available")
        
        # Test similarity search
        if collections and collections[0].count() > 0:
            print(f"\n🔍 Testing Similarity Search:")
            print("-" * 30)
            
            test_queries = [
                "headache and fever symptoms",
                "hair loss treatment",
                "vata dosha imbalance",
                "ayurvedic medicine for digestion"
            ]
            
            collection = collections[0]
            
            for query in test_queries:
                try:
                    results = collection.query(
                        query_texts=[query],
                        n_results=3
                    )
                    
                    print(f"\n🔎 Query: '{query}'")
                    print(f"   Found {len(results['documents'][0])} results:")
                    
                    for i, (doc, distance) in enumerate(zip(
                        results['documents'][0], 
                        results['distances'][0]
                    ), 1):
                        similarity_score = 1 - distance  # Convert distance to similarity
                        print(f"   [{i}] Score: {similarity_score:.3f} | {doc[:80]}...")
                        
                except Exception as e:
                    print(f"   ❌ Search failed: {str(e)}")
        
        # Show database file structure
        print(f"\n📁 ChromaDB File Structure:")
        print("-" * 30)
        
        if chroma_path.exists():
            for item in chroma_path.rglob("*"):
                if item.is_file():
                    size_mb = item.stat().st_size / (1024 * 1024)
                    print(f"   📄 {item.relative_to(chroma_path)} ({size_mb:.2f} MB)")
        
        # Performance info
        print(f"\n⚡ Performance Information:")
        print("-" * 25)
        print(f"   Embedding Model: all-MiniLM-L6-v2 (SentenceTransformers)")
        print(f"   Vector Dimensions: 384 (typical for all-MiniLM-L6-v2)")
        print(f"   Similarity Metric: Cosine similarity")
        print(f"   Storage Type: Persistent (SQLite + files)")
        
        print(f"\n✅ ChromaDB Inspection Complete!")
        
    except Exception as e:
        print(f"❌ Error inspecting ChromaDB: {str(e)}")
        import traceback
        traceback.print_exc()

def show_knowledge_sources():
    """Show what knowledge sources are available"""
    print(f"\n📚 Available Knowledge Sources:")
    print("-" * 35)
    
    knowledge_files = {
        "Ayurvedic Symptoms": "data/ayurvedic_symptoms_knowledge.json",
        "Hair Conditions": "config/hair_config.json", 
        "General Ayurveda": "data/general_ayurvedic_knowledge.json",
        "Treatment Protocols": "data/treatment_protocols.json",
        "Herb Database": "data/herb_database.json"
    }
    
    for name, path in knowledge_files.items():
        file_path = Path(path)
        if file_path.exists():
            size_kb = file_path.stat().st_size / 1024
            print(f"   ✅ {name}: {path} ({size_kb:.1f} KB)")
        else:
            print(f"   ❌ {name}: {path} (Not found)")

def main():
    """Main inspection function"""
    print("🚀 SwasthVedha ChromaDB Inspector")
    print("=" * 40)
    
    # Show knowledge sources first
    show_knowledge_sources()
    
    # Initialize and inspect ChromaDB
    initialize_and_inspect_chromadb()
    
    print(f"\n💡 ChromaDB Usage in SwasthVedha:")
    print("   • Enhances Flan-T5 responses with relevant knowledge")
    print("   • Stores medical and Ayurvedic knowledge as vectors")
    print("   • Enables semantic search for context-aware AI")
    print("   • Supports all LLM components (chatbot, analysis, recommendations)")

if __name__ == "__main__":
    main()