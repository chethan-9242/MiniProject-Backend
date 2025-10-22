# SwasthVedha RAG System - UML Diagrams

## 1. Activity Diagram - RAG Workflow

```plantuml
@startuml RAG_Workflow
!theme plain
skinparam backgroundColor #f8f9fa
skinparam activityBorderColor #333
skinparam activityBackgroundColor #e3f2fd

title SwasthVedha RAG System Workflow

|Knowledge Processing|
start
:📖 Medical Knowledge Files\n(ayurvedic_symptoms_knowledge.json\nhair_config.json\ngeneral_ayurvedic_knowledge.json);
:Process into text chunks\n(500 chars, 50 overlap);
:🧮 Generate SentenceTransformer Embeddings\n(all-MiniLM-L6-v2 model);
:💾 Store in ChromaDB\n(384-dimensional vectors);

|User Interaction|
:👤 User Query\n"I have headache and fever";

|RAG Processing|
:🔍 Semantic Search in ChromaDB\n(Cosine similarity);
:Retrieve top 5 relevant chunks\n(similarity threshold: 0.3);
:📋 Enhance Flan-T5 Prompt\nwith retrieved context;
:🤖 Generate Flan-T5 Response\n(Medical analysis + Ayurvedic advice);
:📤 Return Enhanced Response\nto User;

stop

@enduml
```

## 2. Sequence Diagram - RAG Components Interaction

```plantuml
@startuml RAG_Sequence
!theme plain
skinparam backgroundColor #f8f9fa

title SwasthVedha RAG System - Component Interaction

participant "User" as U
participant "Flan-T5\nService" as F5
participant "RAG\nService" as RAG
participant "SentenceTransformer\nEmbeddings" as ST
participant "ChromaDB\nVector Store" as CDB
participant "Knowledge\nFiles" as KF

== Initialization Phase ==
F5 -> RAG : initialize_rag()
RAG -> ST : load_model("all-MiniLM-L6-v2")
RAG -> CDB : create_collection("swasthvedha_knowledge")
RAG -> KF : load_knowledge_files()
RAG -> ST : generate_embeddings(chunks)
RAG -> CDB : store_vectors(embeddings, metadata)

== Query Phase ==
U -> F5 : "I have headache and fever"
F5 -> RAG : retrieve_context(query)
RAG -> ST : encode_query(query)
RAG -> CDB : similarity_search(query_vector, k=5)
CDB -> RAG : relevant_chunks[]
RAG -> F5 : enhanced_context
F5 -> F5 : generate_response(query + context)
F5 -> U : "Based on symptoms... Ayurvedic analysis..."

@enduml
```

## 3. Component Diagram - System Architecture

```plantuml
@startuml RAG_Components
!theme plain
skinparam backgroundColor #f8f9fa

title SwasthVedha RAG System Architecture

package "SwasthVedha Backend" {
    
    component "Flan-T5 Service" as FlanT5 {
        port "generate_response" as gen
        port "initialize" as init
    }
    
    component "RAG Service" as RAGSvc {
        port "retrieve_context" as ret
        port "enhance_prompt" as enh
        port "load_knowledge" as load
    }
    
    component "Embedding Model" as Embed {
        interface "SentenceTransformer" as ST
        note right : all-MiniLM-L6-v2\n384 dimensions
    }
    
    component "Vector Database" as VectorDB {
        interface "ChromaDB" as CDB
        note right : Persistent storage\nCosine similarity\nSQLite backend
    }
    
    component "Knowledge Sources" as Knowledge {
        file "ayurvedic_symptoms_knowledge.json" as kb1
        file "hair_config.json" as kb2  
        file "general_ayurvedic_knowledge.json" as kb3
    }
    
    component "API Endpoints" as API {
        interface "REST" as rest
        note right : Symptoms analysis\nChatbot\nRecommendations
    }
}

' Connections
API::rest --> FlanT5::gen
FlanT5::init --> RAGSvc::load
FlanT5::gen --> RAGSvc::ret
RAGSvc::enh --> Embed::ST
RAGSvc::load --> VectorDB::CDB
RAGSvc::load --> Knowledge
Embed::ST --> VectorDB::CDB

@enduml
```

## 4. Class Diagram - RAG Service Structure

```plantuml
@startuml RAG_Classes
!theme plain
skinparam backgroundColor #f8f9fa

title SwasthVedha RAG System - Class Structure

class RAGService {
    - vector_store: ChromaDB
    - embedding_model: SentenceTransformer
    - knowledge_chunks: List[str]
    - chunk_metadata: List[Dict]
    - max_retrieval_chunks: int = 5
    - similarity_threshold: float = 0.3
    --
    + initialize_embedding_model(): bool
    + initialize_vector_store(): bool
    + load_knowledge_bases(): void
    + retrieve_relevant_knowledge(query: str): List[Dict]
    + enhance_prompt_with_context(prompt: str): str
    - _create_chunks(documents: List): Tuple
    - _populate_vector_store(): void
}

class FlanT5Service {
    - model: T5ForConditionalGeneration
    - tokenizer: T5Tokenizer
    - rag_service: RAGService
    - device: str
    --
    + generate_response(message: str, context: Dict): Dict
    + load_model(): bool
    + initialize_rag(): bool
    - _construct_prompt(message: str, context: Dict): str
}

class ChromaDBClient {
    - client: PersistentClient
    - collection: Collection
    - path: str = "./data/chroma_db"
    --
    + create_collection(name: str): Collection
    + add_documents(texts: List, embeddings: List): void
    + query(query_embeddings: List, n_results: int): Dict
    + count(): int
}

class SentenceTransformerModel {
    - model: SentenceTransformer
    - model_name: str = "all-MiniLM-L6-v2"
    - dimensions: int = 384
    --
    + encode(texts: List[str]): ndarray
    + encode_single(text: str): ndarray
}

' Relationships
RAGService "1" --> "1" ChromaDBClient : uses
RAGService "1" --> "1" SentenceTransformerModel : uses
FlanT5Service "1" --> "1" RAGService : uses
FlanT5Service "1" --> "1" RAGService : initializes

@enduml
```

## 5. Data Flow Diagram - RAG Processing

```plantuml
@startuml RAG_DataFlow
!theme plain
skinparam backgroundColor #f8f9fa

title SwasthVedha RAG System - Data Flow

(Medical Knowledge\nJSON Files) as KB
[Text Chunking\nProcessor] as CHUNK
[SentenceTransformer\nall-MiniLM-L6-v2] as ST
[ChromaDB\nVector Store] as CDB
[Similarity Search\nEngine] as SEARCH
[Prompt Enhancement\nModule] as ENHANCE
[Flan-T5 LLM\nGenerator] as LLM
(User Query) as USER
(Enhanced Response) as RESPONSE

KB --> CHUNK : Raw medical\nknowledge
CHUNK --> ST : Text chunks\n(500 chars)
ST --> CDB : 384-dim vectors\n+ metadata
USER --> SEARCH : User query\n"headache fever"
SEARCH --> CDB : Query vector
CDB --> SEARCH : Top 5 similar\ndocuments
SEARCH --> ENHANCE : Relevant medical\ncontext
ENHANCE --> LLM : Enhanced prompt\n+ context
LLM --> RESPONSE : Medical analysis +\nAyurvedic advice

note right of ST : Embedding Model\nProduces semantic\nvector representations
note right of CDB : Vector Database\nStores 384-dimensional\nembeddings with metadata
note right of SEARCH : Cosine Similarity\nFinds semantically\nsimilar content

@enduml
```

## 6. Deployment Diagram - System Architecture

```plantuml
@startuml RAG_Deployment
!theme plain
skinparam backgroundColor #f8f9fa

title SwasthVedha RAG System Deployment

node "SwasthVedha Server" {
    
    artifact "FastAPI Backend" as API {
        component "Symptom Analysis Router"
        component "Chatbot Router" 
        component "Recommendations Router"
    }
    
    artifact "AI Services" as AI {
        component "Flan-T5 Service" as F5
        component "RAG Service" as RAG
    }
    
    artifact "ML Models" as ML {
        file "all-MiniLM-L6-v2" as embed_model
        file "google/flan-t5-large" as llm_model
    }
    
    database "ChromaDB" as vectordb {
        file "chroma.sqlite3"
        folder "vector_files"
    }
    
    database "Knowledge Base" as kb {
        file "ayurvedic_symptoms_knowledge.json"
        file "hair_config.json"
        file "general_ayurvedic_knowledge.json"
    }
}

cloud "External Services" {
    interface "Hugging Face Hub" as HF
}

' Connections
API --> AI : HTTP calls
AI --> ML : Model loading
RAG --> vectordb : Vector operations
RAG --> kb : Knowledge loading
ML --> HF : Model download
F5 --> RAG : Context retrieval

note right of vectordb : Local persistent\nvector storage\n384-dimensional embeddings
note right of kb : Medical knowledge\n16.5 KB total\nJSON format

@enduml
```

## Usage Instructions

### To Generate Diagrams:

1. **PlantUML Online**: 
   - Copy any diagram code above
   - Paste into [plantuml.com/plantuml](http://www.plantuml.com/plantuml)
   - Generate PNG/SVG

2. **VS Code Extension**:
   - Install "PlantUML" extension
   - Create `.puml` files with the code
   - Preview diagrams directly

3. **Local PlantUML**:
   ```bash
   # Install PlantUML
   npm install -g plantuml
   
   # Generate diagram
   plantuml diagram.puml
   ```

### Diagram Types Provided:

1. **Activity Diagram** - Shows the step-by-step RAG workflow
2. **Sequence Diagram** - Shows component interactions over time
3. **Component Diagram** - Shows system architecture and relationships
4. **Class Diagram** - Shows object-oriented structure
5. **Data Flow Diagram** - Shows how data moves through the system
6. **Deployment Diagram** - Shows physical system deployment

Each diagram provides a different perspective on your RAG system for documentation, presentations, or development planning.