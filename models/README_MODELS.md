# Model Files

## 📁 Required Model Files

This directory should contain the trained model files:

### Skin Disease Classifier
- **File**: `skin_classifier.pth` (~94 MB)
- **Classes**: See `skin_classes.json`
- **Architecture**: ResNet50 (pretrained on ImageNet)
- **Classes**: 8 skin diseases (bacterial, fungal, parasitic, viral)

### Hair Disease Classifier  
- **File**: `hair_classifier.pth` (~94 MB)
- **Classes**: See `hair_classes.json`
- **Architecture**: ResNet50 (pretrained on ImageNet)
- **Classes**: 10 hair diseases

## ⚠️ Important: Large Files Not in Git

Due to GitHub's file size limits (100 MB), the `.pth` model files are **NOT** included in this repository.

## 📥 How to Get Model Files

### Option 1: Train Models Yourself
Use the provided Jupyter notebooks to train the models:
1. `Train_Skin_Disease_Model.ipynb`
2. `Train_Hair_Disease_Model.ipynb`

### Option 2: Download from Google Drive
Contact the repository owner for access to pre-trained models.

### Option 3: Use Alternative Storage
Upload models to:
- Google Drive
- Dropbox
- AWS S3
- Azure Blob Storage

## 📝 Model Training Details

### Skin Disease Model
- **Dataset**: Custom skin disease dataset
- **Training Time**: ~30-45 minutes on GPU
- **Accuracy**: ~94.4%
- **Input Size**: 224x224 RGB images
- **Output**: 8 disease classes

### Hair Disease Model
- **Dataset**: Custom hair disease dataset  
- **Training Time**: ~30-45 minutes on GPU
- **Accuracy**: ~99.8%
- **Input Size**: 224x224 RGB images
- **Output**: 10 disease classes

## 🔧 Model Loading Code

The models are loaded in `routers/skin_disease.py` and `routers/hair_disease.py`:

```python
model = models.resnet50(weights=None)
model.fc = nn.Linear(model.fc.in_features, num_classes)
model.load_state_dict(torch.load('models/skin_classifier.pth', map_location=device))
model.eval()
```

## ✅ Verification

After placing model files in this directory, verify:
```bash
ls models/
# Should show:
# - skin_classifier.pth
# - hair_classifier.pth
# - skin_classes.json
# - hair_classes.json
```

## 📊 File Structure
```
models/
├── README_MODELS.md (this file)
├── skin_classifier.pth (94 MB) ← Download separately
├── hair_classifier.pth (94 MB) ← Download separately
├── skin_classes.json ✅ Included
└── hair_classes.json ✅ Included
```
