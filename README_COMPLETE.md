# SwasthVedha Backend - Complete Documentation

## 🎯 Overview
AI-powered Ayurvedic healthcare platform backend with disease detection, symptom analysis, and personalized recommendations.

---

## 🚀 Features

### 1. **Skin Disease Detection**
- ResNet50-based classifier
- 8 disease categories (bacterial, fungal, parasitic, viral)
- 94.4% accuracy
- Image upload and real-time prediction

### 2. **Hair Disease Detection**
- ResNet50-based classifier
- 10 disease categories
- 99.8% accuracy
- Image analysis with confidence scores

### 3. **Symptom Checker** ⭐ NEW
- 12 comprehensive Ayurvedic conditions
- Intelligent symptom matching algorithm
- Dosha imbalance detection
- Personalized Ayurvedic recommendations
- **Save/Retrieve Analysis Feature**

### 4. **Dosha Classification**
- Ayurvedic constitution analysis
- Vata, Pitta, Kapha assessment
- Personalized diet and lifestyle recommendations

### 5. **GraphRAG Knowledge Base**
- Ayurvedic knowledge retrieval
- Flan-T5 model integration
- ChromaDB vector database
- 20+ Ayurvedic documents

### 6. **YouTube Integration**
- Ayurvedic remedy videos
- Educational content
- Video recommendations

---

## 📁 Project Structure

```
backend/
├── main.py                          # FastAPI application entry point
├── requirements.txt                 # Python dependencies
├── routers/                         # API route handlers
│   ├── __init__.py
│   ├── skin_disease.py             # Skin disease detection API
│   ├── hair_disease.py             # Hair disease detection API
│   ├── symptoms.py                 # Symptom checker API ⭐ NEW
│   ├── dosha.py                    # Dosha classification API
│   ├── graph_rag.py                # GraphRAG knowledge base API
│   └── youtube.py                  # YouTube video integration
├── models/                          # Trained model files
│   ├── skin_classifier.pth         # Skin disease model (94 MB)
│   ├── hair_classifier.pth         # Hair disease model (94 MB)
│   ├── skin_classes.json           # Skin disease class names
│   ├── hair_classes.json           # Hair disease class names
│   └── README_MODELS.md            # Model documentation
├── saved_analyses/                  # Saved symptom analyses
├── chroma_db/                       # ChromaDB vector storage
├── Train_Skin_Disease_Model.ipynb  # Skin model training notebook
├── Train_Hair_Disease_Model.ipynb  # Hair model training notebook
├── test_symptoms.py                # Symptom checker test script
├── test_save.py                    # Save analysis test script
├── debug_constipation.py           # Debug script
├── TRAINING_GUIDE.md               # Model training guide
├── SETUP_COMPLETE.md               # Setup instructions
├── FINAL_STATUS.md                 # Project status
├── SAVE_ANALYSIS_FEATURE.md        # Save feature documentation
└── UPDATE_GITHUB_REPO.md           # GitHub update guide
```

---

## 🔧 Installation

### Prerequisites
- Python 3.8+
- pip
- Virtual environment (recommended)

### Step 1: Clone Repository
```bash
git clone https://github.com/chethan-9242/MiniProject-Backend.git
cd MiniProject-Backend
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Download Model Files
⚠️ **Important**: Model files are not included in GitHub due to size (94 MB each).

**Options:**
1. Train models using provided Jupyter notebooks
2. Download from Google Drive (contact repository owner)
3. Place your own trained models in `models/` directory

### Step 5: Run Backend
```bash
python -m uvicorn main:app --reload
```

Backend will be available at: `http://localhost:8000`

---

## 📚 API Endpoints

### Skin Disease Detection
- `POST /api/skin/predict` - Upload image for prediction
- `GET /api/skin/health` - Check health status

### Hair Disease Detection
- `POST /api/hair/predict` - Upload image for prediction
- `GET /api/hair/health` - Check health status

### Symptom Checker ⭐ NEW
- `POST /api/symptoms/check` - Analyze symptoms
- `POST /api/symptoms/save` - Save analysis
- `GET /api/symptoms/history/{user_id}` - Get saved analyses
- `GET /api/symptoms/history/{user_id}/{analysis_id}` - Get specific analysis
- `DELETE /api/symptoms/history/{user_id}/{analysis_id}` - Delete analysis
- `GET /api/symptoms/health` - Check health status

### Dosha Classification
- `POST /api/dosha/analyze` - Analyze dosha constitution
- `GET /api/dosha/health` - Check health status

### GraphRAG Knowledge Base
- `POST /api/rag/query` - Query Ayurvedic knowledge
- `GET /api/rag/knowledge/categories` - Get knowledge categories
- `POST /api/rag/knowledge/search` - Semantic search
- `GET /api/rag/health` - Check health status

### YouTube Integration
- `GET /api/youtube/videos` - Get remedy videos
- `GET /api/youtube/health` - Check health status

---

## 🧪 Testing

### Test Symptom Checker
```bash
# Make sure backend is running first
python test_symptoms.py
```

### Test Save Analysis
```bash
python test_save.py
```

### Manual API Testing
Visit: `http://localhost:8000/docs` for interactive API documentation

---

## 🎓 Model Training

### Train Skin Disease Model
1. Open `Train_Skin_Disease_Model.ipynb` in Jupyter/Colab
2. Upload dataset (or use provided paths)
3. Run all cells
4. Save trained model to `models/skin_classifier.pth`

### Train Hair Disease Model
1. Open `Train_Hair_Disease_Model.ipynb` in Jupyter/Colab
2. Upload dataset (or use provided paths)
3. Run all cells
4. Save trained model to `models/hair_classifier.pth`

**See**: `TRAINING_GUIDE.md` for detailed instructions

---

## 📊 Model Performance

### Skin Disease Classifier
- **Architecture**: ResNet50 (ImageNet pretrained)
- **Accuracy**: 94.4%
- **Classes**: 8
- **Dataset**: Custom skin disease images
- **Training Time**: ~30-45 minutes (GPU)

### Hair Disease Classifier
- **Architecture**: ResNet50 (ImageNet pretrained)
- **Accuracy**: 99.8%
- **Classes**: 10
- **Dataset**: Custom hair disease images
- **Training Time**: ~30-45 minutes (GPU)

### Symptom Checker
- **Method**: Knowledge-based matching + scoring
- **Conditions**: 12 Ayurvedic conditions
- **Algorithm**: 40% overlap + 40% keywords + 20% exact match
- **Response Time**: < 100ms

---

## 🔐 Environment Variables

Create `.env` file:
```env
# Optional
DATABASE_URL=postgresql://user:pass@localhost/swasthvedha
YOUTUBE_API_KEY=your_youtube_api_key_here
```

---

## 📖 Documentation Files

- `README.md` - This file
- `TRAINING_GUIDE.md` - How to train models
- `SETUP_COMPLETE.md` - Setup verification
- `FINAL_STATUS.md` - Project status
- `SAVE_ANALYSIS_FEATURE.md` - Save analysis feature details
- `UPDATE_GITHUB_REPO.md` - GitHub update instructions
- `DATASET_FIX.txt` - Dataset fixes applied
- `models/README_MODELS.md` - Model files documentation

---

## 🐛 Troubleshooting

### Models Not Loading?
- Ensure `.pth` files are in `models/` directory
- Check file names match exactly
- Verify file sizes (~94 MB each)

### ChromaDB Errors?
- Delete `chroma_db/` directory
- Restart backend (it will recreate automatically)

### Port Already in Use?
```bash
# Use different port
uvicorn main:app --reload --port 8001
```

### Import Errors?
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

---

## 🚀 Deployment

### Local Development
```bash
uvicorn main:app --reload
```

### Production
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Docker (Optional)
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 👥 Contributors
- **Chethan** - Lead Developer
- Repository: https://github.com/chethan-9242/MiniProject-Backend

---

## 📝 License
This project is for educational purposes.

---

## 🆕 Recent Updates

### Latest (Jan 28, 2025) - Commit `902e4dd`
- ✅ Added comprehensive symptom checker
- ✅ Implemented save/retrieve analysis feature
- ✅ Enhanced symptom matching algorithm
- ✅ Added 12 Ayurvedic condition database
- ✅ Integrated GraphRAG with Flan-T5
- ✅ Updated all routers and documentation
- ✅ Removed outdated utility scripts
- ✅ Added test scripts and debug tools

---

## 📧 Support
For issues, questions, or contributions:
- GitHub Issues: https://github.com/chethan-9242/MiniProject-Backend/issues
- Email: chethan.9242@gmail.com

---

**Status**: ✅ Production Ready
**Last Updated**: January 28, 2025
**Version**: 2.0.0
