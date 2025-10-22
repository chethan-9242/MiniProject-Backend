#!/usr/bin/env python3
"""
Extract training information from saved PyTorch model files
"""
import torch
import json
from pathlib import Path

def extract_skin_model_info(model_path):
    """Extract info from skin model files"""
    try:
        model = torch.load(model_path, map_location='cpu')
        info = {
            'architecture': model.get('model_architecture', 'Unknown'),
            'best_val_accuracy': model.get('best_val_accuracy', 0),
            'num_classes': model.get('num_classes', 0),
        }
        
        history = model.get('training_history', {})
        train_acc = history.get('train_accuracies', [])
        val_acc = history.get('val_accuracies', [])
        
        if train_acc:
            info['final_train_accuracy'] = train_acc[-1]
        if val_acc:
            info['final_val_accuracy'] = val_acc[-1]
            
        return info
    except Exception as e:
        return {'error': str(e)}

def main():
    models_dir = Path('models')
    
    # Skin models
    skin_models = ['skin_classifier.pth', 'skin_classifier_fast.pth', 'skin_classifier_improved.pth']
    
    print("=== SKIN DISEASE MODELS ===")
    for model_file in skin_models:
        model_path = models_dir / model_file
        if model_path.exists():
            print(f"\n--- {model_file} ---")
            info = extract_skin_model_info(model_path)
            for key, value in info.items():
                if 'accuracy' in key and isinstance(value, (int, float)):
                    print(f"{key}: {value:.2f}%")
                else:
                    print(f"{key}: {value}")
    
    # Hair models
    hair_models = ['hair_classifier_improved.pth']
    
    print("\n\n=== HAIR ANALYSIS MODELS ===")
    for model_file in hair_models:
        model_path = models_dir / model_file
        if model_path.exists():
            print(f"\n--- {model_file} ---")
            info = extract_skin_model_info(model_path)  # Same function works for hair models
            for key, value in info.items():
                if 'accuracy' in key and isinstance(value, (int, float)):
                    print(f"{key}: {value:.2f}%")
                else:
                    print(f"{key}: {value}")

if __name__ == "__main__":
    main()