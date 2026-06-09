import os
from PIL import Image

dir_path = r"C:\Users\anaka\OneDrive\Pictures\mugs design\Cat mug Design"
for name in os.listdir(dir_path):
    if name.lower().endswith(('.png', '.jpg', '.jpeg')):
        path = os.path.join(dir_path, name)
        with Image.open(path) as img:
            print(f"File: {name} | Size: {img.size} | Mode: {img.mode}")
            # Count how many pixels are completely grey (120-200, neutral) vs non-grey
            img_rgb = img.convert('RGB')
            w, h = img_rgb.size
            grey_pixels = 0
            for y in range(h):
                for x in range(w):
                    r, g, b = img_rgb.getpixel((x, y))
                    if abs(r - g) <= 2 and abs(g - b) <= 2 and 120 <= r <= 200:
                        grey_pixels += 1
            print(f"  Grey pixels: {grey_pixels} ({grey_pixels / (w*h) * 100:.2f}%)")
