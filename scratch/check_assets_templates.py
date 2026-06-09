import os
import sys
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')
assets_dir = r"c:\Users\anaka\Downloads\third app\third app\assets"

print("Analyzing assets templates:")
print("=" * 80)

for name in sorted(os.listdir(assets_dir)):
    if name.lower().endswith(('.png', '.jpg', '.jpeg')):
        path = os.path.join(assets_dir, name)
        with Image.open(path) as img:
            w, h = img.size
            mode = img.mode
            img_rgb = img.convert('RGB')
            # Check for grey ratio
            grey_count = 0
            for y in range(0, h, 4):
                for x in range(0, w, 4):
                    r, g, b = img_rgb.getpixel((x, y))
                    if abs(r - g) <= 2 and abs(g - b) <= 2 and 120 <= r <= 200:
                        grey_count += 1
            total_sampled = (w // 4) * (h // 4)
            grey_ratio = (grey_count / total_sampled) if total_sampled > 0 else 0
            print(f"File: {name:25s} | Size: {w:4d}x{h:4d} | Mode: {mode:4s} | Grey Ratio: {grey_ratio:6.2%}")
print("=" * 80)
