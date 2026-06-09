import os
import sys
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')
birthday_dir = r"C:\Users\anaka\OneDrive\Pictures\mugs design\birthday"

print("Analyzing birthday folder visual contents:")
print("=" * 80)

for name in sorted(os.listdir(birthday_dir)):
    if name.lower().endswith(('.png', '.jpg', '.jpeg')):
        # Skip the large actual photo for now
        if "chatgpt" in name.lower() or "jun 9" in name.lower():
            continue
            
        path = os.path.join(birthday_dir, name)
        with Image.open(path) as img:
            w, h = img.size
            # Let's count number of unique colors to see if it's a photo or graphic
            img_rgb = img.convert('RGB')
            pixels = list(img_rgb.getdata())
            unique_colors = len(set(pixels))
            
            # Check if there is any white area or if it looks like a photo
            print(f"File: {name} | Size: {w}x{h} | Unique Colors: {unique_colors}")
            # Check if it has any solid color rectangular areas (which could be frames)
            # We will print the color of the corners and center
            corners = [
                img_rgb.getpixel((0, 0)),
                img_rgb.getpixel((w - 1, 0)),
                img_rgb.getpixel((0, h - 1)),
                img_rgb.getpixel((w - 1, h - 1)),
                img_rgb.getpixel((w // 2, h // 2))
            ]
            print(f"  Corners & Center colors: {corners}")
print("=" * 80)
