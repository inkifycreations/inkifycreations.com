import os
import sys
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')
birthday_dir = r"C:\Users\anaka\OneDrive\Pictures\mugs design\birthday"

print("Detailed scan of birthday folder:")
print("=" * 100)

for name in sorted(os.listdir(birthday_dir)):
    if name.lower().endswith(('.png', '.jpg', '.jpeg')):
        path = os.path.join(birthday_dir, name)
        with Image.open(path) as img:
            w, h = img.size
            mode = img.mode
            # Let's count how many grey pixels there are, but with a broader range or other colors
            img_rgb = img.convert('RGB')
            # Let's check if the image contains any transparency
            has_transparency = "transparency" in img.info or mode == "RGBA"
            print(f"File: {name:40s} | Size: {w:4d}x{h:4d} | Mode: {mode:4s} | Has Trans: {has_transparency}")
            
            # Let's sample colors to see if there's any dominant color or grey areas
            colors = {}
            for y in range(0, h, 8):
                for x in range(0, w, 8):
                    r, g, b = img_rgb.getpixel((x, y))
                    color = (r, g, b)
                    colors[color] = colors.get(color, 0) + 1
            sorted_colors = sorted(colors.items(), key=lambda x: x[1], reverse=True)
            print("  Top colors:")
            for c, count in sorted_colors[:5]:
                print(f"    - RGB{c}: {count} pixels")
print("=" * 100)
