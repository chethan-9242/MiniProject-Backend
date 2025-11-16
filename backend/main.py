import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import skin_disease, hair_disease, youtube, dosha, graph_rag, symptoms
from blockchain_integration import router as blockchain_router

app = FastAPI(
    title="SwasthVedha API",
    description="AI-powered Ayurvedic Healthcare Platform with Blockchain Integration",
    version="2.1.0"
)

# CORS configuration (from env or defaults)
origins_env = os.getenv("BACKEND_ALLOWED_ORIGINS")
origins = [o.strip() for o in origins_env.split(",")] if origins_env else [
    "http://localhost:3000",
    "http://localhost:3001",
    "https://swasthvedha.web.app",
    "https://swasthvedha.firebaseapp.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "SwasthVedha API v2.1.0 - with Blockchain Integration",
        "status": "running",
        "features": ["AI Diagnosis", "Ayurvedic Recommendations", "Blockchain Medical Records", "IPFS Storage"],
        "endpoints": {
            "health": "/health",
            "blockchain_health": "/api/blockchain/health",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "2.1.0",
        "message": "Backend is running with blockchain integration.",
        "blockchain_enabled": True
    }

# Include routers
app.include_router(skin_disease.router, prefix="/api/skin", tags=["Skin Disease Detection"])
app.include_router(hair_disease.router, prefix="/api/hair", tags=["Hair Disease Detection"])
app.include_router(youtube.router, prefix="/api/youtube", tags=["YouTube Videos"])
app.include_router(dosha.router, prefix="/api/dosha", tags=["Dosha Classification"])
app.include_router(graph_rag.router, prefix="/api/rag", tags=["GraphRAG Knowledge Base"])
app.include_router(symptoms.router, prefix="/api/symptoms", tags=["Symptom Checker"])
app.include_router(blockchain_router, prefix="/api/blockchain", tags=["Blockchain & IPFS"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
