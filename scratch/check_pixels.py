import os
from PIL import Image

path = r"C:\Users\anaka\OneDrive\Pictures\mugs design\Dad gesign\awesome dad.png"

if os.path.exists(path):
    with Image.open(path) as img:
        print(f"File: {path}")
        print(f"Size: {img.size} | Mode: {img.mode}")
        img_rgb = img.convert('RGB')
        w, h = img_rgb.size
        # Check grey pixels
        grey_count = 0
        for y in range(h):
            for x in range(w):
                r, g, b = img_rgb.getpixel((x, y))
                if abs(r - g) <= 3 and abs(g - b) <= 3 and 110 <= r <= 210:
                    grey_count += 1
        print(f"Grey pixels: {grey_count} ({grey_count / (w * h) * 100:.2f}%)")
else:
    print("File does not exist.")
