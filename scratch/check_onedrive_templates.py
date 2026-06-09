import os
import sys
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')
pictures_dir = r"C:\Users\anaka\OneDrive\Pictures\mugs design"

print("Analyzing original OneDrive templates:")
print("=" * 100)

for root, dirs, files in os.walk(pictures_dir):
    if "outputs" in root.lower() or "output" in root.lower():
        continue
    folder_name = os.path.relpath(root, pictures_dir)
    for name in sorted(files):
        if name.lower().endswith(('.png', '.jpg', '.jpeg')):
            # Skip the actual photo inputs
            if "chatgpt" in name.lower() or "jun 9" in name.lower():
                continue
            path = os.path.join(root, name)
            try:
                with Image.open(path) as img:
                    w, h = img.size
                    mode = img.mode
                    img_rgb = img.convert('RGB')
                    grey_count = 0
                    for y in range(0, h, 4):
                        for x in range(0, w, 4):
                            r, g, b = img_rgb.getpixel((x, y))
                            if abs(r - g) <= 3 and abs(g - b) <= 3 and 110 <= r <= 210:
                                grey_count += 1
                    total_sampled = (w // 4) * (h // 4)
                    grey_ratio = (grey_count / total_sampled) if total_sampled > 0 else 0
                    print(f"Folder: {folder_name:25s} | File: {name:30s} | Size: {w:4d}x{h:4d} | Grey Ratio: {grey_ratio:6.2%}")
            except Exception as e:
                print(f"Error reading {name}: {e}")
print("=" * 100)
