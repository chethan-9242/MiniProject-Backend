from fastapi import APIRouter, File, UploadFile, HTTPException
from pydantic import BaseModel
from typing import Dict, List
from PIL import Image
import io
import json
import torch
import torch.nn as nn
import torchvision.transforms as transforms
import torchvision.models as models
from pathlib import Path

router = APIRouter()

# Load model at startup
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = None
class_mapping = None
transform = None

def load_model():
    global model, class_mapping, transform
    
    try:
        # Load class mapping
        class_mapping_path = Path("models/skin_classes.json")
        with open(class_mapping_path, 'r') as f:
            class_mapping = json.load(f)
        
        num_classes = len(class_mapping)
        
        # Create model architecture (same as training)
        model = models.resnet50(weights=None)
        num_features = model.fc.in_features
        model.fc = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(num_features, 512),
            nn.ReLU(),
            nn.BatchNorm1d(512),
            nn.Dropout(0.3),
            nn.Linear(512, num_classes)
        )
        
        # Load trained weights
        model_path = Path("models/skin_classifier.pth")
        checkpoint = torch.load(model_path, map_location=device)
        model.load_state_dict(checkpoint['model_state_dict'])
        model = model.to(device)
        model.eval()
        
        # Define transforms (same as training validation)
        transform = transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
        
        print(f"✅ Skin disease model loaded successfully!")
        print(f"   Classes: {list(class_mapping.values())}")
        print(f"   Accuracy: {checkpoint.get('best_val_accuracy', 'N/A')}")
        
        return True
    except Exception as e:
        print(f"❌ Error loading skin disease model: {e}")
        return False

# Load model on startup
MODEL_LOADED = load_model()

# Ayurvedic treatment database
def get_ayurvedic_treatment(disease_name: str, confidence: float) -> dict:
    """Get ayurvedic treatment recommendations for detected disease"""
    
    # Map disease to treatment
    treatments = {
        "BA- cellulitis": {
            "herbal_remedies": [
                "Neem for antibacterial action",
                "Turmeric for anti-inflammatory",
                "Manjistha for blood purification"
            ],
            "dietary_recommendations": [
                "Light, nutritious diet",
                "Plenty of water for hydration",
                "Anti-inflammatory foods"
            ],
            "lifestyle_changes": [
                "Elevate affected limb",
                "Keep area clean and dry",
                "Rest to support healing"
            ]
        },
        "BA-impetigo": {
            "herbal_remedies": [
                "Neem paste for antibacterial",
                "Turmeric for healing",
                "Tea tree oil (diluted) for disinfection"
            ],
            "dietary_recommendations": [
                "Immune-boosting foods",
                "Plenty of fluids",
                "Vitamin C rich foods"
            ],
            "lifestyle_changes": [
                "Keep sores clean and covered",
                "Do not touch or scratch",
                "Wash hands frequently"
            ]
        },
        "FU-athlete-foot": {
            "herbal_remedies": [
                "Tea tree oil for antifungal action",
                "Neem oil for treatment",
                "Garlic paste for antimicrobial"
            ],
            "dietary_recommendations": [
                "Reduce sugar intake",
                "Include probiotics",
                "Eat immune-boosting foods"
            ],
            "lifestyle_changes": [
                "Keep feet dry",
                "Wear breathable socks",
                "Avoid sharing footwear"
            ]
        },
        "FU-nail-fungus": {
            "herbal_remedies": [
                "Tea tree oil application",
                "Neem oil for antifungal",
                "Apple cider vinegar soak"
            ],
            "dietary_recommendations": [
                "Reduce sugar and yeast",
                "Include probiotics",
                "Vitamin D rich foods"
            ],
            "lifestyle_changes": [
                "Keep nails trimmed",
                "Avoid nail polish",
                "Wear breathable shoes"
            ]
        },
        "FU-ringworm": {
            "herbal_remedies": [
                "Neem paste for antifungal action",
                "Turmeric with water for topical application",
                "Garlic crushed and applied topically"
            ],
            "dietary_recommendations": [
                "Avoid sugar and refined carbs",
                "Increase probiotic-rich foods",
                "Drink immune-boosting herbal teas"
            ],
            "lifestyle_changes": [
                "Keep skin dry and clean",
                "Do not share personal items",
                "Wash clothes and bedding regularly"
            ]
        },
        "PA-cutaneous-larva-migrans": {
            "herbal_remedies": [
                "Neem for antiparasitic action",
                "Turmeric for healing",
                "Aloe vera for soothing"
            ],
            "dietary_recommendations": [
                "Immune-boosting diet",
                "Anti-inflammatory foods",
                "Plenty of water"
            ],
            "lifestyle_changes": [
                "Avoid walking barefoot",
                "Keep affected area clean",
                "Seek medical treatment"
            ]
        },
        "VI-chickenpox": {
            "herbal_remedies": [
                "Neem leaves bath for relief",
                "Sandalwood paste for cooling",
                "Aloe vera gel for soothing itching"
            ],
            "dietary_recommendations": [
                "Light, easily digestible foods",
                "Plenty of fluids to prevent dehydration",
                "Avoid salty and spicy foods"
            ],
            "lifestyle_changes": [
                "Complete bed rest",
                "Avoid scratching blisters",
                "Isolate from others to prevent spread"
            ]
        },
        "VI-shingles": {
            "herbal_remedies": [
                "Neem for antiviral properties",
                "Turmeric for pain and inflammation",
                "Aloe vera for cooling relief"
            ],
            "dietary_recommendations": [
                "Anti-inflammatory diet",
                "Vitamin B12 rich foods",
                "Include lysine-rich foods (fish, chicken)"
            ],
            "lifestyle_changes": [
                "Rest and stress reduction",
                "Keep rash covered and clean",
                "Apply cool compresses"
            ]
        }
    }
    
    # Get treatment or default
    treatment = treatments.get(disease_name, {
        "herbal_remedies": [
            "Neem for general skin health",
            "Turmeric for anti-inflammatory",
            "Aloe vera for soothing"
        ],
        "dietary_recommendations": [
            "Maintain balanced, nutritious diet",
            "Stay well hydrated",
            "Include fruits and vegetables"
        ],
        "lifestyle_changes": [
            "Practice good hygiene",
            "Use gentle skin care products",
            "Manage stress levels"
        ]
    })
    
    return treatment

class SkinDiseaseResult(BaseModel):
    detected_condition: str
    confidence: float
    description: str
    status: str
    message: str
    all_predictions: Dict[str, float]
    ayurvedic_treatment: Dict[str, List[str]]
    severity: str
    when_to_consult_doctor: str

@router.post("/analyze", response_model=SkinDiseaseResult)
async def analyze_skin_disease(file: UploadFile = File(...)):
    """
    Analyze skin disease from uploaded image
    
    Returns:
    - disease: Predicted disease name
    - confidence: Prediction confidence (0-100%)
    - status: "confident" or "uncertain"
    - message: Additional information
    - all_predictions: Confidence for all disease classes
    """
    
    if not MODEL_LOADED:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Read and validate image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Preprocess
        image_tensor = transform(image).unsqueeze(0).to(device)
        
        # Predict
        with torch.no_grad():
            outputs = model(image_tensor)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            confidence, predicted_idx = torch.max(probabilities, 1)
            
            predicted_idx = predicted_idx.item()
            confidence_pct = confidence.item() * 100
        
        # Get all predictions
        all_preds = {}
        for idx, prob in enumerate(probabilities[0]):
            disease_name = class_mapping.get(str(idx), f"Unknown_{idx}")
            all_preds[disease_name] = round(prob.item() * 100, 2)
        
        # Get predicted disease
        predicted_disease = class_mapping.get(str(predicted_idx), f"Unknown_{predicted_idx}")
        
        # Debug logging
        print(f"\n🔍 Prediction Debug:")
        print(f"   Predicted: {predicted_disease}")
        print(f"   Confidence: {confidence_pct:.2f}%")
        print(f"   All predictions: {all_preds}")
        
        # Confidence threshold: 70%
        CONFIDENCE_THRESHOLD = 70.0
        
        # Get ayurvedic treatment
        treatment = get_ayurvedic_treatment(predicted_disease, confidence_pct)
        
        # Determine severity
        if confidence_pct >= 80:
            severity = "High confidence"
        elif confidence_pct >= CONFIDENCE_THRESHOLD:
            severity = "Moderate confidence"
        else:
            severity = "Low confidence - recommend professional consultation"
        
        if confidence_pct >= CONFIDENCE_THRESHOLD:
            # Confident prediction
            return SkinDiseaseResult(
                detected_condition=predicted_disease,
                confidence=round(confidence_pct, 2),
                description=f"Detected {predicted_disease} with high confidence. This is a {predicted_disease.split('-')[0]} type infection.",
                status="confident",
                message=f"High confidence detection. The model is {confidence_pct:.1f}% confident this is {predicted_disease}.",
                all_predictions=all_preds,
                ayurvedic_treatment=treatment,
                severity=severity,
                when_to_consult_doctor="If symptoms worsen or do not improve in 1-2 weeks, consult a dermatologist."
            )
        else:
            # Uncertain prediction
            return SkinDiseaseResult(
                detected_condition=f"Uncertain (suggests: {predicted_disease})",
                confidence=round(confidence_pct, 2),
                description="This image may not match the trained disease categories. Please consult a dermatologist for accurate diagnosis.",
                status="uncertain",
                message=f"Low confidence ({confidence_pct:.1f}%). This image may not match the trained disease categories. Please consult a dermatologist for accurate diagnosis.",
                all_predictions=all_preds,
                ayurvedic_treatment=treatment,
                severity=severity,
                when_to_consult_doctor="Immediately consult a dermatologist for proper diagnosis and treatment."
            )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing image: {str(e)}")

@router.get("/diseases")
async def get_diseases():
    """Get list of detectable diseases"""
    
    if not MODEL_LOADED:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return {
        "diseases": list(class_mapping.values()),
        "total": len(class_mapping),
        "categories": {
            "bacterial": ["BA- cellulitis", "BA-impetigo"],
            "fungal": ["FU-athlete-foot", "FU-nail-fungus", "FU-ringworm"],
            "parasitic": ["PA-cutaneous-larva-migrans"],
            "viral": ["VI-chickenpox", "VI-shingles"]
        },
        "model_info": {
            "architecture": "ResNet50",
            "accuracy": "94.87%",
            "confidence_threshold": "70%"
        }
    }

@router.get("/health")
async def health_check():
    """Check if model is loaded and ready"""
    return {
        "status": "healthy" if MODEL_LOADED else "error",
        "model_loaded": MODEL_LOADED,
        "device": str(device),
        "num_classes": len(class_mapping) if class_mapping else 0
    }
