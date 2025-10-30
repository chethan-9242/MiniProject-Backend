from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from pydantic import BaseModel
from typing import Dict, List, Optional
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
        class_mapping_path = Path("models/hair_classes.json")
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
        model_path = Path("models/hair_classifier.pth")
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
        
        print(f"✅ Hair disease model loaded successfully!")
        print(f"   Classes: {list(class_mapping.values())}")
        print(f"   Accuracy: {checkpoint.get('best_val_accuracy', 'N/A')}")
        
        return True
    except Exception as e:
        print(f"❌ Error loading hair disease model: {e}")
        return False

# Load model on startup
MODEL_LOADED = load_model()

# Ayurvedic treatment database for hair diseases
def get_ayurvedic_treatment(disease_name: str, confidence: float) -> dict:
    """Get ayurvedic treatment recommendations for detected hair disease"""
    
    # Map disease to treatment
    treatments = {
        "Alopecia Areata": {
            "herbal_remedies": [
                "Bhringraj oil for hair regrowth",
                "Amla (Indian Gooseberry) for strengthening hair follicles",
                "Brahmi oil massage for scalp nourishment"
            ],
            "dietary_recommendations": [
                "Iron-rich foods (spinach, lentils)",
                "Protein-rich diet (eggs, fish, nuts)",
                "Vitamin B complex foods"
            ],
            "lifestyle_changes": [
                "Reduce stress through yoga and meditation",
                "Avoid harsh chemical treatments",
                "Regular scalp massage to improve circulation"
            ]
        },
        "Contact Dermatitis": {
            "herbal_remedies": [
                "Aloe vera gel for soothing irritation",
                "Neem oil for antibacterial action",
                "Coconut oil for moisturizing"
            ],
            "dietary_recommendations": [
                "Anti-inflammatory foods (turmeric, ginger)",
                "Avoid potential allergens",
                "Increase omega-3 fatty acids"
            ],
            "lifestyle_changes": [
                "Identify and avoid irritating products",
                "Use hypoallergenic hair care products",
                "Keep scalp clean and dry"
            ]
        },
        "Folliculitis": {
            "herbal_remedies": [
                "Tea tree oil (diluted) for antibacterial action",
                "Neem paste for treating infection",
                "Turmeric for anti-inflammatory properties"
            ],
            "dietary_recommendations": [
                "Immune-boosting foods (vitamin C, zinc)",
                "Avoid high-sugar foods",
                "Include probiotics"
            ],
            "lifestyle_changes": [
                "Avoid tight hairstyles",
                "Keep hair and scalp clean",
                "Use clean towels and avoid sharing personal items"
            ]
        },
        "Head Lice": {
            "herbal_remedies": [
                "Neem oil for killing lice",
                "Coconut oil suffocation method",
                "Tea tree oil to repel lice"
            ],
            "dietary_recommendations": [
                "Maintain overall health with balanced diet",
                "Include garlic for natural repellent properties",
                "Stay hydrated"
            ],
            "lifestyle_changes": [
                "Regular combing with fine-toothed nit comb",
                "Wash bedding and clothing in hot water",
                "Avoid sharing combs, hats, and pillows"
            ]
        },
        "Lichen Planus": {
            "herbal_remedies": [
                "Aloe vera for soothing inflammation",
                "Turmeric paste for anti-inflammatory action",
                "Coconut oil for moisturizing scalp"
            ],
            "dietary_recommendations": [
                "Anti-inflammatory diet",
                "Avoid acidic and spicy foods",
                "Include vitamin A rich foods"
            ],
            "lifestyle_changes": [
                "Stress management techniques",
                "Avoid harsh hair treatments",
                "Use mild, fragrance-free products"
            ]
        },
        "Male Pattern Baldness": {
            "herbal_remedies": [
                "Bhringraj oil for promoting hair growth",
                "Saw palmetto to block DHT",
                "Amla and Shikakai for hair strengthening"
            ],
            "dietary_recommendations": [
                "Protein-rich diet (lean meat, legumes)",
                "Iron and zinc supplements",
                "Biotin-rich foods (eggs, nuts)"
            ],
            "lifestyle_changes": [
                "Regular scalp massage",
                "Reduce stress levels",
                "Avoid smoking and excessive alcohol"
            ]
        },
        "Psoriasis": {
            "herbal_remedies": [
                "Neem for reducing inflammation",
                "Aloe vera gel for soothing scales",
                "Turmeric for anti-inflammatory properties"
            ],
            "dietary_recommendations": [
                "Anti-inflammatory diet (omega-3, vegetables)",
                "Avoid triggers (alcohol, processed foods)",
                "Include vitamin D rich foods"
            ],
            "lifestyle_changes": [
                "Moisturize scalp regularly",
                "Avoid scratching",
                "Manage stress through relaxation techniques"
            ]
        },
        "Seborrheic Dermatitis": {
            "herbal_remedies": [
                "Tea tree oil for antifungal properties",
                "Neem oil for reducing inflammation",
                "Aloe vera for soothing irritation"
            ],
            "dietary_recommendations": [
                "Reduce sugar and yeast intake",
                "Include zinc-rich foods",
                "Probiotics for gut health"
            ],
            "lifestyle_changes": [
                "Wash hair regularly with mild shampoo",
                "Avoid oil-based hair products",
                "Manage stress levels"
            ]
        },
        "Telogen Effluvium": {
            "herbal_remedies": [
                "Bhringraj oil for hair regrowth",
                "Amla for strengthening hair",
                "Ashwagandha for stress reduction"
            ],
            "dietary_recommendations": [
                "High-protein diet",
                "Iron and vitamin B12 supplements",
                "Include biotin-rich foods"
            ],
            "lifestyle_changes": [
                "Reduce stress through meditation",
                "Get adequate sleep (7-8 hours)",
                "Gentle hair care routine"
            ]
        },
        "Tinea Capitis": {
            "herbal_remedies": [
                "Neem oil for antifungal action",
                "Tea tree oil (diluted) for treatment",
                "Garlic paste for antimicrobial properties"
            ],
            "dietary_recommendations": [
                "Reduce sugar intake",
                "Include immune-boosting foods",
                "Probiotics for gut health"
            ],
            "lifestyle_changes": [
                "Keep scalp clean and dry",
                "Avoid sharing combs and hats",
                "Wash bedding regularly in hot water"
            ]
        }
    }
    
    # Get treatment or default
    treatment = treatments.get(disease_name, {
        "herbal_remedies": [
            "Bhringraj oil for general hair health",
            "Amla for hair strengthening",
            "Coconut oil for scalp nourishment"
        ],
        "dietary_recommendations": [
            "Maintain balanced, protein-rich diet",
            "Stay well hydrated",
            "Include vitamins and minerals"
        ],
        "lifestyle_changes": [
            "Practice good hair hygiene",
            "Use gentle hair care products",
            "Manage stress levels"
        ]
    })
    
    return treatment

class HairDiseaseResult(BaseModel):
    detected_condition: str
    confidence: float
    description: str
    status: str
    message: str
    all_predictions: Dict[str, float]
    ayurvedic_recommendations: Dict[str, List[str]]
    dosha_association: str
    severity: str
    when_to_consult: str

@router.post("/analyze", response_model=HairDiseaseResult)
async def analyze_hair_disease(
    file: Optional[UploadFile] = File(None),
    symptoms: Optional[str] = Form(None)
):
    """
    Analyze hair disease from uploaded image and/or symptoms
    
    Parameters:
    - file: Optional hair/scalp image
    - symptoms: Optional JSON string of symptoms
    
    Returns:
    - disease: Predicted disease name
    - confidence: Prediction confidence (0-100%)
    - status: "confident" or "uncertain"
    - message: Additional information
    - all_predictions: Confidence for all disease classes
    - ayurvedic_treatment: Herbal remedies, diet, lifestyle changes
    """
    
    if not MODEL_LOADED:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    # Check if we have either file or symptoms
    if not file and not symptoms:
        raise HTTPException(status_code=400, detail="Please provide either an image or symptoms")
    
    try:
        # Log incoming request
        print(f"\n📥 Hair Disease Analysis Request:")
        print(f"   Has image: {file is not None}")
        print(f"   Has symptoms: {symptoms is not None}")
        
        # If we have symptoms but no image, analyze based on symptoms
        if not file and symptoms:
            import json
            print(f"   Processing symptom-based analysis...")
            print(f"   Raw symptoms: {symptoms}")
            
            try:
                symptom_list = json.loads(symptoms)
                print(f"   Parsed {len(symptom_list)} symptoms:")
                for s in symptom_list:
                    print(f"      - {s.get('name', 'Unknown')} ({s.get('severity', 'N/A')}, {s.get('duration', 'N/A')})")
            except Exception as e:
                print(f"   ❌ Failed to parse symptoms: {e}")
                raise HTTPException(status_code=400, detail="Invalid symptoms format")
            
            # Simple symptom-based analysis
            # Map common symptoms to possible conditions
            symptom_names = [s.get('name', '').lower() for s in symptom_list]
            
            condition_scores = {}
            
            # Hair loss symptoms
            if any(term in ' '.join(symptom_names) for term in ['hair loss', 'baldness', 'thinning', 'falling']):
                condition_scores['Male Pattern Baldness'] = 60
                condition_scores['Telogen Effluvium'] = 55
                condition_scores['Alopecia Areata'] = 50
            
            # Itching/inflammation symptoms  
            if any(term in ' '.join(symptom_names) for term in ['itching', 'itch', 'irritation', 'red', 'inflamed']):
                condition_scores['Seborrheic Dermatitis'] = 65
                condition_scores['Contact Dermatitis'] = 60
                condition_scores['Psoriasis'] = 55
            
            # Flaking/dandruff symptoms
            if any(term in ' '.join(symptom_names) for term in ['flaking', 'flakes', 'dandruff', 'scaling']):
                condition_scores['Seborrheic Dermatitis'] = 70
                condition_scores['Psoriasis'] = 60
            
            # Bumps/pimples symptoms
            if any(term in ' '.join(symptom_names) for term in ['bump', 'pimple', 'pustule', 'pus']):
                condition_scores['Folliculitis'] = 70
            
            # Patches symptoms
            if any(term in ' '.join(symptom_names) for term in ['patch', 'bald spot', 'circular']):
                condition_scores['Alopecia Areata'] = 75
                condition_scores['Tinea Capitis'] = 60
            
            # If no conditions matched, default to general
            if not condition_scores:
                condition_scores = {
                    'Seborrheic Dermatitis': 40,
                    'Contact Dermatitis': 35,
                    'Telogen Effluvium': 30
                }
            
            # Get top prediction
            predicted_disease = max(condition_scores, key=condition_scores.get)
            confidence_pct = condition_scores[predicted_disease]
            
            # Prepare all predictions
            all_preds = {disease: float(score) for disease, score in condition_scores.items()}
            
            # Get ayurvedic treatment
            treatment = get_ayurvedic_treatment(predicted_disease, confidence_pct)
            
            ayurvedic_recommendations = {
                "herbs_oils": treatment.get("herbal_remedies", []),
                "diet": treatment.get("dietary_recommendations", []),
                "lifestyle": treatment.get("lifestyle_changes", []),
                "home_care": []
            }
            
            dosha_map = {
                "Alopecia Areata": "Vata-Pitta",
                "Contact Dermatitis": "Pitta-Kapha",
                "Folliculitis": "Pitta",
                "Head Lice": "Kapha",
                "Lichen Planus": "Pitta",
                "Male Pattern Baldness": "Vata-Pitta",
                "Psoriasis": "Vata-Kapha",
                "Seborrheic Dermatitis": "Kapha-Pitta",
                "Telogen Effluvium": "Vata",
                "Tinea Capitis": "Kapha"
            }
            dosha = dosha_map.get(predicted_disease, "Unknown")
            
            print(f"\n✅ Symptom-Based Analysis Complete:")
            print(f"   Predicted: {predicted_disease}")
            print(f"   Confidence: {confidence_pct}%")
            print(f"   Dosha: {dosha}")
            
            return HairDiseaseResult(
                detected_condition=predicted_disease,
                confidence=round(confidence_pct, 2),
                description=f"Based on your symptoms, this appears to be {predicted_disease}. For accurate diagnosis, please upload an image or consult a specialist.",
                status="symptom_based",
                message=f"Analysis based on symptoms only. Confidence: {confidence_pct:.1f}%. For better accuracy, please upload an image.",
                all_predictions=all_preds,
                ayurvedic_recommendations=ayurvedic_recommendations,
                dosha_association=dosha,
                severity="Symptom-based analysis - recommend image upload for confirmation",
                when_to_consult="If symptoms persist or worsen, consult a dermatologist or trichologist. Upload an image for more accurate analysis."
            )
        
        # Image-based analysis
        if not file:
            raise HTTPException(status_code=400, detail="Image file is required")
            
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
        print(f"\n🔍 Hair Disease Prediction Debug:")
        print(f"   Predicted: {predicted_disease}")
        print(f"   Confidence: {confidence_pct:.2f}%")
        print(f"   All predictions: {all_preds}")
        
        # Confidence threshold: 70%
        CONFIDENCE_THRESHOLD = 70.0
        
        # Get ayurvedic treatment
        treatment = get_ayurvedic_treatment(predicted_disease, confidence_pct)
        
        # Transform to frontend expected format
        ayurvedic_recommendations = {
            "herbs_oils": treatment.get("herbal_remedies", []),
            "diet": treatment.get("dietary_recommendations", []),
            "lifestyle": treatment.get("lifestyle_changes", []),
            "home_care": []  # Can add home care tips if needed
        }
        
        # Determine dosha association (simplified)
        dosha_map = {
            "Alopecia Areata": "Vata-Pitta",
            "Contact Dermatitis": "Pitta-Kapha",
            "Folliculitis": "Pitta",
            "Head Lice": "Kapha",
            "Lichen Planus": "Pitta",
            "Male Pattern Baldness": "Vata-Pitta",
            "Psoriasis": "Vata-Kapha",
            "Seborrheic Dermatitis": "Kapha-Pitta",
            "Telogen Effluvium": "Vata",
            "Tinea Capitis": "Kapha"
        }
        dosha = dosha_map.get(predicted_disease, "Unknown")
        
        # Determine severity
        if confidence_pct >= 80:
            severity = "High confidence"
        elif confidence_pct >= CONFIDENCE_THRESHOLD:
            severity = "Moderate confidence"
        else:
            severity = "Low confidence - recommend professional consultation"
        
        if confidence_pct >= CONFIDENCE_THRESHOLD:
            # Confident prediction
            return HairDiseaseResult(
                detected_condition=predicted_disease,
                confidence=round(confidence_pct, 2),
                description=f"Detected {predicted_disease}. This condition affects the scalp and hair follicles.",
                status="confident",
                message=f"High confidence detection. The model is {confidence_pct:.1f}% confident this is {predicted_disease}.",
                all_predictions=all_preds,
                ayurvedic_recommendations=ayurvedic_recommendations,
                dosha_association=dosha,
                severity=severity,
                when_to_consult="If symptoms persist or worsen after 2-3 weeks, consult a dermatologist or trichologist."
            )
        else:
            # Uncertain prediction
            return HairDiseaseResult(
                detected_condition=f"Uncertain (suggests: {predicted_disease})",
                confidence=round(confidence_pct, 2),
                description="This image may not match the trained disease categories. Please consult a dermatologist or trichologist for accurate diagnosis.",
                status="uncertain",
                message=f"Low confidence ({confidence_pct:.1f}%). This image may not match the trained disease categories. Please consult a specialist for accurate diagnosis.",
                all_predictions=all_preds,
                ayurvedic_recommendations=ayurvedic_recommendations,
                dosha_association=dosha,
                severity=severity,
                when_to_consult="Immediately consult a dermatologist or trichologist for proper diagnosis and treatment."
            )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing image: {str(e)}")

@router.get("/conditions")
async def get_conditions():
    """Get list of detectable hair conditions (frontend expects this endpoint)"""
    
    if not MODEL_LOADED:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    # Format conditions as list of objects with id and name
    conditions = []
    for idx, name in class_mapping.items():
        conditions.append({
            "id": idx,
            "name": name
        })
    
    return {
        "conditions": conditions,
        "total": len(conditions)
    }

@router.get("/diseases")
async def get_diseases():
    """Get list of detectable hair diseases"""
    
    if not MODEL_LOADED:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return {
        "diseases": list(class_mapping.values()),
        "total": len(class_mapping),
        "categories": {
            "autoimmune": ["Alopecia Areata", "Lichen Planus"],
            "inflammatory": ["Contact Dermatitis", "Seborrheic Dermatitis", "Psoriasis"],
            "infectious": ["Folliculitis", "Head Lice", "Tinea Capitis"],
            "hair_loss": ["Male Pattern Baldness", "Telogen Effluvium"]
        },
        "model_info": {
            "architecture": "ResNet50",
            "accuracy": "100%",
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
