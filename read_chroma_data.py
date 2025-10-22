import chromadb

def print_collection_info(collection):
    print(f"\nCollection Name: {collection.name}")
    print(f"Metadata: {collection.metadata}")
    
    # Get all documents
    results = collection.get()
    print("\nDocuments found:", len(results['ids']))
    
    for i in range(len(results['ids'])):
        print(f"\nDocument {i+1}:")
        print(f"ID: {results['ids'][i]}")
        print(f"Content: {results['documents'][i]}")
        if results['metadatas'][i]:
            print(f"Metadata: {results['metadatas'][i]}")
        print("-" * 50)

# Connect to your existing database
print("Connecting to database...")
client = chromadb.PersistentClient(
    path="C:/Users/Chethan/OneDrive/Desktop/SwasthVedha/backend/data/chroma_db"
)

# List all collections
print("\nListing all collections:")
collections = client.list_collections()
print(f"Found {len(collections)} collections")

# Print details for each collection
for collection in collections:
    print_collection_info(collection)

# You can also search for specific content
if collections:
    collection = collections[0]  # Use the first collection
    print("\nExample search:")
    search_results = collection.query(
        query_texts=["your search term here"],
        n_results=2
    )
    print("Search results:", search_results)