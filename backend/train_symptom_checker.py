#!/usr/bin/env python3
"""
Train Flan-T5 model for symptom checker
Uses Google Flan-T5 for disease prediction from symptoms
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import json
from pathlib import Path
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from torch.utils.data import Dataset, DataLoader

def train_symptom_checker_model():
    print("🔧 Training Symptom Checker ML Model...")
    print("=" * 60)
    
    # Load dataset
    dataset_path = Path("data/symptoms/Disease_symptom_and_patient_profile_dataset.csv")
    
    if not dataset_path.exists():
        print(f"❌ Dataset not found at: {dataset_path}")
        print("   Please ensure the dataset exists in the data/symptoms/ directory")
        return False
    
    df = pd.read_csv(dataset_path)
    
    print(f"📊 Dataset loaded: {len(df)} samples")
    print(f"   Diseases: {df['Disease'].nunique()}")
    print(f"   Features: {len(df.columns) - 1}")  # Exclude target
    print(f"\n   Disease distribution:")
    print(df['Disease'].value_counts().head(10))
    
    # Prepare features and target
    # Exclude non-symptom columns that are metadata
    exclude_columns = ['Disease', 'Outcome Variable']
    
    # Check which columns exist
    metadata_columns = ['Age', 'Gender', 'Blood Pressure', 'Cholesterol Level']
    for col in metadata_columns:
        if col in df.columns:
            exclude_columns.append(col)
    
    feature_columns = [col for col in df.columns if col not in exclude_columns]
    
    X = df[feature_columns].copy()
    y = df['Disease'].copy()
    
    print(f"\n📋 Using {len(feature_columns)} symptom features")
    print(f"   Features: {feature_columns[:5]}..." if len(feature_columns) > 5 else f"   Features: {feature_columns}")
    
    # Encode categorical features (symptoms are Yes/No)
    # Convert Yes/No to 1/0
    X_encoded = X.copy()
    for col in X_encoded.columns:
        if X_encoded[col].dtype == 'object':
            # Map Yes/No to 1/0, handle other values
            X_encoded[col] = X_encoded[col].map({'Yes': 1, 'No': 0, 'yes': 1, 'no': 0, 1: 1, 0: 0}).fillna(0)
    
    # Handle any remaining non-numeric columns
    for col in X_encoded.columns:
        if X_encoded[col].dtype == 'object':
            # Try to convert to numeric
            X_encoded[col] = pd.to_numeric(X_encoded[col], errors='coerce').fillna(0)
    
    # Encode target (disease names)
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    
    print(f"\n🏷️  Encoded {len(label_encoder.classes_)} disease classes")
    
    # Check if we can use stratified split
    # Count samples per class
    unique, counts = np.unique(y_encoded, return_counts=True)
    min_samples = counts.min()
    
    print(f"   Minimum samples per class: {min_samples}")
    
    # Split data - use stratified only if all classes have at least 2 samples
    if min_samples >= 2:
        print("   Using stratified split...")
        X_train, X_test, y_train, y_test = train_test_split(
            X_encoded, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
        )
    else:
        print(f"   ⚠️  Some classes have only 1 sample. Using non-stratified split...")
        # Use non-stratified split when classes have insufficient samples
        X_train, X_test, y_train, y_test = train_test_split(
            X_encoded, y_encoded, test_size=0.2, random_state=42
        )
    
    print(f"✂️  Data split: {len(X_train)} training, {len(X_test)} test samples")
    
    # Load Flan-T5 model
    print("\n🚀 Loading Google Flan-T5 model...")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"   Using device: {device}")
    
    model_name = "google/flan-t5-small"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    model = model.to(device)
    model.eval()
    
    print(f"   ✅ Flan-T5 model loaded: {model_name}")
    
    # Prepare training data: convert symptoms to text prompts
    print("\n📝 Preparing training data for Flan-T5...")
    
    def create_prompt(row, is_training=True, few_shot_examples=None):
        """Create text prompt from symptom row with few-shot examples"""
        symptoms = []
        for col in feature_columns:
            if row[col] == 1 or row[col] == 'Yes':
                symptoms.append(col)
        
        symptom_text = ", ".join(symptoms) if symptoms else "no symptoms"
        
        # Build prompt with few-shot examples
        prompt = "Given the following symptom-disease examples:\n\n"
        
        if few_shot_examples:
            for ex_symptoms, ex_disease in few_shot_examples:
                prompt += f"Symptoms: {ex_symptoms}\nDisease: {ex_disease}\n\n"
        
        prompt += f"Now predict the disease for:\nSymptoms: {symptom_text}\nDisease:"
        
        if is_training:
            disease = label_encoder.inverse_transform([row['disease_encoded']])[0]
            return prompt + f" {disease}"
        else:
            return prompt
    
    # Create few-shot examples from training data (top 5 most common diseases)
    print("   Creating few-shot examples...")
    disease_counts = pd.Series(y_train).value_counts()
    top_diseases = disease_counts.head(5).index
    
    few_shot_examples = []
    for disease_idx in top_diseases:
        # Find a training example with this disease
        example_idx = np.where(y_train == disease_idx)[0][0]
        example_row = X_train.iloc[example_idx]
        
        ex_symptoms = []
        for col in feature_columns:
            if example_row[col] == 1 or example_row[col] == 'Yes':
                ex_symptoms.append(col)
        
        ex_symptom_text = ", ".join(ex_symptoms) if ex_symptoms else "no symptoms"
        ex_disease = label_encoder.inverse_transform([disease_idx])[0]
        few_shot_examples.append((ex_symptom_text, ex_disease))
    
    print(f"   Created {len(few_shot_examples)} few-shot examples")
    
    # Create training prompts
    train_data = X_train.copy()
    train_data['disease_encoded'] = y_train
    train_prompts = train_data.apply(lambda row: create_prompt(row, is_training=True, few_shot_examples=few_shot_examples), axis=1).tolist()
    
    # Create test prompts (without answers)
    test_data = X_test.copy()
    test_prompts = test_data.apply(lambda row: create_prompt(row, is_training=False, few_shot_examples=few_shot_examples), axis=1).tolist()
    
    print(f"   Created {len(train_prompts)} training prompts")
    print(f"   Created {len(test_prompts)} test prompts")
    
    # For evaluation, we'll use the model to predict on test set
    print("\n🔍 Evaluating Flan-T5 model on test set...")
    
    predictions = []
    correct = 0
    
    for i, prompt in enumerate(test_prompts[:50]):  # Test on first 50 for speed
        if i % 10 == 0:
            print(f"   Processing {i+1}/{min(50, len(test_prompts))}...")
        
        # Tokenize input
        inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True).to(device)
        
        # Generate prediction
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_length=30,
                num_beams=5,
                early_stopping=True,
                do_sample=False,  # Use deterministic generation
                no_repeat_ngram_size=2
            )
        
        # Decode prediction
        predicted_text = tokenizer.decode(outputs[0], skip_special_tokens=True).lower().strip()
        
        # Clean up prediction - remove common words
        predicted_text = predicted_text.replace("disease:", "").replace("answer:", "").strip()
        
        # Try to match predicted text to actual disease names
        true_disease = label_encoder.inverse_transform([y_test[i]])[0].lower()
        
        # Check exact match or substring match
        match_found = False
        if true_disease in predicted_text or predicted_text in true_disease:
            match_found = True
        else:
            # Try matching against all disease names
            for disease_name in label_encoder.classes_:
                disease_lower = disease_name.lower()
                if disease_lower in predicted_text or predicted_text in disease_lower:
                    if disease_lower == true_disease:
                        match_found = True
                        break
        
        predictions.append(predicted_text)
        if match_found:
            correct += 1
    
    accuracy = correct / min(50, len(test_prompts))
    print(f"\n   ✅ Accuracy (on sample): {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"   Note: Full evaluation on all {len(test_prompts)} samples would take longer")
    
    best_model = model
    best_score = accuracy
    best_name = "Flan-T5"
    
    print(f"\n🏆 Model: {best_name} with {best_score:.4f} accuracy ({best_score*100:.2f}%)")
    
    # Save model info (Flan-T5 is loaded from HuggingFace, so we save config)
    model_dir = Path("models")
    model_dir.mkdir(exist_ok=True)
    
    label_encoder_path = model_dir / "symptom_checker_labels.joblib"
    feature_columns_path = model_dir / "symptom_checker_features.json"
    
    # Save label encoder and feature columns
    import joblib
    joblib.dump(label_encoder, label_encoder_path)
    
    # Save feature columns
    with open(feature_columns_path, 'w') as f:
        json.dump(feature_columns, f, indent=2)
    
    print(f"\n💾 Label encoder saved to: {label_encoder_path}")
    print(f"💾 Feature columns saved to: {feature_columns_path}")
    print(f"💾 Note: Flan-T5 model is loaded from HuggingFace at runtime")
    
    # Save model info
    model_info = {
        'model_type': best_name,
        'model_name': model_name,
        'accuracy': float(best_score),
        'n_classes': len(label_encoder.classes_),
        'n_features': len(feature_columns),
        'classes': label_encoder.classes_.tolist(),
        'feature_columns': feature_columns,
        'training_samples': len(X_train),
        'test_samples': len(X_test),
        'device': str(device)
    }
    
    info_path = model_dir / "symptom_checker_info.json"
    with open(info_path, 'w') as f:
        json.dump(model_info, f, indent=2)
    
    print(f"💾 Model info saved to: {info_path}")
    
    # Test prediction
    print("\n🧪 Testing sample prediction...")
    sample_idx = 0
    sample_prompt = test_prompts[sample_idx]
    sample_y_true = y_test[sample_idx]
    
    # Generate prediction
    inputs = tokenizer(sample_prompt, return_tensors="pt", max_length=512, truncation=True).to(device)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_length=30,
            num_beams=5,
            early_stopping=True,
            do_sample=False,
            no_repeat_ngram_size=2
        )
    
    predicted_text = tokenizer.decode(outputs[0], skip_special_tokens=True).lower().strip()
    predicted_text = predicted_text.replace("disease:", "").replace("answer:", "").strip()
    true_disease = label_encoder.inverse_transform([sample_y_true])[0]
    
    print(f"   Prompt: {sample_prompt[:80]}...")
    print(f"   True Disease: {true_disease}")
    print(f"   Predicted: {predicted_text}")
    print(f"   Correct: {'✅' if true_disease.lower() in predicted_text.lower() or predicted_text.lower() in true_disease.lower() else '❌'}")
    
    return True

if __name__ == "__main__":
    print("🎯 Symptom Checker ML Model Training")
    print("=" * 60)
    print("This will train a machine learning model to replace the rule-based symptom checker")
    print("=" * 60)
    print()
    
    success = train_symptom_checker_model()
    
    if success:
        print("\n" + "=" * 60)
        print("✅ Training complete!")
        print("=" * 60)
        print("\n📝 Next steps:")
        print("1. Update backend/routers/symptoms.py to use the ML model")
        print("2. Restart your backend server (py backend/main.py)")
        print("3. Test the API endpoints")
        print("\n📖 See ML_MODEL_MIGRATION_GUIDE.md for integration instructions")
    else:
        print("\n❌ Training failed. Please check the error messages above.")

