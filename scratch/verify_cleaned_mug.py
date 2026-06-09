import os
import sys
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

mug_body_left = 450
mug_body_right = 1050
mug_body_top = 150
mug_body_bottom = 900
dark_threshold = 120

def count_dark(path):
    img = Image.open(path)
    img_rgb = img.convert('RGB')
    dark_pixels = 0
    for y in range(mug_body_top, mug_body_bottom + 1):
        for x in range(mug_body_left, mug_body_right + 1):
            r, g, b = img_rgb.getpixel((x, y))
            if r < dark_threshold and g < dark_threshold and b < dark_threshold:
                dark_pixels += 1
    return dark_pixels

orig = count_dark("assets/mug.png")
clean = count_dark("assets/mug_blank_test.png")

print(f"Original dark pixels: {orig}")
print(f"Cleaned dark pixels:  {clean}")
print(f"Removed dark pixels:  {orig - clean}")
