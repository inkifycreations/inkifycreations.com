import os
import sys
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

def analyze_image(path):
    img = Image.open(path)
    w, h = img.size
    img_rgb = img.convert('RGB')
    
    # We sample a grid and count the colors
    # Let's count how many pixels are dark (likely the cat print) on the mug body.
    # The mug body is usually in the center.
    dark_pixels = 0
    for y in range(h):
        for x in range(w):
            r, g, b = img_rgb.getpixel((x, y))
            # Dark pixels (less than 80)
            if r < 80 and g < 80 and b < 80:
                dark_pixels += 1
                
    print(f"File: {os.path.basename(path)}")
    print(f"  Dimensions: {w}x{h}")
    print(f"  Total pixels: {w*h}")
    print(f"  Dark pixels (<80 RGB): {dark_pixels} ({dark_pixels / (w*h):.2%})")

analyze_image("assets/mug.png")
if os.path.exists("assets/mug_photo_print.png"):
    analyze_image("assets/mug_photo_print.png")
