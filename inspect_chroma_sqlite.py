import sqlite3
from pathlib import Path
import os

def inspect_sqlite():
    print("\n🚀 SwasthVedha ChromaDB SQLite Inspector")
    print("=" * 40)
    
    chroma_path = Path("data/chroma_db/chroma.sqlite3")
    if not chroma_path.exists():
        print(f"❌ ChromaDB SQLite file not found at: {chroma_path}")
        return
        
    try:
        conn = sqlite3.connect(str(chroma_path))
        cursor = conn.cursor()
        
        # List all tables
        print("\n📊 Tables in ChromaDB:")
        print("-" * 30)
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        for table in tables:
            print(f"  • {table[0]}")
            
        # Inspect collections
        print("\n📚 Collections:")
        print("-" * 30)
        cursor.execute("SELECT * FROM collections;")
        collections = cursor.fetchall()
        for collection in collections:
            print(f"  • ID: {collection[0]}")
            print(f"    Name: {collection[1]}")
            print()
            
        # Inspect embeddings
        print("\n🔍 Embedding Search Data (First 5):")
        print("-" * 30)
        cursor.execute("PRAGMA table_info(embeddings);")
        embeddings = cursor.fetchall()
        for embedding in embeddings:
            print(f"  • Column: {embedding[1]}")
            print(f"    Type: {embedding[2]}")
            print()
            
        # Inspect metadata
        print("\n📋 Collection Metadata:")
        print("-" * 30)
        cursor.execute("""
            SELECT c.id, c.name, cm.key, cm.str_value 
            FROM collections c
            LEFT JOIN collection_metadata cm ON c.id = cm.collection_id;
        """)
        metadata = cursor.fetchall()
        for meta in metadata:
            print(f"  • Collection: {meta[1]}")
            print(f"    Key: {meta[2]}")
            print(f"    Value: {meta[3]}")
            print()
            
    except sqlite3.Error as e:
        print(f"❌ SQLite Error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    inspect_sqlite()