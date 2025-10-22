"""
Hair Disease Dataset Analyzer
Run this script to analyze your downloaded Kaggle hair disease dataset
"""

import os
from pathlib import Path
from PIL import Image
import json
from collections import Counter

def analyze_hair_dataset(dataset_path):
    """
    Analyze the hair disease dataset and provide comprehensive report
    
    Args:
        dataset_path: Path to the downloaded hair disease dataset folder
    """
    
    print("🔬 HAIR DISEASE DATASET ANALYSIS")
    print("=" * 50)
    
    dataset_path = Path(dataset_path)
    
    if not dataset_path.exists():
        print(f"❌ Dataset path not found: {dataset_path}")
        print("Please check the path and try again.")
        return
    
    # 1. Find dataset structure
    print(f"📁 Dataset Location: {dataset_path}")
    print(f"📁 Dataset exists: {'✅' if dataset_path.exists() else '❌'}")
    
    # Find all subdirectories (classes)
    classes = []
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff'}
    
    for item in dataset_path.iterdir():
        if item.is_dir():
            # Check if directory contains images
            has_images = any(
                file.suffix.lower() in image_extensions 
                for file in item.iterdir() 
                if file.is_file()
            )
            if has_images:
                classes.append(item.name)
    
    # If no subdirectories with images, check if images are in root
    if not classes:
        root_images = [
            file for file in dataset_path.iterdir() 
            if file.is_file() and file.suffix.lower() in image_extensions
        ]
        if root_images:
            print("⚠️  Images found in root directory (not organized by class)")
            print("   This dataset might need restructuring.")
            return analyze_flat_dataset(dataset_path)
    
    print(f"\n📊 DATASET STRUCTURE:")
    print(f"   Number of classes: {len(classes)}")
    
    # 2. Analyze each class
    class_details = {}
    total_images = 0
    all_resolutions = []
    all_file_sizes = []
    
    for class_name in sorted(classes):
        class_path = dataset_path / class_name
        
        # Count images in this class
        class_images = [
            file for file in class_path.iterdir()
            if file.is_file() and file.suffix.lower() in image_extensions
        ]
        
        class_count = len(class_images)
        total_images += class_count
        
        # Sample a few images to check quality
        sample_images = class_images[:min(5, class_count)]  # Sample up to 5 images
        resolutions = []
        file_sizes = []
        
        for img_path in sample_images:
            try:
                # Get file size
                file_size = img_path.stat().st_size / (1024 * 1024)  # MB
                file_sizes.append(file_size)
                all_file_sizes.append(file_size)
                
                # Get image resolution
                with Image.open(img_path) as img:
                    width, height = img.size
                    resolutions.append((width, height))
                    all_resolutions.append((width, height))
                    
            except Exception as e:
                print(f"⚠️  Error reading {img_path.name}: {e}")
        
        # Calculate average resolution for this class
        if resolutions:
            avg_width = sum(r[0] for r in resolutions) / len(resolutions)
            avg_height = sum(r[1] for r in resolutions) / len(resolutions)
            avg_file_size = sum(file_sizes) / len(file_sizes)
        else:
            avg_width = avg_height = avg_file_size = 0
        
        class_details[class_name] = {
            'count': class_count,
            'avg_resolution': (int(avg_width), int(avg_height)),
            'avg_file_size_mb': round(avg_file_size, 2),
            'sample_resolutions': resolutions[:3]  # Show first 3
        }
        
        # Status indicator
        status = "✅" if class_count >= 100 else "⚠️" if class_count >= 50 else "❌"
        print(f"   {status} {class_name}: {class_count} images")
    
    print(f"\n📈 DETAILED CLASS ANALYSIS:")
    for class_name, details in class_details.items():
        print(f"\n🏷️  Class: {class_name}")
        print(f"   📸 Image count: {details['count']}")
        print(f"   📐 Avg resolution: {details['avg_resolution'][0]}x{details['avg_resolution'][1]}")
        print(f"   💾 Avg file size: {details['avg_file_size_mb']} MB")
        
        if details['sample_resolutions']:
            print(f"   🔍 Sample resolutions: {details['sample_resolutions']}")
        
        # Recommendations
        if details['count'] < 50:
            print(f"   ❌ INSUFFICIENT DATA - Need at least 50 images per class")
        elif details['count'] < 100:
            print(f"   ⚠️  LOW DATA - Recommend 100+ images per class")
        else:
            print(f"   ✅ SUFFICIENT DATA")
    
    # 3. Overall dataset statistics
    print(f"\n📊 OVERALL DATASET STATISTICS:")
    print(f"   📁 Total classes: {len(classes)}")
    print(f"   📸 Total images: {total_images}")
    print(f"   📸 Avg images per class: {total_images // len(classes) if classes else 0}")
    
    if all_resolutions:
        # Most common resolution
        resolution_counts = Counter(all_resolutions)
        most_common_res = resolution_counts.most_common(1)[0]
        
        # Resolution range
        widths = [r[0] for r in all_resolutions]
        heights = [r[1] for r in all_resolutions]
        
        print(f"   📐 Most common resolution: {most_common_res[0]} (appears {most_common_res[1]} times)")
        print(f"   📐 Resolution range: {min(widths)}x{min(heights)} to {max(widths)}x{max(heights)}")
    
    if all_file_sizes:
        avg_size = sum(all_file_sizes) / len(all_file_sizes)
        print(f"   💾 Average file size: {avg_size:.2f} MB")
    
    # 4. Training readiness assessment
    print(f"\n🎯 TRAINING READINESS ASSESSMENT:")
    
    ready_classes = sum(1 for details in class_details.values() if details['count'] >= 100)
    partial_classes = sum(1 for details in class_details.values() if 50 <= details['count'] < 100)
    insufficient_classes = sum(1 for details in class_details.values() if details['count'] < 50)
    
    print(f"   ✅ Ready classes (100+ images): {ready_classes}")
    print(f"   ⚠️  Partial classes (50-99 images): {partial_classes}")
    print(f"   ❌ Insufficient classes (<50 images): {insufficient_classes}")
    
    # Overall recommendation
    if ready_classes >= 3 and insufficient_classes == 0:
        print(f"\n🎉 EXCELLENT! Dataset is ready for training.")
        print(f"   Expected accuracy: 75-85%")
    elif ready_classes + partial_classes >= 3 and insufficient_classes <= 1:
        print(f"\n✅ GOOD! Dataset can be used for training with decent results.")
        print(f"   Expected accuracy: 65-75%")
    elif total_images >= 500:
        print(f"\n⚠️  FAIR! Dataset can be used but may need data augmentation.")
        print(f"   Expected accuracy: 55-70%")
    else:
        print(f"\n❌ INSUFFICIENT! Dataset needs more data for reliable training.")
        print(f"   Expected accuracy: <60%")
    
    # 5. Save analysis report
    report = {
        "dataset_path": str(dataset_path),
        "total_classes": len(classes),
        "total_images": total_images,
        "classes": class_details,
        "ready_for_training": ready_classes >= 3 and insufficient_classes == 0
    }
    
    report_path = Path("hair_dataset_analysis_report.json")
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n💾 Analysis report saved to: {report_path}")
    
    return report

def analyze_flat_dataset(dataset_path):
    """Analyze dataset where all images are in one folder (not organized by class)"""
    
    print("📁 FLAT DATASET STRUCTURE DETECTED")
    print("   All images appear to be in the root directory.")
    print("   Checking image files...")
    
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff'}
    
    all_images = [
        file for file in dataset_path.iterdir()
        if file.is_file() and file.suffix.lower() in image_extensions
    ]
    
    print(f"\n📊 BASIC STATISTICS:")
    print(f"   📸 Total images found: {len(all_images)}")
    
    if len(all_images) == 0:
        print("❌ No images found in dataset!")
        return
    
    # Check a sample of images
    sample_images = all_images[:min(10, len(all_images))]
    resolutions = []
    
    print(f"\n🔍 SAMPLE IMAGE ANALYSIS:")
    for i, img_path in enumerate(sample_images, 1):
        try:
            with Image.open(img_path) as img:
                width, height = img.size
                file_size = img_path.stat().st_size / (1024 * 1024)
                resolutions.append((width, height))
                print(f"   {i}. {img_path.name}: {width}x{height}, {file_size:.2f} MB")
                
        except Exception as e:
            print(f"   {i}. {img_path.name}: ❌ Error - {e}")
    
    print(f"\n⚠️  DATASET NEEDS ORGANIZATION:")
    print(f"   This dataset needs to be organized into class folders.")
    print(f"   Each hair condition should have its own folder.")
    print(f"   Example structure:")
    print(f"   hair-diseases/")
    print(f"   ├── alopecia/")
    print(f"   ├── dandruff/")
    print(f"   ├── psoriasis/")
    print(f"   └── ...")

def main():
    """Main function to run dataset analysis"""
    print("🔬 HAIR DISEASE DATASET ANALYZER")
    print("=" * 50)
    
    # Get dataset path from user
    print("Please provide the path to your downloaded hair disease dataset:")
    print("Example: C:\\Users\\YourName\\Downloads\\hair-diseases")
    print("Or drag and drop the folder here and press Enter:")
    
    dataset_path = input("\nDataset path: ").strip().strip('"')
    
    if not dataset_path:
        print("❌ No path provided. Please run the script again.")
        return
    
    # Run analysis
    try:
        analyze_hair_dataset(dataset_path)
        
        print("\n" + "=" * 50)
        print("✅ Analysis complete!")
        print("Check the report above to see if your dataset is ready for training.")
        
    except Exception as e:
        print(f"\n💥 Error during analysis: {str(e)}")
        print("Please check the dataset path and try again.")

if __name__ == "__main__":
    main()