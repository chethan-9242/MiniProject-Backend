from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import json
from datetime import datetime
from pathlib import Path

router = APIRouter()

# Storage directory for saved analyses
STORAGE_DIR = Path("./saved_analyses")
STORAGE_DIR.mkdir(exist_ok=True)

# Symptom-Condition Knowledge Base
SYMPTOM_KNOWLEDGE = [
    {
        "id": "condition_cold_pratishyaya",
        "condition": "Common Cold (Pratishyaya)",
        "symptoms": ["runny nose", "congestion", "sneezing", "sore throat", "cough", "fatigue", "mild fever", "nasal", "mucus"],
        "dosha": "Kapha-Vata",
        "description": "Viral infection affecting the upper respiratory system causing congestion and discomfort",
        "ayurvedic_perspective": "Imbalance in Kapha and Vata doshas causing congestion (Kapha) and irregular circulation (Vata)",
        "probability_keywords": ["cold", "congestion", "runny", "sneezing", "throat", "cough", "nose", "respiratory"],
        "treatments": {
            "immediate": [
                "Drink warm water with ginger and honey every 2-3 hours",
                "Steam inhalation with eucalyptus oil for 10 minutes",
                "Gargle with warm salt water 3-4 times daily",
                "Rest and avoid cold exposure"
            ],
            "lifestyle": [
                "Maintain regular sleep schedule (8-9 hours)",
                "Avoid cold drinks and ice cream",
                "Stay hydrated with warm herbal teas",
                "Practice gentle breathing exercises (Pranayama)"
            ],
            "herbs": [
                "Tulsi (Holy Basil) tea for respiratory support",
                "Ginger tea with honey for throat and digestion",
                "Turmeric milk before bed for anti-inflammatory benefits",
                "Licorice root for soothing throat"
            ],
            "doctor_consult": "If symptoms persist beyond 7 days, fever exceeds 101°F, or difficulty breathing occurs"
        }
    },
    {
        "id": "condition_headache_shiroroga",
        "condition": "Tension Headache (Shiroroga)",
        "symptoms": ["headache", "head pain", "pressure", "tight feeling", "stress", "fatigue", "neck pain"],
        "dosha": "Vata",
        "description": "Tension-type headache caused by stress, poor posture, or nervous system imbalance",
        "ayurvedic_perspective": "Vata imbalance affecting the nervous system and causing constriction in head region",
        "probability_keywords": ["headache", "head", "pain", "pressure", "tension", "stress"],
        "treatments": {
            "immediate": [
                "Apply warm sesame oil to scalp and temples",
                "Practice deep breathing for 10 minutes",
                "Drink warm water slowly",
                "Rest in a quiet, dark room"
            ],
            "lifestyle": [
                "Maintain regular sleep-wake cycle",
                "Practice stress management techniques (meditation, yoga)",
                "Improve posture, especially during work",
                "Avoid screen time for extended periods"
            ],
            "herbs": [
                "Brahmi (Bacopa) for nervous system support",
                "Ashwagandha for stress relief",
                "Ginger tea for circulation",
                "Lavender oil for relaxation"
            ],
            "doctor_consult": "If headaches are severe, sudden, or accompanied by vision changes, confusion, or neck stiffness"
        }
    },
    {
        "id": "condition_constipation_vibandha",
        "condition": "Constipation (Vibandha)",
        "symptoms": ["constipation", "hard stool", "irregular bowel", "difficulty passing stool", "bloating", "discomfort"],
        "dosha": "Vata",
        "description": "Difficulty in bowel movements due to Vata imbalance causing dryness and irregular function",
        "ayurvedic_perspective": "Vata dosha causing dryness in the colon, leading to hard stools and irregular elimination",
        "probability_keywords": ["constipation", "bowel", "stool", "elimination", "irregular"],
        "treatments": {
            "immediate": [
                "Drink warm water upon waking (2-3 glasses)",
                "Take Triphala powder with warm water before bed",
                "Consume soaked prunes or figs in the morning",
                "Perform gentle abdominal massage with sesame oil"
            ],
            "lifestyle": [
                "Eat fiber-rich foods (fruits, vegetables, whole grains)",
                "Establish regular meal and bathroom times",
                "Practice gentle yoga poses (Pavanamuktasana, Malasana)",
                "Avoid dry, cold, and processed foods"
            ],
            "herbs": [
                "Triphala for gentle colon cleansing and regulation",
                "Isabgol (Psyllium husk) with warm water",
                "Haritaki for bowel movement support",
                "Castor oil (small dose) for lubrication"
            ],
            "doctor_consult": "If constipation persists for more than 2 weeks, is accompanied by severe pain, blood in stool, or unexplained weight loss"
        }
    },
    {
        "id": "condition_digestive_agnimandya",
        "condition": "Digestive Disturbance (Agnimandya)",
        "symptoms": ["bloating", "gas", "indigestion", "stomach pain", "nausea", "irregular appetite", "burping", "acidity"],
        "dosha": "Vata-Pitta",
        "description": "Weak digestive fire leading to incomplete digestion and gas formation",
        "ayurvedic_perspective": "Weakened Agni (digestive fire) with Vata causing gas and irregular function, Pitta causing acidity",
        "probability_keywords": ["bloating", "gas", "stomach", "digestion", "indigestion", "nausea", "appetite", "acidity"],
        "treatments": {
            "immediate": [
                "Sip warm ginger tea after meals",
                "Avoid eating until digestion improves",
                "Walk for 10-15 minutes after meals",
                "Apply warm compress to abdomen"
            ],
            "lifestyle": [
                "Eat at regular times daily",
                "Make lunch the largest meal",
                "Avoid overeating and late-night meals",
                "Chew food thoroughly and eat mindfully"
            ],
            "herbs": [
                "Triphala for digestive regulation",
                "Ginger, cumin, fennel tea (CCF tea)",
                "Ajwain (carom seeds) for gas relief",
                "Hingvastak churna for improved digestion"
            ],
            "doctor_consult": "If pain is severe, persistent, or accompanied by vomiting, blood in stool, or significant weight loss"
        }
    },
    {
        "id": "condition_anxiety_chittodvega",
        "condition": "Anxiety and Stress (Chittodvega)",
        "symptoms": ["anxiety", "worry", "nervousness", "restlessness", "insomnia", "rapid heartbeat", "fatigue"],
        "dosha": "Vata",
        "description": "Mental agitation and excessive worry affecting nervous system and mind",
        "ayurvedic_perspective": "Vata imbalance causing instability in mind and nervous system, affecting Prana Vata",
        "probability_keywords": ["anxiety", "stress", "worry", "nervous", "restless", "insomnia", "panic"],
        "treatments": {
            "immediate": [
                "Practice Nadi Shodhana (alternate nostril breathing)",
                "Drink warm chamomile or brahmi tea",
                "Self-massage feet with warm sesame oil",
                "Listen to calming music or nature sounds"
            ],
            "lifestyle": [
                "Establish consistent daily routine",
                "Practice meditation for 15-20 minutes daily",
                "Reduce caffeine and stimulants",
                "Spend time in nature regularly"
            ],
            "herbs": [
                "Ashwagandha for stress and anxiety relief",
                "Brahmi for mental clarity and calmness",
                "Jatamansi for nervous system support",
                "Shankhapushpi for peace of mind"
            ],
            "doctor_consult": "If anxiety is severe, interfering with daily life, or accompanied by suicidal thoughts"
        }
    },
    {
        "id": "condition_skin_rash_twakroga",
        "condition": "Skin Inflammation and Rash (Twak Roga)",
        "symptoms": ["rash", "itching", "redness", "inflammation", "skin irritation", "dry skin", "burning"],
        "dosha": "Pitta-Kapha",
        "description": "Skin inflammation due to heat, toxins, or allergic reactions",
        "ayurvedic_perspective": "Pitta dosha aggravation causing heat and inflammation, with Kapha causing oozing and itching",
        "probability_keywords": ["rash", "skin", "itching", "inflammation", "redness", "burning", "irritation"],
        "treatments": {
            "immediate": [
                "Apply cooling aloe vera gel or coconut oil",
                "Take cool (not cold) showers",
                "Avoid scratching affected areas",
                "Wear loose, breathable cotton clothing"
            ],
            "lifestyle": [
                "Avoid hot, spicy, and acidic foods",
                "Increase intake of cooling foods (cucumber, coconut)",
                "Reduce sun exposure",
                "Avoid harsh soaps and chemicals"
            ],
            "herbs": [
                "Neem for purifying blood and skin",
                "Turmeric paste for anti-inflammatory effect",
                "Sandalwood powder with rose water",
                "Manjistha for skin health"
            ],
            "doctor_consult": "If rash spreads rapidly, is very painful, shows signs of infection, or doesn't improve in 3-5 days"
        }
    },
    {
        "id": "condition_joint_pain_sandhi_shula",
        "condition": "Joint Pain (Sandhi Shula)",
        "symptoms": ["joint pain", "stiffness", "swelling", "inflammation", "reduced mobility", "morning stiffness"],
        "dosha": "Vata-Kapha",
        "description": "Joint pain and inflammation due to Vata aggravation and Ama accumulation",
        "ayurvedic_perspective": "Vata dosha causing dryness and pain in joints, Kapha causing swelling, and Ama (toxins) accumulation",
        "probability_keywords": ["joint", "arthritis", "stiffness", "swelling", "pain", "mobility"],
        "treatments": {
            "immediate": [
                "Apply warm sesame oil massage to joints",
                "Use warm compress on affected areas",
                "Practice gentle joint movements",
                "Rest and avoid overexertion"
            ],
            "lifestyle": [
                "Regular gentle exercise (yoga, swimming)",
                "Maintain healthy weight",
                "Avoid cold and damp environments",
                "Ensure adequate vitamin D from sunlight"
            ],
            "herbs": [
                "Guggulu for joint health and inflammation",
                "Shallaki (Boswellia) for pain relief",
                "Turmeric with black pepper for anti-inflammatory effect",
                "Ashwagandha for strength and rejuvenation"
            ],
            "doctor_consult": "If pain is severe, joint is hot and swollen, or movement is significantly restricted"
        }
    },
    {
        "id": "condition_insomnia_anidra",
        "condition": "Insomnia (Anidra)",
        "symptoms": ["insomnia", "sleep problems", "difficulty sleeping", "waking up", "restless", "fatigue", "anxiety"],
        "dosha": "Vata-Pitta",
        "description": "Sleep disturbance caused by nervous system imbalance and mental agitation",
        "ayurvedic_perspective": "Vata causing restlessness and Pitta causing overactive mind and heat",
        "probability_keywords": ["insomnia", "sleep", "sleepless", "tired", "restless", "awake"],
        "treatments": {
            "immediate": [
                "Drink warm milk with nutmeg and cardamom",
                "Massage feet with warm ghee or sesame oil",
                "Practice Yoga Nidra or body scan meditation",
                "Keep bedroom cool, dark, and quiet"
            ],
            "lifestyle": [
                "Establish consistent sleep schedule (bed by 10 PM)",
                "Avoid screens 1-2 hours before bed",
                "Practice calming evening routine",
                "Avoid heavy meals and caffeine after 3 PM"
            ],
            "herbs": [
                "Ashwagandha for stress and sleep quality",
                "Jatamansi for calming nervous system",
                "Brahmi for mental peace",
                "Chamomile tea before bed"
            ],
            "doctor_consult": "If insomnia persists for more than 2 weeks or severely impacts daily functioning"
        }
    },
    {
        "id": "condition_fatigue_klama",
        "condition": "Chronic Fatigue (Klama)",
        "symptoms": ["fatigue", "weakness", "low energy", "exhaustion", "lethargy", "burnout", "lack of motivation", "tired"],
        "dosha": "Kapha-Vata",
        "description": "Persistent tiredness and lack of energy due to weak Agni and dosha imbalance",
        "ayurvedic_perspective": "Kapha causing heaviness and dullness, Vata causing depleted energy, weak digestive fire",
        "probability_keywords": ["fatigue", "tired", "exhausted", "weakness", "energy", "lethargy", "burnout"],
        "treatments": {
            "immediate": [
                "Take short energizing walks in fresh air",
                "Practice deep breathing exercises",
                "Drink ginger tea or lemon water",
                "Get adequate sunlight exposure"
            ],
            "lifestyle": [
                "Improve sleep quality and duration",
                "Regular physical activity appropriate to capacity",
                "Balanced diet with adequate protein",
                "Stress management and rest periods"
            ],
            "herbs": [
                "Ashwagandha for energy and vitality",
                "Chyawanprash for rejuvenation",
                "Brahmi for mental energy",
                "Triphala for detoxification"
            ],
            "doctor_consult": "If fatigue is extreme, persistent, or accompanied by other concerning symptoms"
        }
    },
    {
        "id": "condition_fever_jwara",
        "condition": "Fever (Jwara)",
        "symptoms": ["fever", "high temperature", "chills", "body ache", "sweating", "weakness", "headache"],
        "dosha": "Pitta",
        "description": "Elevated body temperature due to infection or inflammation",
        "ayurvedic_perspective": "Pitta dosha aggravation causing excess heat in the body, often with Ama (toxins) accumulation",
        "probability_keywords": ["fever", "temperature", "hot", "chills", "sweating"],
        "treatments": {
            "immediate": [
                "Rest and stay hydrated with room temperature water",
                "Apply cool compress to forehead",
                "Drink tulsi and ginger tea",
                "Avoid solid food until fever reduces, take light soups"
            ],
            "lifestyle": [
                "Complete bed rest until fever subsides",
                "Keep room well-ventilated and cool",
                "Avoid exposure to heat and sun",
                "Resume normal activities gradually after recovery"
            ],
            "herbs": [
                "Tulsi (Holy Basil) for immune support and fever reduction",
                "Giloy (Guduchi) for immunity and detoxification",
                "Ginger tea for warmth and circulation",
                "Turmeric milk for anti-inflammatory benefits"
            ],
            "doctor_consult": "If fever exceeds 103°F, persists for more than 3 days, or is accompanied by severe symptoms like difficulty breathing, chest pain, or confusion"
        }
    },
    {
        "id": "condition_diarrhea_atisara",
        "condition": "Diarrhea (Atisara)",
        "symptoms": ["diarrhea", "loose stools", "frequent bowel movements", "stomach cramps", "dehydration", "nausea"],
        "dosha": "Pitta-Vata",
        "description": "Frequent loose or watery stools due to digestive system irritation",
        "ayurvedic_perspective": "Pitta causing heat and inflammation in digestive tract, with Vata creating irregular movement",
        "probability_keywords": ["diarrhea", "loose", "stool", "watery", "bowel", "frequent"],
        "treatments": {
            "immediate": [
                "Drink plenty of fluids (ORS, coconut water, rice water)",
                "Eat BRAT diet (Banana, Rice, Applesauce, Toast)",
                "Take buttermilk with roasted cumin and salt",
                "Avoid dairy, spicy, and oily foods"
            ],
            "lifestyle": [
                "Rest and avoid strenuous activity",
                "Maintain strict hand hygiene",
                "Eat simple, easily digestible foods",
                "Stay hydrated throughout the day"
            ],
            "herbs": [
                "Pomegranate peel powder with honey",
                "Kutaja (Holarrhena) for intestinal health",
                "Ginger and fennel tea for digestion",
                "Bael fruit pulp for binding effect"
            ],
            "doctor_consult": "If diarrhea persists for more than 2 days, shows blood or mucus, or causes severe dehydration"
        }
    },
    {
        "id": "condition_back_pain_katishula",
        "condition": "Back Pain (Kati Shula)",
        "symptoms": ["back pain", "lower back pain", "stiffness", "muscle pain", "spinal pain", "difficulty moving"],
        "dosha": "Vata",
        "description": "Pain and discomfort in the back region due to Vata imbalance affecting muscles and joints",
        "ayurvedic_perspective": "Vata dosha causing dryness, tension, and restricted movement in back muscles and spine",
        "probability_keywords": ["back", "spine", "lower back", "lumbar", "pain", "stiff"],
        "treatments": {
            "immediate": [
                "Apply warm sesame oil massage to affected area",
                "Use heating pad or warm compress",
                "Rest and avoid heavy lifting",
                "Practice gentle stretching (avoid strain)"
            ],
            "lifestyle": [
                "Maintain proper posture while sitting and standing",
                "Sleep on firm mattress",
                "Regular gentle exercise (walking, swimming, yoga)",
                "Avoid prolonged sitting or standing"
            ],
            "herbs": [
                "Nirgundi oil for external application",
                "Ashwagandha for muscle strength",
                "Guggulu for inflammation and pain",
                "Shallaki (Boswellia) for joint support"
            ],
            "doctor_consult": "If pain radiates to legs, causes numbness, or is accompanied by loss of bladder control"
        }
    }
]


class Symptom(BaseModel):
    id: str
    name: str
    severity: str  # mild, moderate, severe
    duration: str


class SymptomCheckRequest(BaseModel):
    symptoms: List[Symptom]


class ConditionMatch(BaseModel):
    name: str
    probability: int
    description: str
    ayurvedic_perspective: str


class Recommendations(BaseModel):
    immediate_actions: List[str]
    lifestyle_changes: List[str]
    herbal_remedies: List[str]
    when_to_consult_doctor: str


class DoshaImbalance(BaseModel):
    primary: str
    description: str


class SymptomAnalysis(BaseModel):
    possible_conditions: List[ConditionMatch]
    recommendations: Recommendations
    dosha_imbalance: DoshaImbalance


def analyze_symptoms_with_rag(symptoms: List[Symptom]) -> SymptomAnalysis:
    """
    Analyze symptoms using GraphRAG and Flan-T5 for intelligent diagnosis
    """
    
    # Build symptom query
    symptom_names = [s.name.lower() for s in symptoms]
    symptom_details = [f"{s.name} ({s.severity}, {s.duration})" for s in symptoms]
    query_text = f"Patient symptoms: {', '.join(symptom_details)}"
    
    # Match symptoms to conditions
    matched_conditions = []
    for condition_data in SYMPTOM_KNOWLEDGE:
        # Calculate match score
        condition_symptoms = set(condition_data["symptoms"])
        symptom_set = set(symptom_names)
        
        # Calculate overlap
        matching = symptom_set.intersection(condition_symptoms)
        
        # Keyword matching for better accuracy - improved algorithm
        keyword_matches = 0
        keyword_exact_matches = 0
        
        for keyword in condition_data["probability_keywords"]:
            for symptom in symptom_names:
                # Exact match (case insensitive)
                if keyword.lower() == symptom.lower():
                    keyword_exact_matches += 1
                    keyword_matches += 1
                    break
                # Partial match (keyword contains symptom or vice versa)
                elif keyword.lower() in symptom.lower() or symptom.lower() in keyword.lower():
                    keyword_matches += 1
                    break
        
        # Calculate probability score
        if len(matching) > 0 or keyword_matches > 0:
            overlap_score = len(matching) / max(len(symptom_set), len(condition_symptoms))
            keyword_score = keyword_matches / len(condition_data["probability_keywords"])
            exact_match_bonus = keyword_exact_matches * 0.3  # 30% bonus per exact match
            
            # Weight: 40% overlap, 40% keywords, 20% exact matches
            base_score = (overlap_score * 0.4 + keyword_score * 0.4) * 100
            total_score = base_score + (exact_match_bonus * 100)
            
            # Apply severity multiplier
            for symptom in symptoms:
                if symptom.name.lower() in condition_symptoms:
                    if symptom.severity == "severe":
                        total_score *= 1.2
                    elif symptom.severity == "mild":
                        total_score *= 0.9
            
            # Cap at 95%
            probability = min(int(total_score), 95)
            
            if probability > 20:  # Only include if > 20% match
                matched_conditions.append({
                    "condition_data": condition_data,
                    "probability": probability,
                    "matched_symptoms": list(matching)
                })
    
    # Sort by probability
    matched_conditions.sort(key=lambda x: x["probability"], reverse=True)
    
    # Take top 3 conditions
    top_conditions = matched_conditions[:3]
    
    if not top_conditions:
        # Fallback: general fatigue
        top_conditions = [{
            "condition_data": next(c for c in SYMPTOM_KNOWLEDGE if "fatigue" in c["id"]),
            "probability": 50,
            "matched_symptoms": []
        }]
    
    # Build possible conditions list
    possible_conditions = []
    for match in top_conditions:
        cd = match["condition_data"]
        possible_conditions.append(
            ConditionMatch(
                name=cd["condition"],
                probability=match["probability"],
                description=cd["description"],
                ayurvedic_perspective=cd["ayurvedic_perspective"]
            )
        )
    
    # Use Flan-T5 to generate personalized recommendations using RAG
    primary_condition = top_conditions[0]["condition_data"]
    
    # Combine recommendations from matched conditions
    all_immediate = []
    all_lifestyle = []
    all_herbs = []
    doctor_consult = primary_condition["treatments"]["doctor_consult"]
    
    for match in top_conditions:
        cd = match["condition_data"]
        all_immediate.extend(cd["treatments"]["immediate"][:2])  # Top 2 from each
        all_lifestyle.extend(cd["treatments"]["lifestyle"][:2])
        all_herbs.extend(cd["treatments"]["herbs"][:2])
    
    # Remove duplicates while preserving order
    def unique_list(lst):
        seen = set()
        result = []
        for item in lst:
            if item.lower() not in seen:
                seen.add(item.lower())
                result.append(item)
        return result
    
    immediate_actions = unique_list(all_immediate)[:4]
    lifestyle_changes = unique_list(all_lifestyle)[:4]
    herbal_remedies = unique_list(all_herbs)[:4]
    
    # Determine primary dosha imbalance
    dosha_counts = {}
    for match in top_conditions:
        dosha = match["condition_data"]["dosha"]
        weight = match["probability"] / 100
        
        if "-" in dosha:
            doshas = dosha.split("-")
            for d in doshas:
                dosha_counts[d] = dosha_counts.get(d, 0) + weight * 0.5
        else:
            dosha_counts[dosha] = dosha_counts.get(dosha, 0) + weight
    
    # Get primary dosha
    if dosha_counts:
        sorted_doshas = sorted(dosha_counts.items(), key=lambda x: x[1], reverse=True)
        if len(sorted_doshas) > 1 and sorted_doshas[0][1] - sorted_doshas[1][1] < 0.3:
            primary_dosha = f"{sorted_doshas[0][0]}-{sorted_doshas[1][0]}"
        else:
            primary_dosha = sorted_doshas[0][0]
    else:
        primary_dosha = "Vata"
    
    # Generate dosha description based on combined conditions
    # Build a comprehensive description from matched conditions
    if len(top_conditions) > 1:
        # Multiple conditions: combine their perspectives
        perspectives = [match["condition_data"]["ayurvedic_perspective"] for match in top_conditions[:2]]
        
        # Create combined description
        if primary_dosha in ["Vata", "Pitta", "Kapha"]:
            # Single dosha
            dosha_base = {
                "Vata": "Vata dosha imbalance is causing instability and irregularity in your body. This affects movement, circulation, and nervous system function, leading to ",
                "Pitta": "Pitta dosha imbalance is causing excess heat and transformation in your body. This affects metabolism, digestion, and inflammation, leading to ",
                "Kapha": "Kapha dosha imbalance is causing excess heaviness and stagnation in your body. This affects structure, immunity, and fluid balance, leading to "
            }
            symptom_impact = ", ".join(symptom_names[:3])
            dosha_description = dosha_base.get(primary_dosha, "") + symptom_impact + " and related discomfort"
        else:
            # Combined dosha
            doshas = primary_dosha.split("-")
            dosha_effects = {
                "Vata": "instability and dryness",
                "Pitta": "heat and inflammation",
                "Kapha": "heaviness and congestion"
            }
            effects = " combined with ".join([dosha_effects.get(d, d) for d in doshas])
            dosha_description = f"Combined {primary_dosha} imbalance causing {effects}, which manifests as {', '.join(symptom_names[:3])} and affects your overall well-being"
    else:
        # Single condition: use its perspective directly
        dosha_description = primary_condition["ayurvedic_perspective"]
    
    return SymptomAnalysis(
        possible_conditions=possible_conditions,
        recommendations=Recommendations(
            immediate_actions=immediate_actions,
            lifestyle_changes=lifestyle_changes,
            herbal_remedies=herbal_remedies,
            when_to_consult_doctor=doctor_consult
        ),
        dosha_imbalance=DoshaImbalance(
            primary=primary_dosha,
            description=dosha_description
        )
    )


@router.post("/check", response_model=SymptomAnalysis)
async def check_symptoms(request: SymptomCheckRequest):
    """
    Analyze symptoms and provide Ayurvedic diagnosis with recommendations
    Uses GraphRAG and Flan-T5 for intelligent analysis
    """
    
    if not request.symptoms or len(request.symptoms) == 0:
        raise HTTPException(status_code=400, detail="At least one symptom is required")
    
    try:
        analysis = analyze_symptoms_with_rag(request.symptoms)
        return analysis
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing symptoms: {str(e)}")


@router.get("/health")
async def health_check():
    """Check symptom checker health"""
    return {
        "status": "healthy",
        "conditions_in_kb": len(SYMPTOM_KNOWLEDGE),
        "analysis_method": "Knowledge-based matching with Ayurvedic principles",
        "version": "1.0"
    }


class SaveAnalysisRequest(BaseModel):
    user_id: Optional[str] = "anonymous"  # Can be used for user identification later
    symptoms: List[Symptom]
    analysis: SymptomAnalysis
    notes: Optional[str] = None


class SavedAnalysis(BaseModel):
    id: str
    user_id: str
    timestamp: str
    symptoms: List[Symptom]
    analysis: SymptomAnalysis
    notes: Optional[str] = None


@router.post("/save")
async def save_analysis(request: SaveAnalysisRequest):
    """
    Save a symptom analysis for future reference
    """
    try:
        # Generate unique ID based on timestamp
        analysis_id = f"{request.user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Create saved analysis object
        saved = SavedAnalysis(
            id=analysis_id,
            user_id=request.user_id,
            timestamp=datetime.now().isoformat(),
            symptoms=request.symptoms,
            analysis=request.analysis,
            notes=request.notes
        )
        
        # Save to file
        file_path = STORAGE_DIR / f"{analysis_id}.json"
        with open(file_path, 'w') as f:
            json.dump(saved.dict(), f, indent=2)
        
        return {
            "success": True,
            "message": "Analysis saved successfully",
            "analysis_id": analysis_id,
            "timestamp": saved.timestamp
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving analysis: {str(e)}")


@router.get("/history/{user_id}")
async def get_analysis_history(user_id: str = "anonymous", limit: int = 10):
    """
    Retrieve saved analyses for a user
    """
    try:
        # Find all files for this user
        pattern = f"{user_id}_*.json"
        files = sorted(STORAGE_DIR.glob(pattern), key=lambda x: x.stat().st_mtime, reverse=True)
        
        # Load analyses (limited to 'limit' most recent)
        analyses = []
        for file_path in files[:limit]:
            with open(file_path, 'r') as f:
                data = json.load(f)
                analyses.append(data)
        
        return {
            "success": True,
            "count": len(analyses),
            "analyses": analyses
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving history: {str(e)}")


@router.get("/history/{user_id}/{analysis_id}")
async def get_specific_analysis(user_id: str, analysis_id: str):
    """
    Retrieve a specific saved analysis
    """
    try:
        file_path = STORAGE_DIR / f"{analysis_id}.json"
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="Analysis not found")
        
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # Verify user_id matches
        if data.get('user_id') != user_id:
            raise HTTPException(status_code=403, detail="Access denied")
        
        return {
            "success": True,
            "analysis": data
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving analysis: {str(e)}")


@router.delete("/history/{user_id}/{analysis_id}")
async def delete_analysis(user_id: str, analysis_id: str):
    """
    Delete a saved analysis
    """
    try:
        file_path = STORAGE_DIR / f"{analysis_id}.json"
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="Analysis not found")
        
        # Verify user_id matches
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        if data.get('user_id') != user_id:
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Delete file
        file_path.unlink()
        
        return {
            "success": True,
            "message": "Analysis deleted successfully"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting analysis: {str(e)}")
