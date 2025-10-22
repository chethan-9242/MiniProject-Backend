"""
Quick Dataset Explorer
Explore what's actually inside your hair disease dataset folder
"""

import os
from pathlib import Path

def explore_directory(path, max_depth=3, current_depth=0):
    """Explore directory structure"""
    
    path = Path(path)
    indent = "  " * current_depth
    
    if not path.exists():
        print(f"{indent}❌ Path does not exist: {path}")
        return
    
    if path.is_file():
        size_mb = path.stat().st_size / (1024 * 1024)
        print(f"{indent}📄 {path.name} ({size_mb:.2f} MB)")
        return
    
    print(f"{indent}📁 {path.name}/")
    
    if current_depth >= max_depth:
        print(f"{indent}  ... (max depth reached)")
        return
    
    try:
        items = list(path.iterdir())
        
        # Sort: directories first, then files
        dirs = [item for item in items if item.is_dir()]
        files = [item for item in items if item.is_file()]
        
        # Show directories
        for item in sorted(dirs):
            explore_directory(item, max_depth, current_depth + 1)
        
        # Show files (limit to first 10)
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif'}
        other_files = []
        image_files = []
        
        for item in sorted(files):
            if item.suffix.lower() in image_extensions:
                image_files.append(item)
            else:
                other_files.append(item)
        
        # Show other files first
        for item in other_files[:5]:  # Limit to first 5
            size_mb = item.stat().st_size / (1024 * 1024)
            print(f"{indent}  📄 {item.name} ({size_mb:.2f} MB)")
        
        # Show sample image files
        if image_files:
            print(f"{indent}  📸 Images found: {len(image_files)} files")
            for item in image_files[:3]:  # Show first 3 as examples
                size_mb = item.stat().st_size / (1024 * 1024)
                print(f"{indent}    🖼️  {item.name} ({size_mb:.2f} MB)")
            
            if len(image_files) > 3:
                print(f"{indent}    ... and {len(image_files) - 3} more image files")
        
        if len(other_files) > 5:
            print(f"{indent}  ... and {len(other_files) - 5} more files")
            
    except PermissionError:
        print(f"{indent}  ❌ Permission denied")
    except Exception as e:
        print(f"{indent}  ❌ Error: {e}")

def main():
    """Main exploration function"""
    print("🔍 DATASET STRUCTURE EXPLORER")
    print("=" * 50)
    
    # Use the path from the previous attempt
    dataset_path = input("Enter dataset path (or press Enter to use previous): ").strip()
    
    if not dataset_path:
        dataset_path = r"C:\Users\Chethan\Downloads\archive (16)\Hair Diseases - Final"
    
    print(f"\n🔍 Exploring: {dataset_path}")
    print("=" * 50)
    
    explore_directory(dataset_path)
    
    print("\n" + "=" * 50)
    print("📊 STRUCTURE ANALYSIS COMPLETE")
    
    # Provide recommendations based on what we find
    path = Path(dataset_path)
    if path.exists():
        items = list(path.iterdir())
        dirs = [item for item in items if item.is_dir()]
        files = [item for item in items if item.is_file()]
        
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif'}
        image_files = [f for f in files if f.suffix.lower() in image_extensions]
        
        print(f"\n📋 SUMMARY:")
        print(f"   📁 Subdirectories: {len(dirs)}")
        print(f"   📸 Image files in root: {len(image_files)}")
        print(f"   📄 Total files: {len(files)}")
        
        if len(dirs) > 0 and len(image_files) == 0:
            print(f"\n💡 RECOMMENDATION:")
            print(f"   The images are likely organized in subdirectories.")
            print(f"   Each subdirectory should represent a hair condition class.")
            
        elif len(image_files) > 0 and len(dirs) == 0:
            print(f"\n💡 RECOMMENDATION:")
            print(f"   All images are in the root folder.")
            print(f"   This dataset needs to be organized by classes.")
            
        elif len(dirs) > 0 and len(image_files) > 0:
            print(f"\n💡 RECOMMENDATION:")
            print(f"   Mixed structure detected. Check subdirectories for organized classes.")
            
    else:
        print(f"❌ Cannot analyze - path does not exist")

if __name__ == "__main__":
    main()