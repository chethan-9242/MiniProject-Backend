#!/usr/bin/env python3
"""
Create a compatible dosha classification model for current environment
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.multioutput import MultiOutputRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import r2_score, mean_absolute_error
import joblib
from pathlib import Path

def create_compatible_dosha_model():
    print("🔧 Creating compatible dosha classification model...")
    print("=" * 55)
    
    # Generate synthetic dosha assessment dataset (same as in Colab)
    np.random.seed(42)
    n_samples = 1000
    
    print("📊 Generating synthetic training data...")
    
    # Initialize data dictionary
    data = {}
    
    # Body constitution questions (10 questions)
    body_options = ['thin', 'medium', 'heavy']
    for i in range(10):
        data[f'body_type_q{i+1}'] = np.random.choice(body_options, n_samples)
    
    # Energy and mood questions (10 questions) 
    energy_options = ['low', 'moderate', 'high']
    for i in range(10):
        data[f'energy_mood_q{i+1}'] = np.random.choice(energy_options, n_samples)
    
    # Digestive system questions (8 questions)
    digest_options = ['weak', 'strong', 'variable']
    for i in range(8):
        data[f'digestion_q{i+1}'] = np.random.choice(digest_options, n_samples)
    
    # Mental/emotional wellness (10 questions, scale 1-5)
    for i in range(10):
        data[f'mental_wellness_q{i+1}'] = np.random.randint(1, 6, n_samples)
    
    # Lifestyle patterns (5 questions)
    lifestyle_options = ['active', 'moderate', 'sedentary']
    for i in range(5):
        data[f'lifestyle_q{i+1}'] = np.random.choice(lifestyle_options, n_samples)
    
    print(f"✅ Generated {len([k for k in data.keys()])} assessment questions")
    
    # Generate realistic dosha percentages
    vata_base = np.random.uniform(15, 55, n_samples)
    pitta_base = np.random.uniform(15, 55, n_samples) 
    kapha_base = np.random.uniform(15, 55, n_samples)
    
    # Normalize to sum to 100
    total = vata_base + pitta_base + kapha_base
    data['vata_percentage'] = np.round((vata_base / total) * 100).astype(int)
    data['pitta_percentage'] = np.round((pitta_base / total) * 100).astype(int)
    data['kapha_percentage'] = np.round((kapha_base / total) * 100).astype(int)
    
    # Ensure percentages sum exactly to 100
    total_check = data['vata_percentage'] + data['pitta_percentage'] + data['kapha_percentage']
    adjustment = 100 - total_check
    data['kapha_percentage'] = data['kapha_percentage'] + adjustment
    
    # Create DataFrame
    df = pd.DataFrame(data)
    target_cols = ['vata_percentage', 'pitta_percentage', 'kapha_percentage']
    feature_cols = [c for c in df.columns if c not in target_cols]
    
    print(f"📋 Dataset created: {df.shape[0]} samples, {len(feature_cols)} features")
    
    # Prepare features and targets
    X = df[feature_cols].copy()
    y = df[target_cols].copy()
    
    # Identify categorical vs numeric features
    categorical_features = []
    numeric_features = []
    
    for col in X.columns:
        if X[col].dtype == 'object':
            categorical_features.append(col)
        else:
            numeric_features.append(col)
    
    print(f"📊 Features: {len(categorical_features)} categorical, {len(numeric_features)} numeric")
    
    # Create preprocessing pipeline
    numeric_transformer = Pipeline(steps=[
        ('scaler', StandardScaler())
    ])
    
    categorical_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore'))
    ])
    
    # Combine preprocessing steps
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ]
    )
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print(f"✂️ Data split: {X_train.shape[0]} training, {X_test.shape[0]} test samples")
    
    # Create the model pipeline
    print("🚀 Training model...")
    model = Pipeline([
        ('preprocessor', preprocessor),
        ('regressor', MultiOutputRegressor(
            DecisionTreeRegressor(
                max_depth=12,
                min_samples_split=10,
                min_samples_leaf=5,
                random_state=42
            )
        ))
    ])
    
    # Train the model
    model.fit(X_train, y_train)
    
    # Make predictions and evaluate
    y_pred = model.predict(X_test)
    
    # Ensure predictions are valid
    y_pred_clipped = np.clip(y_pred, 0, 100)
    row_sums = y_pred_clipped.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1
    y_pred_normalized = (y_pred_clipped / row_sums) * 100
    
    r2 = r2_score(y_test, y_pred_normalized)
    print(f"📊 Model Performance: R² Score = {r2:.4f}")
    
    # Test a sample prediction
    print("\n🧪 Testing sample prediction...")
    sample_X = X_test.iloc[[0]]
    sample_pred = model.predict(sample_X)[0]
    sample_pred = np.clip(sample_pred, 0, 100)
    total = sample_pred.sum()
    if total > 0:
        sample_pred = (sample_pred / total) * 100
    
    print(f"   Sample prediction: Vata={sample_pred[0]:.1f}%, Pitta={sample_pred[1]:.1f}%, Kapha={sample_pred[2]:.1f}%")
    
    # Prepare model artifacts for saving
    artifacts = {
        'model': model,
        'feature_columns': feature_cols,
        'target_columns': target_cols,
        'categorical_features': categorical_features,
        'numeric_features': numeric_features,
        'model_info': {
            'model_type': 'DecisionTreeRegressor with MultiOutput',
            'n_features': len(feature_cols),
            'n_targets': len(target_cols),
            'training_samples': len(X_train),
            'test_r2_score': r2,
            'sklearn_version': '1.7.1',
            'created_locally': True
        }
    }
    
    # Save the model
    model_dir = Path("backend/models")
    model_dir.mkdir(exist_ok=True)
    model_path = model_dir / "dosha_classifier.joblib"
    
    joblib.dump(artifacts, model_path)
    print(f"💾 Model saved to: {model_path}")
    
    return True

if __name__ == "__main__":
    print("🔧 Creating a compatible dosha classification model for your environment...")
    print("   This will replace the Colab-trained model with a locally compatible version.\n")
    
    success = create_compatible_dosha_model()
    
    if success:
        print(f"\n✅ SUCCESS! Compatible dosha model created and saved.")
        print(f"🎉 Your FastAPI backend can now use this model without version conflicts.")
        print(f"🚀 Ready to test the integration!")
    else:
        print(f"\n❌ Failed to create compatible model.")