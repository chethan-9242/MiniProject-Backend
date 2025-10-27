# Update GitHub Repository - Step by Step Guide

## 🎯 Goal
Replace the old backend code in https://github.com/chethan-9242/MiniProject-Backend.git with the new updated backend

## 📋 Files to Copy from Current Backend

### Core Application Files:
1. `main.py` - Main FastAPI application with all routers
2. `routers/` - All router files:
   - `skin_disease.py`
   - `hair_disease.py` 
   - `youtube.py`
   - `dosha.py`
   - `graph_rag.py`
   - `symptoms.py` (NEW - Symptom Checker with save functionality)
3. `requirements.txt` - All Python dependencies

### Model Files (Large):
- `models/skin_disease_model.h5`
- `models/hair_disease_model.h5`

### Configuration:
- `.env` or `.env.example` - Environment variables template
- `.gitignore` - Git ignore rules

### Documentation:
- `README.md` - Updated documentation
- `SAVE_ANALYSIS_FEATURE.md` - New feature documentation
- `test_symptoms.py` - Test script for symptom checker
- `test_save.py` - Test script for save functionality
- `debug_constipation.py` - Debug script

## 🚀 Quick Update Commands

```powershell
# Navigate to the cloned temporary repository
cd C:\Users\Chethan\OneDrive\Desktop\SwasthVedha-Backend-Temp

# Remove all old Python files (keep .git directory)
Remove-Item *.py
Remove-Item -Recurse routers -ErrorAction SilentlyContinue

# Copy new backend files
Copy-Item C:\Users\Chethan\OneDrive\Desktop\SwasthVedha\backend\main.py .
Copy-Item -Recurse C:\Users\Chethan\OneDrive\Desktop\SwasthVedha\backend\routers .
Copy-Item C:\Users\Chethan\OneDrive\Desktop\SwasthVedha\backend\requirements.txt .
Copy-Item C:\Users\Chethan\OneDrive\Desktop\SwasthVedha\backend\test_*.py .
Copy-Item C:\Users\Chethan\OneDrive\Desktop\SwasthVedha\backend\debug_*.py .
Copy-Item C:\Users\Chethan\OneDrive\Desktop\SwasthVedha\SAVE_ANALYSIS_FEATURE.md .

# Copy models if needed (skip if already there and large)
# Copy-Item -Recurse C:\Users\Chethan\OneDrive\Desktop\SwasthVedha\backend\models .

# Add all changes
git add .

# Commit changes
git commit -m "Update backend with symptom checker, save analysis, and improvements

- Added symptom checker with 12 condition knowledge base
- Implemented save/retrieve analysis endpoints
- Enhanced symptom matching algorithm
- Added GraphRAG integration
- Improved dosha classification
- Added YouTube video integration
- Updated all routers and models"

# Push to GitHub
git push origin main
```

## 📝 Manual Alternative

If automated copying doesn't work, manually:

1. Open both folders side by side
2. Delete old `.py` files from `SwasthVedha-Backend-Temp`
3. Copy new files from `SwasthVedha/backend`
4. Commit and push

## ✅ Verification

After pushing, verify on GitHub:
1. Check main.py has all 6 routers
2. Check symptoms.py exists in routers/
3. Verify requirements.txt is updated
4. Check README and documentation

## 🔧 Key Changes Summary

### What's New:
- **Symptom Checker**: 12 conditions with intelligent matching
- **Save Analysis**: Backend storage + localStorage fallback
- **Enhanced Algorithms**: Better keyword matching and scoring
- **GraphRAG**: Ayurvedic knowledge base with Flan-T5
- **4 New Endpoints**:
  - POST /api/symptoms/save
  - GET /api/symptoms/history/{user_id}
  - GET /api/symptoms/history/{user_id}/{analysis_id}
  - DELETE /api/symptoms/history/{user_id}/{analysis_id}

### What's Updated:
- main.py - Added symptoms router
- requirements.txt - Added necessary dependencies
- All routers improved and tested
