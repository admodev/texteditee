#!/usr/bin/env python3
"""
Convert PNG image to ICO format for Windows installer.
Requires Pillow: pip install Pillow
"""

from PIL import Image
import sys
import os

def create_ico(png_path, ico_path):
    """Convert PNG to ICO with multiple sizes."""
    try:
        img = Image.open(png_path)
        
        # Convert to RGBA if needed
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Create multiple sizes for ICO
        sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        
        # Resize and save as ICO
        img.save(ico_path, format='ICO', sizes=sizes)
        print(f"✓ Icon created: {ico_path}")
        return True
        
    except Exception as e:
        print(f"✗ Error creating icon: {e}")
        return False

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Look for PNG in common locations
    png_candidates = [
        os.path.join(script_dir, "texteditee_icon.png"),
        os.path.join(script_dir, "..", "..", "texteditee_icon.png"),
    ]
    
    png_path = None
    for candidate in png_candidates:
        if os.path.exists(candidate):
            png_path = candidate
            break
    
    if not png_path:
        print("✗ PNG icon not found. Please provide path as argument:")
        print(f"  python create_icon.py <path_to_png>")
        if len(sys.argv) > 1:
            png_path = sys.argv[1]
        else:
            sys.exit(1)
    
    ico_path = os.path.join(script_dir, "icon.ico")
    
    print(f"Converting {png_path} to {ico_path}...")
    
    if create_ico(png_path, ico_path):
        print("✓ Icon conversion successful!")
        sys.exit(0)
    else:
        sys.exit(1)
