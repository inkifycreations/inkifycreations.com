import os
import sys
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

pictures_dir = r"C:\Users\anaka\OneDrive\Pictures\mugs design"

print(f"Inspecting images in: {pictures_dir}")
print("-" * 80)

for root, dirs, files in os.walk(pictures_dir):
    for name in files:
        if name.lower().endswith(('.png', '.jpg', '.jpeg')):
            full_path = os.path.join(root, name)
            try:
                with Image.open(full_path) as img:
                    width, height = img.size
                    fmt = img.format
                    size_kb = os.path.getsize(full_path) // 1024
                    rel_path = os.path.relpath(full_path, pictures_dir)
                    print(f"{rel_path} | Format: {fmt} | Dim: {width}x{height} | Size: {size_kb} KB")
            except Exception as e:
                print(f"Error reading {name}: {e}")
