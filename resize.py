#!/usr/bin/env python3
"""
App Store Screenshot Resizer
Crops and resizes screenshots to exact App Store Connect display size dimensions.
"""

import argparse
from PIL import Image
import os

def resize_images(inputs, target_w, target_h):
    for inp in inputs:
        if not os.path.exists(inp):
            print(f"Error: file not found: {inp}")
            continue
        
        # Replace extension with -resized.jpg/png
        base, ext = os.path.splitext(inp)
        # Handle cases where the input is already named -resized
        if base.endswith("-resized"):
            out = inp
        else:
            out = f"{base}-resized{ext}"
            
        img = Image.open(inp)
        w, h = img.size
        
        # Crop to the target aspect ratio, preserving the height, centered horizontally
        crop_w = round(h * target_w / target_h)
        offset_x = round((w - crop_w) / 2)
        
        # Crop: (left, upper, right, lower)
        img_cropped = img.crop((offset_x, 0, offset_x + crop_w, h))
        
        # Resize using LANCZOS filter (safely checks Pillow versions)
        resample_filter = Image.Resampling.LANCZOS if hasattr(Image, 'Resampling') else Image.LANCZOS
        img_resized = img_cropped.resize((target_w, target_h), resample_filter)
        
        img_resized.save(out)
        print(f"OK: Cropped and resized {inp} -> {out} ({target_w}x{target_h})")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Crop and resize screenshots to App Store Connect specifications")
    parser.add_argument("inputs", nargs="+", help="Input image file paths")
    parser.add_argument("--width", type=int, default=1290, help="Target width (default: 1290)")
    parser.add_argument("--height", type=int, default=2796, help="Target height (default: 2796)")
    args = parser.parse_args()
    
    resize_images(args.inputs, args.width, args.height)
