# 🚀 Quick Start: Train ML Models

## 📋 What You Need to Run

### Prerequisites
```bash
# Install required packages
pip install scikit-learn pandas numpy joblib
```

---

## 🎯 Step 1: Train Symptom Checker ML Model

### Directory: Project Root
```bash
# Navigate to project root first
cd C:\Users\Chethan\OneDrive\Desktop\SwasthVedha

# Then run training (from root directory)
py backend/train_symptom_checker.py
```

**Why from root?** Script looks for dataset at `data/symptoms/` and saves models to `backend/models/`

### What it does:
- ✅ Loads dataset from `data/symptoms/Disease_symptom_and_patient_profile_dataset.csv`
- ✅ Trains Random Forest and Gradient Boosting models
- ✅ Selects best model based on accuracy
- ✅ Saves model to `backend/models/symptom_checker_model.joblib`
- ✅ Expected accuracy: **85-98%**

### Expected output:
```
🔧 Training Symptom Checker ML Model...
📊 Dataset loaded: 350 samples
   Diseases: 12
🚀 Training Random Forest...
   ✅ Accuracy: 0.92 (92.00%)
🚀 Training Gradient Boosting...
   ✅ Accuracy: 0.89 (89.00%)
🏆 Best Model: Random Forest with 0.92 accuracy
💾 Model saved to: models/symptom_checker_model.joblib
✅ Training complete!
```

---

## 🎯 Step 2: Train Dosha Decision Tree Model

### Directory: Project Root (already there from Step 1)
```bash
# Make sure you're still in project root
# If not, run: cd C:\Users\Chethan\OneDrive\Desktop\SwasthVedha

# Run dosha training
py create_compatible_model.py
```

**Why from root?** Script saves model to `backend/models/dosha_classifier.joblib`

### What it does:
- ✅ Generates synthetic training data (1000 samples)
- ✅ Trains Decision Tree Regressor model
- ✅ Saves model to `backend/models/dosha_classifier.joblib`
- ✅ Expected R² Score: **0.7-0.9**

### Expected output:
```
🔧 Creating compatible dosha classification model...
📊 Generating synthetic training data...
🚀 Training model...
📊 Model Performance: R² Score = 0.85
💾 Model saved to: backend/models/dosha_classifier.joblib
✅ SUCCESS! Compatible dosha model created and saved.
```

---

## 🔧 Step 3: Update Backend Code

### Files to modify:
1. **`backend/routers/symptoms.py`** - Add ML model loading and prediction
2. **`backend/routers/dosha.py`** - Add Decision Tree model loading

### See detailed instructions in:
- `ML_MODEL_MIGRATION_GUIDE.md` (Step 3)

---

## 🧪 Step 4: Test Models

### Directory: Backend Directory
```bash
# Navigate to backend directory
cd C:\Users\Chethan\OneDrive\Desktop\SwasthVedha\backend

# Start the server
py main.py
```

**Why from backend?** FastAPI needs to find routers in the same directory structure

### Test Symptom Checker:
```bash
# In another terminal
curl -X POST "http://localhost:8000/api/symptoms/check" -H "Content-Type: application/json" -d "{\"symptoms\": [{\"id\": \"1\", \"name\": \"fever\", \"severity\": \"moderate\", \"duration\": \"2 days\"}]}"
```

### Test Dosha Classification:
```bash
curl -X POST "http://localhost:8000/api/dosha/analyze" -H "Content-Type: application/json" -d "{\"body_frame\": \"thin\", \"skin_type\": \"dry\", \"digestion\": \"irregular\", \"sleep_pattern\": \"light\", \"stress_response\": \"anxious\", \"climate_preference\": \"warm\", \"energy_level\": \"variable\", \"appetite\": \"irregular_appetite\", \"mental_state\": \"creative\", \"physical_activity\": \"quick_movements\"}"
```

---

## 📊 Summary of Commands with Directories

```bash
# ============================================
# STEP 1: Install dependencies
# Directory: Anywhere
# ============================================
pip install scikit-learn pandas numpy joblib

# ============================================
# STEP 2: Train Symptom Checker ML Model
# Directory: Project Root
# ============================================
cd C:\Users\Chethan\OneDrive\Desktop\SwasthVedha
py backend/train_symptom_checker.py

# ============================================
# STEP 3: Train Dosha Decision Tree Model
# Directory: Project Root (already there)
# ============================================
py create_compatible_model.py

# ============================================
# STEP 4: Update backend code
# Directory: Anywhere (edit in code editor)
# ============================================
# Edit: backend/routers/symptoms.py
# Edit: backend/routers/dosha.py
# (See ML_MODEL_MIGRATION_GUIDE.md)

# ============================================
# STEP 5: Start backend server
# Directory: Backend Directory
# ============================================
cd backend
py main.py
```

---

## ✅ Expected Results

### After training, you'll have:

1. **Symptom Checker ML Model**
   - File: `backend/models/symptom_checker_model.joblib`
   - Accuracy: 85-98%
   - Type: Random Forest or Gradient Boosting

2. **Dosha Decision Tree Model**
   - File: `backend/models/dosha_classifier.joblib`
   - R² Score: 0.7-0.9
   - Type: Decision Tree Regressor

---

## 🔍 Why Rule-Based Was Used (And Why ML is Better)

### Rule-Based (Current)
- ✅ Quick to implement
- ✅ No training needed
- ❌ Can't learn patterns
- ❌ Requires manual updates
- ❌ Limited to predefined rules

### ML Models (New)
- ✅ Learns from data
- ✅ Higher accuracy (85-98%)
- ✅ Handles complex patterns
- ✅ Improves with more data
- ✅ Can adapt to new conditions

---

## 📖 Full Documentation

See `ML_MODEL_MIGRATION_GUIDE.md` for:
- Complete code changes
- Integration instructions
- Testing procedures
- Migration strategy

---

**Ready? Run the commands above!** 🚀

