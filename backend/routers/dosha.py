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
_PARSE_ERRS = 0

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

def generate_scores_with_flan_t5(answers: Dict[str, str]) -> Dict[str, float]:
    """Use Flan-T5 to infer dosha percentages from questionnaire answers.
    Returns dict with keys: vata, pitta, kapha (percentages summing ~100).
    """
    if not MODEL_LOADED:
        # Fallback to neutral distribution if model unavailable
        return {"vata": 33.3, "pitta": 33.3, "kapha": 33.3}

    # Build a compact, structured prompt and ask for strict JSON
    key_map = {
        "body_frame": "Body Frame",
        "skin_type": "Skin Type",
        "digestion": "Digestion",
        "sleep_pattern": "Sleep Pattern",
        "stress_response": "Stress Response",
        "climate_preference": "Climate Preference",
        "energy_level": "Energy Level",
        "appetite": "Appetite",
        "mental_state": "Mental State",
        "physical_activity": "Physical Activity",
    }
    pairs = [f"{key_map.get(k,k)}: {v}" for k, v in answers.items()]
    survey = "\n".join(pairs)

    # Few-shot prompt to force strict JSON output
    prompt = (
        "You are an Ayurvedic practitioner. Estimate dosha composition percentages (Vata, Pitta, Kapha) that sum to 100.\n"
        "Respond with STRICT JSON only. No prose, no labels, no extra text. Keys must be: vata, pitta, kapha. Values must be numbers.\n\n"
        "Example 1 Input:\n"
        "Body Frame: thin\nSkin Type: dry\nDigestion: irregular\nSleep Pattern: light\nStress Response: anxious\nClimate Preference: warm\nEnergy Level: variable\nAppetite: irregular_appetite\nMental State: creative\nPhysical Activity: quick_movements\n\n"
        "Example 1 Output:\n{\"vata\": 55.0, \"pitta\": 25.0, \"kapha\": 20.0}\n\n"
        "Example 2 Input:\n"
        "Body Frame: large\nSkin Type: oily\nDigestion: slow\nSleep Pattern: deep\nStress Response: withdrawn\nClimate Preference: moderate_temp\nEnergy Level: steady\nAppetite: steady_appetite\nMental State: calm\nPhysical Activity: slow_steady\n\n"
        "Example 2 Output:\n{\"vata\": 15.0, \"pitta\": 25.0, \"kapha\": 60.0}\n\n"
        "Now use the following questionnaire to produce ONLY a JSON object in the same format.\n\n"
        f"Questionnaire:\n{survey}\n\n"
        "Output JSON only:"
    )

    inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True).to(device)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_length=96,
            min_length=10,
            num_beams=1,
            early_stopping=True,
            do_sample=False,
            no_repeat_ngram_size=3,
        )
    text = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

    # Parse JSON robustly, with regex fallbacks
    import json, re
    try:
        json_text = text
        if "{" not in json_text:
            m = re.search(r"\{.*\}", text, re.DOTALL)
            if m:
                json_text = m.group(0)
        data = json.loads(json_text)
        v = float(data.get("vata", 0))
        p = float(data.get("pitta", 0))
        k = float(data.get("kapha", 0))
    except Exception:
        # Fallback 1: extract numbers near keywords
        def find_val(label: str) -> float | None:
            m = re.search(label + r"[^0-9\-]*([0-9]+(?:\.[0-9]+)?)", text, re.IGNORECASE)
            if m:
                try:
                    return float(m.group(1))
                except Exception:
                    return None
            return None
        v = find_val("vata")
        p = find_val("pitta")
        k = find_val("kapha")
        # Fallback 2: if any missing, grab first three numbers in order
        if v is None or p is None or k is None:
            nums = re.findall(r"([0-9]+(?:\.[0-9]+)?)", text)
            nums = [float(n) for n in nums[:3]]
            if v is None and len(nums) > 0:
                v = nums[0]
            if p is None and len(nums) > 1:
                p = nums[1]
            if k is None and len(nums) > 2:
                k = nums[2]
        # Fallback 3: if exactly two values present, infer the third as 100 - sum(present)
        present = {"vata": v, "pitta": p, "kapha": k}
        missing = [k_ for k_, val_ in present.items() if val_ is None]
        known_vals = [val_ for val_ in present.values() if val_ is not None]
        if len(missing) == 1 and len(known_vals) == 2:
            rem = 100.0 - sum(known_vals)
            # Clamp to [0, 100]
            rem = max(0.0, min(100.0, rem))
            if missing[0] == "vata":
                v = rem
            elif missing[0] == "pitta":
                p = rem
            else:
                k = rem
        # Final guard: defaults if still invalid
        if v is None or p is None or k is None:
            global _PARSE_ERRS
            if _PARSE_ERRS < 3:
                print(f"Failed to parse Flan-T5 dosha JSON/text; raw=\n{text}")
            _PARSE_ERRS += 1
            return {"vata": 33.3, "pitta": 33.3, "kapha": 33.3}
    # Normalize if needed
    s = (v or 0) + (p or 0) + (k or 0)
    if s <= 0:
        return {"vata": 33.3, "pitta": 33.3, "kapha": 33.3}
    v, p, k = 100.0 * v / s, 100.0 * p / s, 100.0 * k / s
    return {"vata": round(v, 1), "pitta": round(p, 1), "kapha": round(k, 1)}

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
    """Analyze dosha using Flan-T5 generated percentages from questionnaire answers"""
    
    # Generate dosha scores with Flan-T5
    scores = generate_scores_with_flan_t5(answers.dict())
    
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
