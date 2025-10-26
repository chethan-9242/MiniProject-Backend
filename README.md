# 🩺 SwasthVedha Backend - AI-Powered Ayurvedic Healthcare Platform

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.6+-red.svg)](https://pytorch.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **An intelligent AI-driven healthcare platform that combines traditional Ayurvedic knowledge with cutting-edge machine learning technology.**

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [API Documentation](#api-documentation)
- [Machine Learning Models](#machine-learning-models)
- [RAG System](#rag-system)
- [Deployment](#deployment)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## 🌟 Overview

SwasthVedha is a sophisticated AI-powered healthcare platform that bridges traditional Ayurvedic medicine with modern artificial intelligence. The system provides intelligent health consultations, visual health analysis, and personalized recommendations based on ancient wisdom enhanced by cutting-edge technology.

### Key Capabilities

- 🤖 **AI-Powered Consultations**: Google Flan-T5 Large (780M parameters) for intelligent health conversations
- 🖼️ **Visual Health Analysis**: CNN models for hair and skin condition detection
- 🧠 **RAG-Enhanced Intelligence**: Retrieval-Augmented Generation for context-aware responses
- 🧘 **Ayurvedic Integration**: Dosha analysis and traditional medicine recommendations
- 🚨 **Emergency Detection**: Intelligent triage and emergency symptom recognition
- 📊 **Comprehensive Analytics**: Detailed health insights and personalized guidance

## ✨ Features

### Core Healthcare Features

- **Symptom Analysis**: Multi-method health assessment with emergency detection
- **Dosha Classification**: Vata, Pitta, Kapha constitution analysis
- **Hair Disease Detection**: ResNet50-based visual analysis
- **Skin Condition Analysis**: CNN models for dermatological assessment
- **Personalized Recommendations**: AI-driven lifestyle and treatment guidance
- **Health Chatbot**: Intelligent conversational AI for health queries

### Advanced AI Features

- **RAG System**: ChromaDB + SentenceTransformers for knowledge retrieval
- **Multi-Modal Analysis**: Text, image, and symptom integration
- **Context-Aware Responses**: Dynamic knowledge base enhancement
- **Fallback Mechanisms**: TF-IDF backup when vector store unavailable
- **Real-time Processing**: Fast inference with optimized models

### Technical Features

- **Production-Ready**: Comprehensive deployment configurations
- **Health Monitoring**: Built-in health checks and status endpoints
- **Scalable Architecture**: Modular, maintainable codebase
- **Multi-Platform Support**: Docker, Vercel, Railway, Heroku deployment
- **Comprehensive Logging**: Detailed system monitoring and debugging

## 🏗️ Architecture

### System Overview

```
SwasthVedha Backend
├── 🚀 FastAPI Application (main.py)
├── 🧠 AI Services Layer
│   ├── Google Flan-T5 Large (780M parameters)
│   ├── RAG System (ChromaDB + Embeddings)
│   └── Computer Vision Models (ResNet50, CNN)
├── 🗄️ Database Layer
│   ├── PostgreSQL (Primary)
│   ├── ChromaDB (Vector Store)
│   └── Redis (Caching)
├── 📊 Knowledge Base
│   ├── Ayurvedic Symptoms Database
│   ├── Hair Conditions Knowledge
│   └── General Ayurvedic Knowledge
└── 🔧 Configuration & Deployment
    ├── Multi-platform Deployment
    ├── Environment Management
    └── Health Monitoring
```

### Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend Framework** | FastAPI 0.104+ | High-performance API server |
| **AI Language Model** | Google Flan-T5 Large | Intelligent health conversations |
| **Computer Vision** | PyTorch 2.6+, ResNet50 | Visual health analysis |
| **Vector Database** | ChromaDB | RAG knowledge retrieval |
| **Relational Database** | PostgreSQL | Primary data storage |
| **Caching** | Redis | Session and performance optimization |
| **Embeddings** | SentenceTransformers | Semantic search capabilities |
| **Deployment** | Docker, Vercel, Railway | Multi-platform deployment |

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- PostgreSQL database
- 8GB+ RAM (for AI models)
- CUDA-compatible GPU (optional, for faster inference)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/swasthvedha-backend.git
   cd swasthvedha-backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Initialize the database**
   ```bash
   # Set up PostgreSQL database
   # Update DATABASE_URL in .env file
   ```

6. **Start the server**
   ```bash
   python main.py
   ```

The API will be available at `http://localhost:8000`

### Quick Test

```bash
# Health check
curl http://localhost:8000/health

# Test AI chatbot
curl -X POST "http://localhost:8000/api/chat/message" \
  -H "Content-Type: application/json" \
  -d '{"message": "I have a headache and fever"}'
```

## 📚 API Documentation

### Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | System health check |
| `/db/ping` | GET | Database connectivity test |
| `/rag/initialize` | GET | Initialize RAG system |
| `/config/validate` | GET | Validate configuration |

### Healthcare Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/chat/message` | POST | AI health chatbot |
| `/api/symptoms/check` | POST | Symptom analysis |
| `/api/dosha/classify` | POST | Dosha constitution analysis |
| `/api/hair/analyze` | POST | Hair condition detection |
| `/api/skin/analyze` | POST | Skin condition analysis |
| `/api/recommendations/generate` | POST | Personalized recommendations |

### RAG-Enhanced Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/hair-rag/analyze-enhanced` | POST | RAG-enhanced hair analysis |
| `/api/recommendations-rag/personalized` | POST | AI-powered recommendations |
| `/api/hair-rag/rag-status` | GET | RAG system status |

### Example API Usage

#### Symptom Analysis
```python
import requests

response = requests.post("http://localhost:8000/api/symptoms/check", json={
    "symptoms": [
        {"name": "headache", "severity": "moderate", "duration": "2 days"},
        {"name": "fever", "severity": "mild", "duration": "1 day"}
    ],
    "patient_context": {"age": 30, "gender": "unspecified"}
})

print(response.json())
```

#### Hair Analysis
```python
import requests

# Upload image file
with open("hair_image.jpg", "rb") as f:
    files = {"file": f}
    data = {"symptoms": "itching, dandruff"}
    
    response = requests.post(
        "http://localhost:8000/api/hair/analyze",
        files=files,
        data=data
    )

print(response.json())
```

## 🤖 Machine Learning Models

### Current Model Status

| Model | Type | Status | Accuracy | Purpose |
|-------|------|--------|----------|---------|
| **Google Flan-T5 Large** | Language Model | ✅ Active | High Quality | Health conversations |
| **Skin Disease CNN** | Computer Vision | ✅ Active | 85-90% | Skin condition detection |
| **Hair Disease ResNet50** | Computer Vision | ⚠️ Needs Training | Not Trained | Hair condition analysis |
| **Symptom Analysis** | ML Classifier | ✅ Active | 15.7% | Symptom assessment |
| **RAG System** | Vector Search | ✅ Active | 85-90% | Knowledge retrieval |

### Model Training

#### Hair Disease Classification
```bash
# Train ResNet50 model
python train_hair_resnet50.py

# Analyze dataset
python analyze_hair_dataset.py
```

#### Skin Disease Detection
```bash
# Use Jupyter notebook for training
jupyter notebook Skin_Disease_CNN_Optimized_Colab.ipynb
```

### Model Performance Testing
```bash
# Test Flan-T5 accuracy
python test_flan_t5_accuracy.py

# Test symptoms analysis
python test_symptoms_analysis.py
```

## 🧠 RAG System

### Overview

The Retrieval-Augmented Generation (RAG) system enhances all AI responses with relevant medical knowledge:

- **Vector Database**: ChromaDB with persistent storage
- **Embeddings**: SentenceTransformers (all-MiniLM-L6-v2)
- **Knowledge Base**: JSON-structured Ayurvedic knowledge
- **Fallback**: TF-IDF when vector store unavailable

### Knowledge Sources

- **Ayurvedic Symptoms**: `data/ayurvedic_symptoms_knowledge.json`
- **Hair Conditions**: `config/hair_config.json`
- **General Ayurveda**: `data/general_ayurvedic_knowledge.json`
- **Treatment Protocols**: `data/treatment_protocols.json`

### RAG Inspection Tools

```bash
# Inspect ChromaDB
python inspect_chromadb.py

# Inspect RAG system
python inspect_rag.py

# Add data to ChromaDB
python add_data_to_chroma.py
```

## 🚀 Deployment

### Docker Deployment

```bash
# Build Docker image
docker build -t swasthvedha-backend .

# Run container
docker run -p 8000:8000 swasthvedha-backend
```

### Platform-Specific Deployment

#### Vercel
```bash
# Deploy to Vercel
vercel --prod
```

#### Railway
```bash
# Deploy to Railway
railway deploy
```

#### Heroku
```bash
# Deploy to Heroku
git push heroku main
```

### Environment Variables

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/swasthvedha
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=swasthvedha

# AI Models
FLAN_T5_MODEL_NAME=google/flan-t5-large
FLAN_T5_DEVICE=auto
FLAN_T5_MAX_LENGTH=512
FLAN_T5_TEMPERATURE=0.7

# RAG System
RAG_CHUNK_SIZE=500
RAG_MAX_CHUNKS=5
RAG_SIMILARITY_THRESHOLD=0.3

# Security
SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
```

## ⚙️ Configuration

### Model Configuration

The system uses environment-driven configuration for AI models:

```python
# config/model_config.py
class ModelConfig:
    flan_t5_model_name: str = "google/flan-t5-large"
    device: str = "auto"
    max_length: int = 512
    temperature: float = 0.7
    use_cache: bool = True
```

### Database Configuration

```python
# db.py
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)
```

## 📊 Performance Monitoring

### Health Endpoints

- `/health` - Overall system health
- `/db/ping` - Database connectivity
- `/rag/initialize` - RAG system status
- `/config/validate` - Configuration validation

### Logging

The system provides comprehensive logging:

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('swasthvedha.log'),
        logging.StreamHandler()
    ]
)
```

## 🔧 Development

### Project Structure

```
swasthvedha-backend/
├── main.py                 # FastAPI application
├── db.py                   # Database configuration
├── swasthvedha_db.py       # ChromaDB setup
├── requirements.txt        # Dependencies
├── Dockerfile             # Container configuration
├── routers/               # API route handlers (to be created)
├── services/              # Business logic layer (to be created)
├── config/                # Configuration management (to be created)
├── models/                # AI model storage
├── data/                  # Knowledge base
└── scripts/               # Training & utilities
```

### Adding New Features

1. **Create router**: Add new endpoint in `routers/`
2. **Implement service**: Add business logic in `services/`
3. **Update main.py**: Include new router
4. **Add tests**: Create test cases
5. **Update docs**: Document new features

### Testing

```bash
# Run all tests
python -m pytest

# Test specific components
python test_symptoms_analysis.py
python test_flan_t5_accuracy.py
```

## ⚠️ Known Issues

### Critical Issues
- **Missing Directories**: `routers/`, `services/`, `config/` directories need to be created
- **Symptom Analysis**: Model accuracy is critically low (15.7%)
- **Hair Disease Model**: Needs training before production use

### Performance Issues
- **Memory Usage**: AI models require significant RAM
- **Inference Speed**: GPU acceleration recommended for production

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google**: For the Flan-T5 Large model
- **PyTorch Team**: For the deep learning framework
- **FastAPI**: For the modern web framework
- **ChromaDB**: For vector database capabilities
- **Ayurvedic Community**: For traditional medical knowledge

## 📞 Support

- **Documentation**: [Full Documentation](docs/)
- **Issues**: [GitHub Issues](https://github.com/your-username/swasthvedha-backend/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/swasthvedha-backend/discussions)

---

**⚠️ Medical Disclaimer**: This system is for informational purposes only and should not replace professional medical advice. Always consult with qualified healthcare providers for medical decisions.

**Made with ❤️ for better healthcare through AI**
