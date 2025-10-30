from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

router = APIRouter()

# Load Flan-T5 model for dosha analysis
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
tokenizer = None
model = None

def load_flan_t5():
    """Load Google's Flan-T5 model"""
    global tokenizer, model
    try:
        print("Loading Flan-T5 model...")
        # Using smaller model for faster inference
        model_name = "google/flan-t5-small"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        model = model.to(device)
        model.eval()
        print(f"✅ Flan-T5 model loaded on {device}")
        return True
    except Exception as e:
        print(f"❌ Error loading Flan-T5 model: {e}")
        return False

# Load model on startup
MODEL_LOADED = load_flan_t5()

class DoshaAnswers(BaseModel):
    body_frame: str
    skin_type: str
    digestion: str
    sleep_pattern: str
    stress_response: str
    climate_preference: str
    energy_level: str
    appetite: str
    mental_state: str
    physical_activity: str

class DoshaResult(BaseModel):
    vata: float
    pitta: float
    kapha: float
    dominant_dosha: str
    secondary_dosha: str
    dosha_description: str
    health_recommendations: List[str]
    dietary_guidelines: List[str]
    lifestyle_tips: List[str]
    warning_signs: List[str]

def calculate_dosha_scores(answers: Dict[str, str]) -> Dict[str, float]:
    """Calculate dosha scores based on answers"""
    
    # Scoring system for each answer
    dosha_mapping = {
        # Body Frame
        "thin": {"vata": 2, "pitta": 0, "kapha": 0},
        "medium": {"vata": 0, "pitta": 2, "kapha": 0},
        "large": {"vata": 0, "pitta": 0, "kapha": 2},
        
        # Skin Type
        "dry": {"vata": 2, "pitta": 0, "kapha": 0},
        "sensitive": {"vata": 0, "pitta": 2, "kapha": 0},
        "oily": {"vata": 0, "pitta": 0, "kapha": 2},
        
        # Digestion
        "irregular": {"vata": 2, "pitta": 0, "kapha": 0},
        "strong": {"vata": 0, "pitta": 2, "kapha": 0},
        "slow": {"vata": 0, "pitta": 0, "kapha": 2},
        
        # Sleep Pattern
        "light": {"vata": 2, "pitta": 0, "kapha": 0},
        "moderate": {"vata": 0, "pitta": 2, "kapha": 0},
        "deep": {"vata": 0, "pitta": 0, "kapha": 2},
        
        # Stress Response
        "anxious": {"vata": 2, "pitta": 0, "kapha": 0},
        "irritable": {"vata": 0, "pitta": 2, "kapha": 0},
        "withdrawn": {"vata": 0, "pitta": 0, "kapha": 2},
        
        # Climate Preference
        "warm": {"vata": 2, "pitta": 0, "kapha": 0},
        "cool": {"vata": 0, "pitta": 2, "kapha": 0},
        "moderate_temp": {"vata": 0, "pitta": 0, "kapha": 2},
        
        # Energy Level
        "variable": {"vata": 2, "pitta": 0, "kapha": 0},
        "high": {"vata": 0, "pitta": 2, "kapha": 0},
        "steady": {"vata": 0, "pitta": 0, "kapha": 2},
        
        # Appetite
        "irregular_appetite": {"vata": 2, "pitta": 0, "kapha": 0},
        "strong_appetite": {"vata": 0, "pitta": 2, "kapha": 0},
        "steady_appetite": {"vata": 0, "pitta": 0, "kapha": 2},
        
        # Mental State
        "creative": {"vata": 2, "pitta": 0, "kapha": 0},
        "focused": {"vata": 0, "pitta": 2, "kapha": 0},
        "calm": {"vata": 0, "pitta": 0, "kapha": 2},
        
        # Physical Activity
        "quick_movements": {"vata": 2, "pitta": 0, "kapha": 0},
        "purposeful": {"vata": 0, "pitta": 2, "kapha": 0},
        "slow_steady": {"vata": 0, "pitta": 0, "kapha": 2},
    }
    
    scores = {"vata": 0, "pitta": 0, "kapha": 0}
    
    for answer in answers.values():
        if answer in dosha_mapping:
            for dosha, points in dosha_mapping[answer].items():
                scores[dosha] += points
    
    # Normalize to percentages
    total = sum(scores.values())
    if total > 0:
        scores = {k: round((v / total) * 100, 1) for k, v in scores.items()}
    
    return scores

def generate_recommendations_with_flan_t5(dominant_dosha: str, secondary_dosha: str) -> Dict[str, List[str]]:
    """Use Flan-T5 to generate personalized recommendations"""
    
    if not MODEL_LOADED:
        # Fallback recommendations if model not loaded
        return get_default_recommendations(dominant_dosha)
    
    try:
        # Craft prompts for Flan-T5
        prompts = {
            "health": f"List 3 important health recommendations for someone with {dominant_dosha} dosha dominance in Ayurveda:",
            "diet": f"List 3 dietary guidelines for balancing {dominant_dosha} dosha in Ayurveda:",
            "lifestyle": f"List 3 lifestyle tips for someone with {dominant_dosha}-{secondary_dosha} dosha combination:",
            "warnings": f"List 3 warning signs of {dominant_dosha} imbalance in Ayurvedic medicine:"
        }
        
        recommendations = {}
        
        for key, prompt in prompts.items():
            inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True).to(device)
            
            with torch.no_grad():
                outputs = model.generate(
                    **inputs,
                    max_length=200,
                    min_length=20,
                    num_beams=5,
                    early_stopping=True,
                    temperature=0.8,
                    do_sample=True,
                    top_k=50,
                    top_p=0.95,
                    repetition_penalty=1.2,
                    no_repeat_ngram_size=3
                )
            
            response = tokenizer.decode(outputs[0], skip_special_tokens=True)
            # Split into list items
            items = [item.strip() for item in response.split('\n') if item.strip()]
            recommendations[key] = items[:3] if items else get_default_recommendations(dominant_dosha)[key]
        
        return {
            "health_recommendations": recommendations.get("health", []),
            "dietary_guidelines": recommendations.get("diet", []),
            "lifestyle_tips": recommendations.get("lifestyle", []),
            "warning_signs": recommendations.get("warnings", [])
        }
    
    except Exception as e:
        print(f"Error generating recommendations with Flan-T5: {e}")
        return get_default_recommendations(dominant_dosha)

def get_default_recommendations(dominant_dosha: str) -> Dict[str, List[str]]:
    """Fallback recommendations if LLM fails"""
    
    recommendations = {
        "Vata": {
            "health_recommendations": [
                "Maintain a regular daily routine to ground Vata energy",
                "Practice calming activities like yoga, meditation, and tai chi",
                "Keep warm and avoid cold, windy environments"
            ],
            "dietary_guidelines": [
                "Eat warm, cooked, nourishing foods",
                "Include healthy fats like ghee, olive oil, and avocado",
                "Favor sweet, sour, and salty tastes; reduce bitter, pungent, astringent"
            ],
            "lifestyle_tips": [
                "Get adequate sleep (7-8 hours) with consistent bedtime",
                "Practice oil massage (abhyanga) with warm sesame oil",
                "Avoid excessive travel, multitasking, and overstimulation"
            ],
            "warning_signs": [
                "Anxiety, worry, or restlessness",
                "Constipation, gas, or bloating",
                "Dry skin, hair, or joints; insomnia"
            ]
        },
        "Pitta": {
            "health_recommendations": [
                "Stay cool and avoid excessive heat exposure",
                "Practice moderation and avoid overworking",
                "Cultivate patience and avoid perfectionism"
            ],
            "dietary_guidelines": [
                "Eat cooling foods like cucumbers, coconut, and leafy greens",
                "Avoid spicy, fried, and acidic foods",
                "Favor sweet, bitter, and astringent tastes"
            ],
            "lifestyle_tips": [
                "Engage in cooling activities like swimming",
                "Practice stress management techniques",
                "Spend time in nature, especially near water"
            ],
            "warning_signs": [
                "Irritability, anger, or impatience",
                "Heartburn, acid reflux, or inflammation",
                "Skin rashes, acne, or excessive sweating"
            ]
        },
        "Kapha": {
            "health_recommendations": [
                "Stay active with regular vigorous exercise",
                "Avoid oversleeping and maintain an active lifestyle",
                "Seek variety and new experiences"
            ],
            "dietary_guidelines": [
                "Eat light, warm, and stimulating foods",
                "Favor pungent, bitter, and astringent tastes",
                "Reduce heavy, oily, and sweet foods"
            ],
            "lifestyle_tips": [
                "Wake up early (before 6 AM) to avoid sluggishness",
                "Practice energizing activities like cardio and dancing",
                "Avoid daytime napping"
            ],
            "warning_signs": [
                "Lethargy, depression, or mental fog",
                "Weight gain and slow metabolism",
                "Congestion, excess mucus, or water retention"
            ]
        }
    }
    
    return recommendations.get(dominant_dosha, recommendations["Vata"])

@router.post("/analyze", response_model=DoshaResult)
async def analyze_dosha(answers: DoshaAnswers):
    """Analyze dosha based on questionnaire answers"""
    
    # Calculate dosha scores
    scores = calculate_dosha_scores(answers.dict())
    
    # Determine dominant and secondary doshas
    sorted_doshas = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    dominant_dosha = sorted_doshas[0][0].capitalize()
    secondary_dosha = sorted_doshas[1][0].capitalize()
    
    # Dosha descriptions
    descriptions = {
        "Vata": "The energy of movement - governs breathing, blinking, muscle and tissue movement, pulsation of the heart, and cellular mobility.",
        "Pitta": "The energy of digestion and metabolism - governs digestion, absorption, nutrition, metabolism, and body temperature.",
        "Kapha": "The energy of lubrication and structure - governs growth, adding structure unit by unit, and providing protective cushioning."
    }
    
    # Generate recommendations using Flan-T5
    recommendations = generate_recommendations_with_flan_t5(dominant_dosha, secondary_dosha)
    
    return DoshaResult(
        vata=scores["vata"],
        pitta=scores["pitta"],
        kapha=scores["kapha"],
        dominant_dosha=dominant_dosha,
        secondary_dosha=secondary_dosha,
        dosha_description=descriptions[dominant_dosha],
        health_recommendations=recommendations["health_recommendations"],
        dietary_guidelines=recommendations["dietary_guidelines"],
        lifestyle_tips=recommendations["lifestyle_tips"],
        warning_signs=recommendations["warning_signs"]
    )

@router.get("/health")
async def health_check():
    """Check if Flan-T5 model is loaded"""
    return {
        "status": "healthy" if MODEL_LOADED else "degraded",
        "model_loaded": MODEL_LOADED,
        "model": "google/flan-t5-small",
        "device": str(device)
    }
