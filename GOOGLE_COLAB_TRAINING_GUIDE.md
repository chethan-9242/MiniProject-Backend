# 🚀 Google Colab Training Guide for SwasthVedha

## Step-by-Step Instructions for Training Models in Chrome

### 📋 Prerequisites
- Google account (Gmail)
- Chrome browser
- SwasthVedha data folder zipped
- Stable internet connection

---

## 🎯 Step 1: Prepare Your Data

### 1.1 Create Data Zip File
```powershell
# In your SwasthVedha folder, compress the data directory
Compress-Archive -Path "data" -DestinationPath "SwasthVedha_data.zip"
```

**Expected zip structure:**
```
SwasthVedha_data.zip
└── data/
    ├── skin_disease/
    │   ├── train_set/
    │   └── test_set/
    ├── symptoms/
    │   └── Disease_symptom_and_patient_profile_dataset.csv
    └── dosha/
        └── Ayurveda/
```

---

## 🎯 Step 2: Access Google Colab

### 2.1 Open Google Colab
1. Open **Chrome browser**
2. Go to: `https://colab.research.google.com/`
3. Sign in with your Google account

### 2.2 Upload Training Notebooks
1. Click **"Upload"** in Colab
2. Upload these notebooks from your `notebooks/` folder:
   - `skin_disease_cnn_colab.ipynb`
   - `symptom_checker_ml_colab.ipynb`

---

## 🎯 Step 3: Train Skin Disease CNN

### 3.1 Open Skin Disease Notebook
1. Click on `skin_disease_cnn_colab.ipynb`
2. **Important**: Set runtime to GPU
   - Go to **Runtime > Change runtime type**
   - Set **Hardware accelerator** to **GPU (T4)**
   - Click **Save**

### 3.2 Execute Training Steps
**Run cells in order (Ctrl+Enter for each cell):**

#### Cell 1: Install Dependencies
```python
# This installs PyTorch, OpenCV, etc.
# ⏳ Takes ~2-3 minutes
```

#### Cell 2: Mount Google Drive
```python
# Click the authorization link
# Copy the code back to Colab
# ✅ Shows "Google Drive mounted successfully!"
```

#### Cell 3: Upload Data
```python
# Click "Choose Files"
# Select your SwasthVedha_data.zip
# Wait for upload (depends on file size)
# ✅ Shows extraction confirmation
```

#### Cell 4: Analyze Dataset
```python
# Shows your skin disease classes
# Displays training/test counts
# ⏳ Takes ~30 seconds
```

#### Cell 5-8: Training Process
```python
# 🔥 Main training happens here
# ⏳ Takes ~20-30 minutes with GPU
# 📊 Shows progress for each epoch
```

#### Cell 9-10: Results & Visualization
```python
# Shows accuracy plots
# Displays confusion matrix
# 📈 Training vs Testing accuracy
```

#### Cell 11: Save Model
```python
# Saves to Google Drive
# Downloads model file to your computer
# ✅ Model ready for integration!
```

### 3.3 Expected Results
- **Training Time**: 20-30 minutes
- **Expected Accuracy**: 85-95%
- **Output Files**: 
  - `swasthvedha_skin_cnn_model.pth`
  - Saved in Google Drive

---

## 🎯 Step 4: Train Symptom Checker ML

### 4.1 Open Symptom Checker Notebook
1. Click on `symptom_checker_ml_colab.ipynb`
2. **No GPU needed** for this notebook

### 4.2 Execute Training Steps
**Run cells in order:**

#### Cell 1: Install Dependencies
```python
# Installs scikit-learn, pandas, etc.
# ⏳ Takes ~1-2 minutes
```

#### Cell 2: Mount Google Drive
```python
# Same process as before
```

#### Cell 3: Upload Data
```python
# Upload same SwasthVedha_data.zip
# Or skip if already uploaded
```

#### Cell 4: Data Analysis
```python
# Shows disease distribution
# Analyzes symptom patterns
# 📊 Creates visualization charts
```

#### Cell 5-6: Model Training
```python
# Trains multiple ML models
# Compares performance
# 🏆 Selects best model
```

#### Cell 7: Hyperparameter Tuning
```python
# Optimizes best model
# ⏳ Takes ~5-10 minutes
```

#### Cell 8: Save Model
```python
# Downloads trained model
# ✅ Ready for integration!
```

### 4.3 Expected Results
- **Training Time**: 10-15 minutes
- **Expected Accuracy**: 85-98%
- **Output Files**:
  - `swasthvedha_symptom_checker_model.joblib`
  - `symptom_checker_integration.py`

---

## 🎯 Step 5: Integration with Your Backend

### 5.1 Download Model Files
After training, you'll have these files:
```
Downloads/
├── swasthvedha_skin_cnn_model.pth
├── swasthvedha_symptom_checker_model.joblib
└── symptom_checker_integration.py
```

### 5.2 Place in Your Project
```
SwasthVedha/
├── backend/
│   └── models/               # 📁 Create this folder
│       ├── skin_disease_cnn_model.pth
│       └── symptom_checker_model.joblib
└── ... (rest of project)
```

### 5.3 Update Backend Code
1. **For Skin Disease**: Copy code from notebook's final cell
2. **For Symptoms**: Use the `symptom_checker_integration.py` file
3. **Replace mock functions** in your FastAPI routers

---

## 🎯 Step 6: Testing Your Models

### 6.1 Test Skin Disease Model
```python
# In your backend, test with a sample image
from routers.skin_disease import analyze_skin_image_cnn
# Upload test image and verify predictions
```

### 6.2 Test Symptom Checker
```python
# Test with sample symptoms
from routers.symptoms import analyze_symptoms_ml
# Try symptoms like ["fever", "cough", "fatigue"]
```

---

## 🔧 Troubleshooting

### Common Issues:

#### 1. **"Runtime disconnected"**
- **Solution**: Reconnect and re-run from the beginning
- **Prevention**: Keep Colab tab active during training

#### 2. **"GPU not available"**
- **Solution**: Runtime > Change runtime type > GPU
- **Alternative**: Use CPU (will be slower)

#### 3. **"Upload failed"**
- **Solution**: Check zip file size (<100MB recommended)
- **Alternative**: Upload to Google Drive first, then access

#### 4. **"Model accuracy too low"**
- **Causes**: Insufficient training data or poor data quality
- **Solutions**: 
  - Increase training epochs
  - Add more data
  - Adjust hyperparameters

#### 5. **"Integration errors"**
- **Solution**: Follow integration code exactly
- **Check**: File paths and model loading

---

## 📊 Performance Expectations

### Skin Disease CNN:
- **Training Time**: 20-30 minutes (GPU)
- **Accuracy**: 85-95%
- **Memory**: ~2GB GPU RAM
- **Model Size**: ~100MB

### Symptom Checker ML:
- **Training Time**: 10-15 minutes (CPU)
- **Accuracy**: 85-98%
- **Memory**: ~1GB RAM
- **Model Size**: ~10MB

---

## 🎉 Success Indicators

### ✅ Training Complete When:
1. **No error messages** in any cell
2. **Model files downloaded** successfully
3. **Accuracy metrics** displayed
4. **Integration code** generated

### ✅ Ready for Production When:
1. **Models integrated** in backend
2. **API endpoints** working with real predictions
3. **Test predictions** make sense
4. **Performance** meets expectations

---

## 💡 Pro Tips

### 🚀 Speed Up Training:
- Use **GPU runtime** for CNN training
- **Keep Colab tab active** to prevent disconnection
- **Upload data once**, use for both notebooks

### 🎯 Better Results:
- **More training data** = better accuracy
- **Clean data** = more reliable predictions
- **Longer training** = potentially better models

### 💾 Save Work:
- **Models auto-save** to Google Drive
- **Download immediately** after training
- **Keep backups** of trained models

---

## 🆘 Need Help?

### If Training Fails:
1. **Check error messages** in Colab output
2. **Verify data structure** matches expected format
3. **Try reducing batch size** if memory errors
4. **Use CPU runtime** if GPU issues persist

### If Models Don't Work:
1. **Check file paths** in integration code
2. **Verify model loading** syntax
3. **Test with simple examples** first
4. **Compare with notebook predictions**

---

**Happy Training! 🎯**

Your models will be ready for production use in SwasthVedha once training completes successfully!