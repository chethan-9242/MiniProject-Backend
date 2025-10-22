from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn
import json
from datetime import datetime
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

# Import our modules (we'll create these next)
from routers import dosha, symptoms, skin_disease, chatbot, recommendations, hair, auth
from routers import hair_rag, recommendations_rag  # RAG-enhanced routers
from routers import youtube_integration  # YouTube integration
from routers import rag_debug  # RAG debug endpoints
from routers import n8n_bridge  # n8n integration bridge
from config.model_config import validate_environment, get_model_config
from services.rag_service import initialize_rag_system
from sqlalchemy import text
from db import get_db
from fastapi import Depends

app = FastAPI(
    title="SwasthVedha API",
    description="AI-driven Ayurvedic Healthcare Assistant",
    version="1.0.0",
    docs_url="/",  # Serve Swagger UI at root
    redoc_url=None
)

# CORS configuration
# Defaults cover local dev and Firebase Hosting; you can add more via BACKEND_ALLOWED_ORIGINS (comma-separated)
_default_origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3001",
    "https://swasthvedha.web.app",
    "https://swasthvedha.firebaseapp.com",
]
_extra_origins_env = os.getenv("BACKEND_ALLOWED_ORIGINS", "")
_extra_origins = [o.strip() for o in _extra_origins_env.split(",") if o.strip()]
_allow_origins = _default_origins + _extra_origins

# Allow any ngrok HTTPS URL via regex to avoid code edits each time (development convenience)
_ngrok_regex = r"^https://[a-z0-9-]+\.ngrok-free\.app$"

app.add_middleware(
    CORSMiddleware,
    allow_origins=_allow_origins,
    allow_origin_regex=_ngrok_regex,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(dosha.router, prefix="/api/dosha", tags=["Dosha Classification"])
app.include_router(symptoms.router, prefix="/api/symptoms", tags=["Symptom Checker"])
app.include_router(skin_disease.router, prefix="/api/skin", tags=["Skin Disease Detection"])
app.include_router(hair.router, prefix="/api/hair", tags=["Hair & Scalp Disorders"])
app.include_router(chatbot.router, prefix="/api/chat", tags=["Healthcare Chatbot"])
app.include_router(recommendations.router, prefix="/api/recommendations", tags=["Personalized Recommendations"])
# RAG-enhanced routers with advanced AI capabilities
app.include_router(hair_rag.router, prefix="/api/hair-rag", tags=["Enhanced Hair Analysis (RAG)"])
app.include_router(recommendations_rag.router, prefix="/api/recommendations-rag", tags=["AI-Powered Recommendations (RAG)"])
app.include_router(youtube_integration.router, prefix="/api/youtube", tags=["YouTube Integration"])
app.include_router(rag_debug.router)
app.include_router(n8n_bridge.router)
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])

# Info endpoint (since Swagger UI is at "/")
@app.get("/info")
async def info():
    return {
        "message": "SwasthVedha API - AI-driven Ayurvedic Healthcare Assistant",
        "version": "1.0.0",
        "endpoints": {
            "dosha": "/api/dosha/classify",
            "symptoms": "/api/symptoms/check",
            "skin": "/api/skin/analyze",
            "hair": "/api/hair/analyze",
            "chat": "/api/chat/message",
            "recommendations": "/api/recommendations/generate",
            # RAG-enhanced endpoints with advanced AI
            "hair_enhanced": "/api/hair-rag/analyze-enhanced",
            "personalized_recommendations": "/api/recommendations-rag/personalized",
            "rag_status": "/api/hair-rag/rag-status"
        }
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "SwasthVedha API",
        "allowed_origins": _allow_origins,
    }

# Simple DB ping (verifies Postgres connection via SQLAlchemy)
@app.get("/db/ping")
async def db_ping(db=Depends(get_db)):
    try:
        val = db.execute(text("SELECT 1")).scalar_one()
        return {"db": "ok", "result": int(val)}
    except Exception as e:
        return {"db": "error", "error": str(e)}

# RAG system initialization endpoint
@app.get("/rag/initialize")
async def initialize_rag():
    """
    Initialize or check RAG system status
    """
    try:
        success = initialize_rag_system()
        return {
            "timestamp": datetime.now().isoformat(),
            "rag_initialized": success,
            "message": "RAG system initialized successfully" if success else "RAG system initialization failed"
        }
    except Exception as e:
        return {
            "timestamp": datetime.now().isoformat(),
            "rag_initialized": False,
            "error": str(e)
        }

# Configuration validation endpoint
@app.get("/config/validate")
async def validate_config():
    """
    Validate environment configuration and model setup
    """
    try:
        validation_result = validate_environment()
        config = get_model_config()
        
        return {
            "timestamp": datetime.now().isoformat(),
            "validation": validation_result,
            "model_config": {
                "model_name": config.flan_t5_model_name,
                "device": config.device,
                "max_length": config.flan_t5_max_length,
                "temperature": config.flan_t5_temperature,
                "use_cache": config.flan_t5_use_cache
            }
        }
    except Exception as e:
        return {
            "timestamp": datetime.now().isoformat(),
            "validation": {
                "valid": False,
                "errors": [str(e)]
            }
        }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
