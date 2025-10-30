from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from pathlib import Path
import json

router = APIRouter()

# Initialize ChromaDB
chroma_client = None
collection = None
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
tokenizer = None
model = None

# Ayurvedic Knowledge Base - Core concepts and treatments
AYURVEDA_KNOWLEDGE = [
    {
        "id": "dosha_vata",
        "category": "Doshas",
        "title": "Vata Dosha Characteristics",
        "content": "Vata is composed of Air and Space elements. It governs movement, circulation, breathing, and nerve impulses. People with Vata dominance tend to be thin, energetic, creative, and quick-thinking but may experience anxiety, dry skin, constipation, and irregular digestion when imbalanced. Vata is cold, dry, light, and mobile in nature.",
        "metadata": {"dosha": "vata", "type": "constitution"}
    },
    {
        "id": "dosha_pitta",
        "category": "Doshas",
        "title": "Pitta Dosha Characteristics",
        "content": "Pitta is composed of Fire and Water elements. It governs digestion, metabolism, body temperature, and transformation. People with Pitta dominance tend to have medium build, strong digestion, sharp intellect, and leadership qualities but may experience inflammation, anger, heartburn, and skin issues when imbalanced. Pitta is hot, sharp, light, and spreading in nature.",
        "metadata": {"dosha": "pitta", "type": "constitution"}
    },
    {
        "id": "dosha_kapha",
        "category": "Doshas",
        "title": "Kapha Dosha Characteristics",
        "content": "Kapha is composed of Water and Earth elements. It governs structure, lubrication, immunity, and stability. People with Kapha dominance tend to have larger build, strong stamina, calm temperament, and good memory but may experience weight gain, lethargy, congestion, and slow metabolism when imbalanced. Kapha is cold, wet, heavy, and stable in nature.",
        "metadata": {"dosha": "kapha", "type": "constitution"}
    },
    {
        "id": "herb_ashwagandha",
        "category": "Herbs",
        "title": "Ashwagandha (Withania somnifera)",
        "content": "Ashwagandha is a powerful adaptogenic herb used in Ayurveda for over 3000 years. It reduces stress and anxiety, improves sleep quality, enhances cognitive function, and boosts immunity. It balances Vata and Kapha doshas and is particularly beneficial for nervous system health, reproductive health, and building strength. Typical dosage is 300-500mg of extract twice daily.",
        "metadata": {"type": "herb", "properties": "adaptogen, rejuvenative"}
    },
    {
        "id": "herb_turmeric",
        "category": "Herbs",
        "title": "Turmeric (Curcuma longa)",
        "content": "Turmeric is a golden spice with powerful anti-inflammatory and antioxidant properties. It contains curcumin, which supports liver function, joint health, and digestive health. Turmeric balances all three doshas and is used for skin conditions, wound healing, and reducing inflammation. Best absorbed with black pepper and healthy fats. Typical dosage is 500-1000mg daily.",
        "metadata": {"type": "herb", "properties": "anti-inflammatory, antioxidant"}
    },
    {
        "id": "herb_triphala",
        "category": "Herbs",
        "title": "Triphala (Three Fruits)",
        "content": "Triphala is a combination of three fruits: Amalaki, Bibhitaki, and Haritaki. It is a gentle detoxifier that supports digestive health, regularity, and colon cleansing. Triphala balances all three doshas, supports healthy elimination, improves nutrient absorption, and acts as an antioxidant. Typical dosage is 500-1000mg before bed or upon waking.",
        "metadata": {"type": "herb", "properties": "digestive, detoxifying"}
    },
    {
        "id": "treatment_skin_pitta",
        "category": "Treatments",
        "title": "Ayurvedic Treatment for Pitta Skin Conditions",
        "content": "Pitta-type skin conditions include rashes, acne, inflammation, and sensitivity. Treatment includes cooling herbs like neem, sandalwood, and aloe vera. Avoid hot, spicy, and acidic foods. Use coconut oil for massage. Include cooling foods like cucumber, mint, and coriander. Practice stress management and avoid excessive heat and sun exposure.",
        "metadata": {"dosha": "pitta", "condition": "skin", "type": "treatment"}
    },
    {
        "id": "treatment_digestion_vata",
        "category": "Treatments",
        "title": "Ayurvedic Treatment for Vata Digestive Issues",
        "content": "Vata digestive imbalances include gas, bloating, constipation, and irregular appetite. Treatment includes warm, cooked, easily digestible foods with healthy fats. Use digestive spices like ginger, cumin, fennel, and ajwain. Establish regular meal times. Practice oil massage (abhyanga) and include ghee in diet. Avoid cold, raw, and dry foods.",
        "metadata": {"dosha": "vata", "condition": "digestion", "type": "treatment"}
    },
    {
        "id": "treatment_weight_kapha",
        "category": "Treatments",
        "title": "Ayurvedic Treatment for Kapha Weight Management",
        "content": "Kapha imbalance often leads to weight gain and slow metabolism. Treatment includes light, warm, spicy foods. Exercise regularly, especially cardio and vigorous activities. Use metabolism-boosting spices like ginger, black pepper, and cinnamon. Avoid heavy, oily, sweet, and cold foods. Practice intermittent fasting and wake up early (before 6 AM).",
        "metadata": {"dosha": "kapha", "condition": "weight", "type": "treatment"}
    },
    {
        "id": "diet_vata_balancing",
        "category": "Diet",
        "title": "Vata-Balancing Diet Guidelines",
        "content": "To balance Vata, favor warm, moist, grounding foods. Include cooked grains like rice and oats, root vegetables, nuts, seeds, ghee, and warm milk. Use sweet, sour, and salty tastes. Avoid raw vegetables, cold foods, dry foods, and excessive beans. Eat regular meals at consistent times. Include warming spices like ginger, cinnamon, and cardamom.",
        "metadata": {"dosha": "vata", "type": "diet"}
    },
    {
        "id": "diet_pitta_balancing",
        "category": "Diet",
        "title": "Pitta-Balancing Diet Guidelines",
        "content": "To balance Pitta, favor cool, refreshing, mildly spiced foods. Include sweet fruits, leafy greens, cucumber, coconut, milk, and ghee. Use sweet, bitter, and astringent tastes. Avoid hot, spicy, fried, and acidic foods. Reduce coffee, alcohol, and red meat. Include cooling spices like coriander, fennel, and cardamom.",
        "metadata": {"dosha": "pitta", "type": "diet"}
    },
    {
        "id": "diet_kapha_balancing",
        "category": "Diet",
        "title": "Kapha-Balancing Diet Guidelines",
        "content": "To balance Kapha, favor light, warm, stimulating foods. Include plenty of vegetables, legumes, light grains like quinoa and barley. Use pungent, bitter, and astringent tastes. Avoid heavy, oily, sweet, and cold foods. Reduce dairy, wheat, and sweet fruits. Include metabolism-boosting spices like ginger, black pepper, turmeric, and cayenne.",
        "metadata": {"dosha": "kapha", "type": "diet"}
    },
    {
        "id": "lifestyle_dinacharya",
        "category": "Lifestyle",
        "title": "Dinacharya - Daily Ayurvedic Routine",
        "content": "Dinacharya is the Ayurvedic daily routine for optimal health. Wake before sunrise (6 AM), eliminate waste, scrape tongue, oil pulling, abhyanga (self-massage), yoga/exercise, meditation, eat largest meal at midday, avoid late-night meals, sleep by 10 PM. This routine aligns with natural circadian rhythms and balances all doshas.",
        "metadata": {"type": "lifestyle", "practice": "daily_routine"}
    },
    {
        "id": "practice_abhyanga",
        "category": "Practices",
        "title": "Abhyanga - Ayurvedic Oil Massage",
        "content": "Abhyanga is daily self-massage with warm oil. Use sesame oil for Vata, coconut oil for Pitta, and mustard or sunflower oil for Kapha. Massage in long strokes on limbs and circular motions on joints. Practice before bathing, ideally in the morning. Benefits include improved circulation, lymphatic drainage, nervous system calming, and skin nourishment.",
        "metadata": {"type": "practice", "name": "oil_massage"}
    },
    {
        "id": "season_winter",
        "category": "Seasonal",
        "title": "Winter Season (Hemanta & Shishira Ritu)",
        "content": "Winter aggravates Vata and sometimes Kapha. Favor warming, nourishing, heavier foods. Increase healthy fats like ghee and sesame oil. Use warming spices. Practice oil massage daily. Avoid cold foods and drinks. Stay warm and moisturize skin regularly. Build immunity with Chyawanprash and warm herbal teas.",
        "metadata": {"season": "winter", "type": "seasonal_guidance"}
    },
    {
        "id": "season_summer",
        "category": "Seasonal",
        "title": "Summer Season (Grishma Ritu)",
        "content": "Summer aggravates Pitta dosha. Favor cooling, hydrating foods. Include sweet fruits, coconut water, mint, cilantro. Avoid hot, spicy, fried foods. Stay hydrated. Practice cooling pranayama like Shitali. Wear light-colored, breathable clothing. Avoid excessive sun exposure and intense exercise during peak heat.",
        "metadata": {"season": "summer", "type": "seasonal_guidance"}
    },
    {
        "id": "mind_sattva",
        "category": "Mind",
        "title": "Sattva - Mental Purity and Clarity",
        "content": "Sattva represents purity, clarity, harmony, and balance in the mind. Sattvic qualities include compassion, contentment, peace, and wisdom. Cultivate Sattva through meditation, positive company, pure foods, spiritual practices, and selfless service. Sattvic foods include fresh fruits, vegetables, whole grains, nuts, and pure water.",
        "metadata": {"type": "mental_quality", "guna": "sattva"}
    },
    {
        "id": "agni_digestive_fire",
        "category": "Concepts",
        "title": "Agni - Digestive Fire",
        "content": "Agni is the digestive fire that transforms food into energy and consciousness. Strong Agni leads to good health, clear mind, and strong immunity. Weak Agni causes ama (toxins), disease, and fatigue. Support Agni by eating at regular times, avoiding overeating, using digestive spices, and not drinking excess water during meals.",
        "metadata": {"type": "concept", "importance": "fundamental"}
    },
    {
        "id": "ama_toxins",
        "category": "Concepts",
        "title": "Ama - Toxic Accumulation",
        "content": "Ama is undigested food matter and metabolic waste that accumulates in the body. It causes disease, fatigue, heaviness, and cloudy thinking. Signs include coated tongue, bad breath, sluggishness. Remove Ama through fasting, light diet, spices like ginger and turmeric, hot water sipping, and detoxification practices like Panchakarma.",
        "metadata": {"type": "concept", "importance": "pathology"}
    },
    {
        "id": "pranayama_breathing",
        "category": "Practices",
        "title": "Pranayama - Breath Control",
        "content": "Pranayama is yogic breathing practice that balances prana (life force) and doshas. Nadi Shodhana (alternate nostril) balances Vata, Shitali (cooling breath) reduces Pitta, Kapalabhati (skull shining breath) reduces Kapha. Practice in morning on empty stomach. Benefits include stress reduction, mental clarity, and improved lung capacity.",
        "metadata": {"type": "practice", "name": "breathing"}
    }
]

def initialize_chromadb():
    """Initialize ChromaDB with Ayurvedic knowledge base"""
    global chroma_client, collection, tokenizer, model
    
    try:
        print("🔍 Initializing ChromaDB for GraphRAG...")
        
        # Initialize ChromaDB client
        chroma_client = chromadb.Client(Settings(
            persist_directory="./chroma_db",
            anonymized_telemetry=False
        ))
        
        # Create or get collection
        try:
            collection = chroma_client.get_collection(name="ayurveda_knowledge")
            print(f"   Found existing collection with {collection.count()} documents")
        except:
            # Use default embedding function (all-MiniLM-L6-v2)
            embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name="all-MiniLM-L6-v2"
            )
            
            collection = chroma_client.create_collection(
                name="ayurveda_knowledge",
                embedding_function=embedding_function,
                metadata={"description": "Ayurvedic knowledge base for RAG"}
            )
            
            # Add documents to collection
            collection.add(
                documents=[doc["content"] for doc in AYURVEDA_KNOWLEDGE],
                metadatas=[doc["metadata"] for doc in AYURVEDA_KNOWLEDGE],
                ids=[doc["id"] for doc in AYURVEDA_KNOWLEDGE]
            )
            
            print(f"   Created new collection with {len(AYURVEDA_KNOWLEDGE)} documents")
        
        # Load Flan-T5 for generation (reuse if already loaded)
        if tokenizer is None:
            print("   Loading Flan-T5 model for generation...")
            model_name = "google/flan-t5-small"
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            model = model.to(device)
            model.eval()
        
        print("✅ GraphRAG initialized successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error initializing GraphRAG: {e}")
        return False

# Initialize on startup
RAG_LOADED = initialize_chromadb()

class QueryRequest(BaseModel):
    query: str
    context_type: Optional[str] = None  # dosha, herb, treatment, diet, etc.
    max_results: int = 5

class RAGResponse(BaseModel):
    answer: str
    sources: List[Dict]
    confidence: float

@router.post("/query", response_model=RAGResponse)
async def query_knowledge_base(request: QueryRequest):
    """Query the Ayurvedic knowledge base using GraphRAG"""
    
    if not RAG_LOADED:
        raise HTTPException(status_code=503, detail="GraphRAG not initialized")
    
    try:
        # Retrieve relevant documents from ChromaDB
        results = collection.query(
            query_texts=[request.query],
            n_results=request.max_results,
            where={"type": request.context_type} if request.context_type else None
        )
        
        # Extract documents and metadata
        documents = results['documents'][0] if results['documents'] else []
        metadatas = results['metadatas'][0] if results['metadatas'] else []
        distances = results['distances'][0] if results['distances'] else []
        
        if not documents:
            return RAGResponse(
                answer="I don't have enough information to answer that question. Please try asking about doshas, herbs, treatments, or diet.",
                sources=[],
                confidence=0.0
            )
        
        # Build context from retrieved documents
        context = "\n\n".join([f"Source {i+1}: {doc}" for i, doc in enumerate(documents)])
        
        # Generate answer using Flan-T5 with context
        prompt = f"""Based on the following Ayurvedic knowledge, answer the question concisely and accurately.

Context:
{context}

Question: {request.query}

Answer:"""
        
        inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True).to(device)
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_length=250,
                min_length=30,
                num_beams=5,
                early_stopping=True,
                temperature=0.8,
                do_sample=True,
                top_k=50,
                top_p=0.95,
                repetition_penalty=1.2,
                no_repeat_ngram_size=3
            )
        
        answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Calculate confidence based on retrieval distances
        avg_distance = sum(distances) / len(distances) if distances else 1.0
        confidence = max(0.0, min(1.0, 1.0 - avg_distance))
        
        # Prepare sources
        sources = [
            {
                "content": doc[:200] + "...",  # Truncate for response
                "metadata": meta,
                "relevance": 1.0 - dist
            }
            for doc, meta, dist in zip(documents, metadatas, distances)
        ]
        
        return RAGResponse(
            answer=answer,
            sources=sources,
            confidence=round(confidence, 2)
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error querying knowledge base: {str(e)}")

@router.get("/knowledge/categories")
async def get_categories():
    """Get all knowledge categories"""
    
    if not RAG_LOADED:
        raise HTTPException(status_code=503, detail="GraphRAG not initialized")
    
    categories = list(set(doc["category"] for doc in AYURVEDA_KNOWLEDGE))
    
    return {
        "categories": sorted(categories),
        "total_documents": len(AYURVEDA_KNOWLEDGE),
        "collection_size": collection.count() if collection else 0
    }

@router.post("/knowledge/search")
async def semantic_search(request: QueryRequest):
    """Perform semantic search without generation"""
    
    if not RAG_LOADED:
        raise HTTPException(status_code=503, detail="GraphRAG not initialized")
    
    try:
        results = collection.query(
            query_texts=[request.query],
            n_results=request.max_results
        )
        
        documents = results['documents'][0] if results['documents'] else []
        metadatas = results['metadatas'][0] if results['metadatas'] else []
        distances = results['distances'][0] if results['distances'] else []
        ids = results['ids'][0] if results['ids'] else []
        
        search_results = [
            {
                "id": id_,
                "content": doc,
                "metadata": meta,
                "relevance_score": round(1.0 - dist, 3)
            }
            for id_, doc, meta, dist in zip(ids, documents, metadatas, distances)
        ]
        
        return {
            "query": request.query,
            "results": search_results,
            "total": len(search_results)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error performing search: {str(e)}")

@router.get("/health")
async def health_check():
    """Check GraphRAG system health"""
    return {
        "status": "healthy" if RAG_LOADED else "error",
        "rag_loaded": RAG_LOADED,
        "collection_size": collection.count() if collection and RAG_LOADED else 0,
        "embedding_model": "all-MiniLM-L6-v2",
        "generation_model": "google/flan-t5-small"
    }
