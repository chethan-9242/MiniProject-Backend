#!/usr/bin/env python3
"""
Fix dataset structure for skin disease training
"""

import os
import shutil
from pathlib import Path

def fix_dataset_structure():
    """
    Fix the dataset structure to match expected format
    """
    print("🔧 Fixing dataset structure...")
    
    # Source and destination paths
    source_dir = Path("data/skin_disease")
    train_source = source_dir / "train_set"
    test_source = source_dir / "test_set"
    
    # Create new structure
    train_dest = source_dir / "train"
    test_dest = source_dir / "test"
    
    # Remove existing train/test folders if they exist
    if train_dest.exists():
        shutil.rmtree(train_dest)
    if test_dest.exists():
        shutil.rmtree(test_dest)
    
    # Copy train_set to train
    if train_source.exists():
        print(f"📁 Copying {train_source} to {train_dest}")
        shutil.copytree(train_source, train_dest)
        print("✅ Training data copied successfully")
    else:
        print(f"❌ Source training directory not found: {train_source}")
        return False
    
    # Copy test_set to test
    if test_source.exists():
        print(f"📁 Copying {test_source} to {test_dest}")
        shutil.copytree(test_source, test_dest)
        print("✅ Test data copied successfully")
    else:
        print(f"❌ Source test directory not found: {test_source}")
        return False
    
    # Count classes and images
    train_classes = [d.name for d in train_dest.iterdir() if d.is_dir()]
    test_classes = [d.name for d in test_dest.iterdir() if d.is_dir()]
    
    print(f"\n📊 Dataset Summary:")
    print(f"   Training classes: {len(train_classes)}")
    print(f"   Test classes: {len(test_classes)}")
    
    total_train_images = 0
    total_test_images = 0
    
    print(f"\n📁 Training data:")
    for class_name in train_classes:
        class_path = train_dest / class_name
        image_count = len(list(class_path.glob("*.*")))
        total_train_images += image_count
        print(f"   {class_name}: {image_count} images")
    
    print(f"\n📁 Test data:")
    for class_name in test_classes:
        class_path = test_dest / class_name
        image_count = len(list(class_path.glob("*.*")))
        total_test_images += image_count
        print(f"   {class_name}: {image_count} images")
    
    print(f"\n📈 Total images:")
    print(f"   Training: {total_train_images}")
    print(f"   Test: {total_test_images}")
    print(f"   Total: {total_train_images + total_test_images}")
    
    print(f"\n✅ Dataset structure fixed successfully!")
    print(f"🎯 Ready for training with {len(train_classes)} classes")
    
    return True

if __name__ == "__main__":
    success = fix_dataset_structure()
    if success:
        print("\n🚀 You can now run: py train_skin_model_improved.py")
    else:
        print("\n❌ Failed to fix dataset structure")
