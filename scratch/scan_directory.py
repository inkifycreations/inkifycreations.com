import os
import sys
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')
pictures_dir = r"C:\Users\anaka\OneDrive\Pictures\mugs design"

print("Detailed scan of all subfolders:")
print("=" * 100)

for root, dirs, files in os.walk(pictures_dir):
    folder_name = os.path.relpath(root, pictures_dir)
    if folder_name == ".":
        continue
    print(f"\nFolder: '{folder_name}'")
    for name in sorted(files):
        if name.lower().endswith(('.png', '.jpg', '.jpeg')):
            path = os.path.join(root, name)
            try:
                with Image.open(path) as img:
                    w, h = img.size
                    mode = img.mode
                    # Check for grey pixels
                    img_rgb = img.convert('RGB')
                    grey_count = 0
                    # Check a sample of pixels to see if it contains grey regions
                    # Let's count how many pixels have neutral grey colors (120-200, R=G=B)
                    for y in range(0, h, 4):
                        for x in range(0, w, 4):
                            r, g, b = img_rgb.getpixel((x, y))
                            if abs(r - g) <= 2 and abs(g - b) <= 2 and 120 <= r <= 200:
                                grey_count += 1
                    total_sampled = (w // 4) * (h // 4)
                    grey_ratio = (grey_count / total_sampled) if total_sampled > 0 else 0
                    print(f"  - {name:40s} | {w:4d}x{h:4d} | Mode: {mode:4s} | Grey Ratio: {grey_ratio:6.2%}")
            except Exception as e:
                print(f"  - {name:40s} | Error: {e}")

print("=" * 100)
